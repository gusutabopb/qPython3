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

from qpython3 import qconnection


if __name__ == '__main__':
    # create connection object
    q = qconnection.QConnection(host='localhost', port=5000)
    # initialize connection
    q.open()

    print(q)
    print('IPC version: %s. Is connected: %s' % (q.protocol_version, q.is_connected()))

    # simple query execution via: QConnection.__call__
    data = q('{`int$ til x}', 10)
    print(f'type: {type(data)}, numpy.dtype: {data.dtype}, '
          f'meta.qtype: {data.meta.qtype}, data: {data}')

    # simple query execution via: QConnection.sync
    data = q.sync('{`long$ til x}', 10)
    print(f'type: {type(data)}, numpy.dtype: {data.dtype}, '
          f'meta.qtype: {data.meta.qtype}, data: {data}')

    # low-level query and read
    q.query(qconnection.MessageType.SYNC, '{`short$ til x}', 10) # sends a SYNC query
    msg = q.receive(data_only=False, raw=False) # retrieve entire message
    print(f'type: {type(msg)}, message type: {msg.type}, '
          f'data size: {msg.size}, is_compressed: {msg.is_compressed}')
    data = msg.data
    print(f'type: {type(data)}, numpy.dtype: {data.dtype}, '
          f'meta.qtype: {data.meta.qtype}, data: {data}')
    # close connection
    q.close()

