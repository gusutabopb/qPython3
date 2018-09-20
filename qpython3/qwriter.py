#
#  Copyright (c) 2011-2014 Exxeleron GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

import struct
from io import BytesIO

from . import MetaData, CONVERSION_OPTIONS
from .qtype import *  # @UnusedWildImport
from .qcollection import qlist, QList, QTemporalList, QDictionary, QTable, QKeyedTable, get_list_qtype
from .qtemporal import QTemporal, to_raw_qtemporal, array_to_raw_qtemporal


class QWriterException(Exception):
    '''
    Indicates an error raised during data serialization.
    '''
    pass



ENDIANESS = '\1' if sys.byteorder == 'little' else '\0'


class QWriter(object):
    '''
    Provides serialization to q IPC protocol.
    
    :Parameters:
     - `stream` (`socket` or `None`) - stream for data serialization
     - `protocol_version` (`integer`) - version IPC protocol
     - `encoding` (`string`) - encoding for characters serialization
    
    :Attrbutes:
     - `_writer_map` - stores mapping between Python types and functions 
       responsible for serializing into IPC representation
    '''

    _writer_map = {}
    serialize = Mapper(_writer_map)


    def __init__(self, stream, protocol_version, encoding = 'latin-1'):
        self._stream = stream
        self._protocol_version = protocol_version
        self._encoding = encoding


    def write(self, data, msg_type, **options):
        '''Serializes and pushes single data object to a wrapped stream.
        
        :Parameters:
         - `data` - data to be serialized
         - `msg_type` (one of the constants defined in :class:`.MessageType`) -
           type of the message
        :Options:
         - `single_char_strings` (`boolean`) - if ``True`` single char Python 
           strings are encoded as q strings instead of chars, 
           **Default**: ``False``
        
        :returns: if wraped stream is ``None`` serialized data, 
                  otherwise ``None`` 
        '''
        self._buffer = BytesIO()

        self._options = MetaData(**CONVERSION_OPTIONS.union_dict(**options))

        # header and placeholder for message size
        self._buffer.write(('%s%s\0\0\0\0\0\0' % (ENDIANESS, chr(msg_type))).encode(self._encoding))

        self._write(data)

        # update message size
        data_size = self._buffer.tell()
        self._buffer.seek(4)
        self._buffer.write(struct.pack('i', data_size))

        # write data to socket
        if self._stream:
            self._stream.sendall(self._buffer.getvalue())
        else:
            return self._buffer.getvalue()


    def _write(self, data):
        if data is None:
            self._write_null()
        else:
            if isinstance(data, Exception) or (type(data) == type and issubclass(data, Exception)):
                data_type = Exception
            else:
                data_type = type(data)

            writer = self._get_writer(data_type)

            if writer:
                writer(self, data)
            else:
                qtype = Q_TYPE.get(type(data), None)

                if qtype:
                    self._write_atom(data, qtype)
                else:
                    t = data.__class__ if isinstance(data, object) else type(data)
                    raise QWriterException(f'Unable to serialize type: {t!r}')


    def _get_writer(self, data_type):
        return self._writer_map.get(data_type, None)


    def _write_null(self):
        self._buffer.write(struct.pack('=bx', QNULL))


    @serialize(Exception)
    def _write_error(self, data):
        self._buffer.write(struct.pack('b', QERROR))
        if isinstance(data, Exception):
            msg = data.__class__.__name__
            if data.args:
                msg = data.args[0]
        else:
            msg = data.__name__

        self._buffer.write(msg.encode(self._encoding))
        self._buffer.write(b'\0')


    def _write_atom(self, data, qtype):
        try:
            self._buffer.write(struct.pack('b', qtype))
            fmt = STRUCT_MAP[qtype]
            if isinstance(data, np.bool_):
                self._buffer.write(struct.pack(fmt, bool(data)))
            else:
                self._buffer.write(struct.pack(fmt, data))
        except KeyError:
            t = data.__class__ if isinstance(data, object) else type(data)
            raise QWriterException(f'Unable to serialize type: {t!r}')


    @serialize(tuple, list)
    def _write_generic_list(self, data):
        self._buffer.write(struct.pack('=bxi', QGENERAL_LIST, len(data)))
        for element in data:
            self._write(element)


    @serialize(str, bytes)
    def _write_string(self, data):
        if not self._options.single_char_strings and len(data) == 1:
            self._write_atom(ord(data), QCHAR)
        else:
            self._buffer.write(struct.pack('=bxi', QSTRING, len(data)))
            if isinstance(data, str):
                self._buffer.write(data.encode(self._encoding))
            else:
                self._buffer.write(data)


    @serialize(np.string_)
    def _write_symbol(self, data):
        self._buffer.write(struct.pack('=b', QSYMBOL))
        if data:
            self._buffer.write(data)
        self._buffer.write(b'\0')


    @serialize(uuid.UUID)
    def _write_guid(self, data):
        if self._protocol_version < 3:
            raise QWriterException('kdb+ protocol version violation: Guid not supported pre kdb+ v3.0')

        self._buffer.write(struct.pack('=b', QGUID))
        self._buffer.write(data.bytes)


    @serialize(QTemporal)
    def _write_temporal(self, data):
        try:
            if self._protocol_version < 1 and (data.meta.qtype == QTIMESPAN or data.meta.qtype == QTIMESTAMP):
                raise QWriterException('kdb+ protocol version violation: data type %s not supported pre kdb+ v2.6' % hex(data.meta.qtype))

            self._buffer.write(struct.pack('=b', data.meta.qtype))
            fmt = STRUCT_MAP[data.meta.qtype]
            self._buffer.write(struct.pack(fmt, to_raw_qtemporal(data.raw, data.meta.qtype)))
        except KeyError:
            raise QWriterException('Unable to serialize type: %s' % type(data))


    @serialize(np.datetime64, np.timedelta64)
    def _write_numpy_temporal(self, data):
        try:
            qtype = TEMPORAL_PY_TYPE[str(data.dtype)]

            if self._protocol_version < 1 and (qtype == QTIMESPAN or qtype == QTIMESTAMP):
                raise QWriterException(f'kdb+ protocol version violation: '
                                       f'data type {hex(qtype)} not supported pre kdb+ v2.6')

            self._buffer.write(struct.pack('=b', qtype))
            fmt = STRUCT_MAP[qtype]
            self._buffer.write(struct.pack(fmt, to_raw_qtemporal(data, qtype)))
        except KeyError:
            raise QWriterException(f'Unable to serialize type: {data.dtype}')


    @serialize(QLambda)
    def _write_lambda(self, data):
        self._buffer.write(struct.pack('=b', QLAMBDA))
        self._buffer.write(b'\0')
        self._write_string(data.expression)


    @serialize(QProjection)
    def _write_projection(self, data):
        self._buffer.write(struct.pack('=bi', QPROJECTION, len(data.parameters)))
        for parameter in data.parameters:
            self._write(parameter)


    @serialize(QDictionary, QKeyedTable)
    def _write_dictionary(self, data):
        self._buffer.write(struct.pack('=b', QDICTIONARY))
        self._write(data.keys)
        self._write(data.values)


    @serialize(QTable)
    def _write_table(self, data):
        self._buffer.write(struct.pack('=bxb', QTABLE, QDICTIONARY))
        self._write(qlist(np.array(data.dtype.names), qtype = QSYMBOL_LIST))
        self._buffer.write(struct.pack('=bxi', QGENERAL_LIST, len(data.dtype)))
        for column in data.dtype.names:
            self._write_list(data[column], data.meta[column])


    @serialize(np.ndarray, QList, QTemporalList)
    def _write_list(self, data, qtype = None):
        if qtype is not None:
            qtype = -abs(qtype)

        if qtype is None:
            qtype = get_list_qtype(data)

        if self._protocol_version < 1 and (abs(qtype) == QTIMESPAN_LIST or abs(qtype) == QTIMESTAMP_LIST):
            raise QWriterException(f'kdb+ protocol version violation: '
                                   f'data type {hex(data.meta.qtype)} not supported pre kdb+ v2.6')

        if qtype == QGENERAL_LIST:
            self._write_generic_list(data)
        elif qtype == QCHAR:
            self._write_string(data.tostring())
        else:
            self._buffer.write(struct.pack('=bxi', -qtype, len(data)))
            if data.dtype.type in (np.datetime64, np.timedelta64):
                # convert numpy temporal to raw q temporal
                data = array_to_raw_qtemporal(data, qtype = qtype)

            if qtype == QSYMBOL:
                for symbol in data:
                    if symbol:
                        self._buffer.write(symbol)
                    self._buffer.write(b'\0')
            elif qtype == QGUID:
                if self._protocol_version < 3:
                    raise QWriterException('kdb+ protocol version violation: '
                                           'Guid not supported pre kdb+ v3.0')

                for guid in data:
                    self._buffer.write(guid.bytes)
            else:
                self._buffer.write(data.tostring())

