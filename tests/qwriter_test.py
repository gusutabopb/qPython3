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

import binascii
import sys
if sys.version > '3':
    long = int

from collections import OrderedDict
from qpython3 import qwriter
from qpython3.qtype import *  # @UnusedWildImport
from qpython3.qcollection import qlist, QDictionary, qtable, QKeyedTable
from qpython3.qtemporal import qtemporal, to_raw_qtemporal, array_to_raw_qtemporal

BINARY = OrderedDict()

EXPRESSIONS = OrderedDict((
    (b'("G"$"8c680a01-5a49-5aab-5a65-d4bfddb6a661"; 0Ng)',
                                                      qlist(np.array([uuid.UUID('8c680a01-5a49-5aab-5a65-d4bfddb6a661'), qnull(QGUID)]), qtype=QGUID_LIST)),
    (b'"G"$"8c680a01-5a49-5aab-5a65-d4bfddb6a661"',    uuid.UUID('8c680a01-5a49-5aab-5a65-d4bfddb6a661')),
    (b'"G"$"00000000-0000-0000-0000-000000000000"',    uuid.UUID('00000000-0000-0000-0000-000000000000')),
    (b'(2001.01m; 0Nm)',                               (qlist(np.array([to_raw_qtemporal(np.datetime64('2001-01', 'M'), QMONTH), qnull(QMONTH)]), qtype=QMONTH_LIST),
                                                       qlist(np.array([12, qnull(QMONTH)]), qtype=QMONTH_LIST),
                                                       qlist(array_to_raw_qtemporal(np.array([np.datetime64('2001-01', 'M'), np.datetime64('NaT', 'M')]), qtype = QMONTH_LIST), qtype = QMONTH_LIST),
                                                       qlist([12, qnull(QMONTH)], qtype=QMONTH_LIST),
                                                       qlist(np.array([np.datetime64('2001-01'), np.datetime64('NaT')], dtype='datetime64[M]'), qtype=QMONTH_LIST),
                                                       np.array([np.datetime64('2001-01'), np.datetime64('NaT')], dtype='datetime64[M]'),
                                                       )),
    (b'2001.01m',                                      (qtemporal(np.datetime64('2001-01', 'M'), qtype=QMONTH),
                                                       np.datetime64('2001-01', 'M'))),
    (b'0Nm',                                           (qtemporal(qnull(QMONTH), qtype=QMONTH),
                                                       qtemporal(np.datetime64('NaT', 'M'), qtype=QMONTH),
                                                       np.datetime64('NaT', 'M'))),
    (b'2001.01.01 2000.05.01 0Nd',                     (qlist(np.array([to_raw_qtemporal(np.datetime64('2001-01-01', 'D'), qtype=QDATE), to_raw_qtemporal(np.datetime64('2000-05-01', 'D'), qtype=QDATE), qnull(QDATE)]), qtype=QDATE_LIST),
                                                       qlist(np.array([366, 121, qnull(QDATE)]), qtype=QDATE_LIST),
                                                       qlist(array_to_raw_qtemporal(np.array([np.datetime64('2001-01-01', 'D'), np.datetime64('2000-05-01', 'D'), np.datetime64('NaT', 'D')]), qtype = QDATE_LIST), qtype = QDATE_LIST),
                                                       qlist([366, 121, qnull(QDATE)], qtype=QDATE_LIST),
                                                       qlist(np.array([np.datetime64('2001-01-01'), np.datetime64('2000-05-01'), np.datetime64('NaT')], dtype='datetime64[D]'), qtype=QDATE_LIST),
                                                       np.array([np.datetime64('2001-01-01'), np.datetime64('2000-05-01'), np.datetime64('NaT')], dtype='datetime64[D]'),
                                                       )),
    (b'2001.01.01',                                    (qtemporal(np.datetime64('2001-01-01', 'D'), qtype=QDATE),
                                                       np.datetime64('2001-01-01', 'D'))),
    (b'0Nd',                                           (qtemporal(qnull(QDATE), qtype=QDATE),
                                                       qtemporal(np.datetime64('NaT', 'D'), qtype=QDATE),
                                                       np.datetime64('NaT', 'D'))),
    (b'2000.01.04T05:36:57.600 0Nz',                   (qlist(np.array([3.234, qnull(QDATETIME)]), qtype=QDATETIME_LIST),
                                                       qlist(array_to_raw_qtemporal(np.array([np.datetime64('2000-01-04T05:36:57.600Z', 'ms'), np.datetime64('nat', 'ms')]), qtype=QDATETIME_LIST), qtype=QDATETIME_LIST),
                                                       qlist([3.234, qnull(QDATETIME)], qtype=QDATETIME_LIST),
                                                       qlist(np.array([np.datetime64('2000-01-04T05:36:57.600Z', 'ms'), np.datetime64('nat', 'ms')]), qtype = QDATETIME_LIST),
                                                       np.array([np.datetime64('2000-01-04T05:36:57.600Z', 'ms'), np.datetime64('nat', 'ms')])
                                                       )),
    (b'2000.01.04T05:36:57.600',                       (qtemporal(np.datetime64('2000-01-04T05:36:57.600Z', 'ms'), qtype=QDATETIME),
                                                       np.datetime64('2000-01-04T05:36:57.600Z', 'ms'))),
    (b'0Nz',                                           (qtemporal(qnull(QDATETIME), qtype=QDATETIME),
                                                       qtemporal(np.datetime64('NaT', 'ms'), qtype=QDATETIME),
                                                       np.datetime64('NaT', 'ms'))),
    (b'12:01 0Nu',                                     (qlist(np.array([721, qnull(QMINUTE)]), qtype=QMINUTE_LIST),
                                                       qlist(array_to_raw_qtemporal(np.array([np.timedelta64(721, 'm'), np.timedelta64('nat', 'm')]), qtype=QMINUTE_LIST), qtype=QMINUTE_LIST),
                                                       qlist([721, qnull(QMINUTE)], qtype=QMINUTE_LIST),
                                                       qlist(np.array([np.timedelta64(721, 'm'), np.timedelta64('nat', 'm')]), qtype = QMINUTE),
                                                       np.array([np.timedelta64(721, 'm'), np.timedelta64('nat', 'm')]),
                                                       )),
    (b'12:01',                                         (qtemporal(np.timedelta64(721, 'm'), qtype=QMINUTE),
                                                       np.timedelta64(721, 'm'))),
    (b'0Nu',                                           (qtemporal(qnull(QMINUTE), qtype=QMINUTE),
                                                       qtemporal(np.timedelta64('NaT', 'm'), qtype=QMINUTE),
                                                       np.timedelta64('NaT', 'm'))),
    (b'12:05:00 0Nv',                                  (qlist(np.array([43500, qnull(QSECOND)]), qtype=QSECOND_LIST),
                                                       qlist(array_to_raw_qtemporal(np.array([np.timedelta64(43500, 's'), np.timedelta64('nat', 's')]), qtype=QSECOND_LIST), qtype=QSECOND_LIST),
                                                       qlist([43500, qnull(QSECOND)], qtype=QSECOND_LIST),
                                                       qlist(np.array([np.timedelta64(43500, 's'), np.timedelta64('nat', 's')]), qtype = QSECOND),
                                                       np.array([np.timedelta64(43500, 's'), np.timedelta64('nat', 's')])
                                                       )),
    (b'12:05:00',                                      (qtemporal(np.timedelta64(43500, 's'), qtype=QSECOND),
                                                       np.timedelta64(43500, 's'))),
    (b'0Nv',                                           (qtemporal(qnull(QSECOND), qtype=QSECOND),
                                                       qtemporal(np.timedelta64('nat', 's'), qtype=QSECOND),
                                                       np.timedelta64('nat', 's'))),
    (b'12:04:59.123 0Nt',                              (qlist(np.array([43499123, qnull(QTIME)]), qtype=QTIME_LIST),
                                                       qlist([43499123, qnull(QTIME)], qtype=QTIME_LIST),
                                                       qlist(np.array([np.timedelta64(43499123, 'ms'), np.timedelta64('nat', 'ms')]), qtype = QTIME_LIST),
                                                       np.array([np.timedelta64(43499123, 'ms'), np.timedelta64('nat', 'ms')])
                                                       )),
    (b'12:04:59.123',                                  (qtemporal(np.timedelta64(43499123, 'ms'), qtype=QTIME),
                                                       np.timedelta64(43499123, 'ms'))),
    (b'0Nt',                                           (qtemporal(qnull(QTIME), qtype=QTIME),
                                                       qtemporal(np.timedelta64('NaT', 'ms'), qtype=QTIME),
                                                       np.timedelta64('NaT', 'ms'))),
    (b'2000.01.04D05:36:57.600 0Np',                   (qlist(np.array([long(279417600000000), qnull(QTIMESTAMP)]), qtype=QTIMESTAMP_LIST),
                                                       qlist(array_to_raw_qtemporal(np.array([np.datetime64('2000-01-04T05:36:57.600Z', 'ns'), np.datetime64('nat', 'ns')]), qtype=QTIMESTAMP_LIST), qtype=QTIMESTAMP_LIST),
                                                       qlist([long(279417600000000), qnull(QTIMESTAMP)], qtype=QTIMESTAMP_LIST),
                                                       qlist(np.array([np.datetime64('2000-01-04T05:36:57.600Z', 'ns'), np.datetime64('nat', 'ns')]), qtype = QTIMESTAMP_LIST),
                                                       np.array([np.datetime64('2000-01-04T05:36:57.600Z', 'ns'), np.datetime64('nat', 'ns')])
                                                       )),
    (b'2000.01.04D05:36:57.600',                       (qtemporal(np.datetime64('2000-01-04T05:36:57.600Z', 'ns'), qtype=QTIMESTAMP),
                                                       np.datetime64('2000-01-04T05:36:57.600Z', 'ns'))),
    (b'0Np',                                           (qtemporal(qnull(QTIMESTAMP), qtype=QTIMESTAMP),
                                                       qtemporal(np.datetime64('NaT', 'ns'), qtype=QTIMESTAMP),
                                                       np.datetime64('NaT', 'ns'))),
    (b'0D05:36:57.600 0Nn',                            (qlist(np.array([long(20217600000000), qnull(QTIMESPAN)]), qtype=QTIMESPAN_LIST),
                                                       qlist(array_to_raw_qtemporal(np.array([np.timedelta64(20217600000000, 'ns'), np.timedelta64('nat', 'ns')]), qtype=QTIMESPAN_LIST), qtype=QTIMESPAN_LIST),
                                                       qlist([long(20217600000000), qnull(QTIMESPAN)], qtype=QTIMESPAN_LIST),
                                                       qlist(np.array([np.timedelta64(20217600000000, 'ns'), np.timedelta64('nat', 'ns')]), qtype = QTIMESPAN_LIST),
                                                       np.array([np.timedelta64(20217600000000, 'ns'), np.timedelta64('nat', 'ns')])
                                                       )),
    (b'0D05:36:57.600',                                (qtemporal(np.timedelta64(20217600000000, 'ns'), qtype=QTIMESPAN),
                                                       np.timedelta64(20217600000000, 'ns'))),
    (b'0Nn',                                           (qtemporal(qnull(QTIMESPAN), qtype=QTIMESPAN),
                                                       qtemporal(np.timedelta64('NaT', 'ns'), qtype=QTIMESPAN),
                                                       np.timedelta64('NaT', 'ns'))),

    (b'::',                                            None),
    (b'1+`',                                           QException('type')),
    (b'1',                                             np.int64(1)),
    (b'1i',                                            np.int32(1)),
    (b'-234h',                                         np.int16(-234)),
    (b'0b',                                            np.bool_(False)),
    (b'1b',                                            np.bool_(True)),
    (b'0x2a',                                          np.byte(0x2a)),
    (b'89421099511627575j',                            np.int64(long(89421099511627575))),
    (b'5.5e',                                          np.float32(5.5)),
    (b'3.234',                                         np.float64(3.234)),
    (b'"0"',                                           '0'),
    (b'"abc"',                                         ('abc',
                                                       np.array(list('abc'), dtype='S'))),
    (b'"quick brown fox jumps over a lazy dog"',       'quick brown fox jumps over a lazy dog'),
    (b'`abc',                                          np.string_('abc')),
    (b'`quickbrownfoxjumpsoveralazydog',               np.string_('quickbrownfoxjumpsoveralazydog')),
    (b'0Nh',                                           qnull(QSHORT)),
    (b'0N',                                            qnull(QLONG)),
    (b'0Ni',                                           qnull(QINT)),
    (b'0Nj',                                           qnull(QLONG)),
    (b'0Ne',                                           qnull(QFLOAT)),
    (b'0n',                                            qnull(QDOUBLE)),
    (b'" "',                                           qnull(QSTRING)),
    (b'`',                                             qnull(QSYMBOL)),
    (b'0Ng',                                           qnull(QGUID)),
    (b'()',                                            []),
    (b'(0b;1b;0b)',                                    (np.array([False, True, False], dtype=np.bool_),
                                                       qlist(np.array([False, True, False]), qtype = QBOOL_LIST),
                                                       qlist([False, True, False], qtype = QBOOL_LIST))),
    (b'(0x01;0x02;0xff)',                              (np.array([0x01, 0x02, 0xff], dtype=np.byte),
                                                       qlist(np.array([0x01, 0x02, 0xff], dtype=np.byte), qtype = QBYTE_LIST),
                                                       qlist(np.array([0x01, 0x02, 0xff]), qtype = QBYTE_LIST),
                                                       qlist([0x01, 0x02, 0xff], qtype = QBYTE_LIST))),
    (b'(1h;2h;3h)',                                    (np.array([1, 2, 3], dtype=np.int16),
                                                       qlist(np.array([1, 2, 3], dtype=np.int16), qtype = QSHORT_LIST),
                                                       qlist(np.array([1, 2, 3]), qtype = QSHORT_LIST),
                                                       qlist([1, 2, 3], qtype = QSHORT_LIST))),
    (b'(1h;0Nh;3h)',                                   qlist(np.array([1, qnull(QSHORT), 3], dtype=np.int16), qtype=QSHORT_LIST)),
    (b'1 2 3',                                         (np.array([1, 2, 3], dtype=np.int64),
                                                       qlist(np.array([1, 2, 3], dtype=np.int64), qtype = QLONG_LIST),
                                                       qlist(np.array([1, 2, 3]), qtype = QLONG_LIST),
                                                       qlist([1, 2, 3], qtype = QLONG_LIST))),
    (b'1 0N 3',                                        qlist(np.array([1, qnull(QLONG), 3], dtype=np.int64), qtype=QLONG_LIST)),
    (b'(1i;2i;3i)',                                    (np.array([1, 2, 3], dtype=np.int32),
                                                       qlist(np.array([1, 2, 3], dtype=np.int32), qtype = QINT_LIST),
                                                       qlist(np.array([1, 2, 3]), qtype = QINT_LIST),
                                                       qlist([1, 2, 3], qtype = QINT_LIST))),
    (b'(1i;0Ni;3i)',                                   qlist(np.array([1, qnull(QINT), 3], dtype=np.int32), qtype=QINT_LIST)),
    (b'(1j;2j;3j)',                                    (np.array([1, 2, 3], dtype=np.int64),
                                                       qlist(np.array([1, 2, 3], dtype=np.int64), qtype = QLONG_LIST),
                                                       qlist(np.array([1, 2, 3]), qtype = QLONG_LIST),
                                                       qlist([1, 2, 3], qtype = QLONG_LIST))),
    (b'(1j;0Nj;3j)',                                   qlist(np.array([1, qnull(QLONG), 3], dtype=np.int64), qtype=QLONG_LIST)),
    (b'(5.5e; 8.5e)',                                  (np.array([5.5, 8.5], dtype=np.float32),
                                                       qlist(np.array([5.5, 8.5], dtype=np.float32), qtype = QFLOAT_LIST),
                                                       qlist(np.array([5.5, 8.5]), qtype = QFLOAT_LIST),
                                                       qlist([5.5, 8.5], qtype = QFLOAT_LIST))),
    (b'(5.5e; 0Ne)',                                   qlist(np.array([5.5, qnull(QFLOAT)], dtype=np.float32), qtype=QFLOAT_LIST)),
    (b'3.23 6.46',                                     (np.array([3.23, 6.46], dtype=np.float64),
                                                       qlist(np.array([3.23, 6.46], dtype=np.float64), qtype = QDOUBLE_LIST),
                                                       qlist(np.array([3.23, 6.46]), qtype = QDOUBLE_LIST),
                                                       qlist([3.23, 6.46], qtype = QDOUBLE_LIST))),
    (b'3.23 0n',                                       qlist(np.array([3.23, qnull(QDOUBLE)], dtype=np.float64), qtype=QDOUBLE_LIST)),
    (b'(1;`bcd;"0bc";5.5e)',                           [np.int64(1), np.string_('bcd'), '0bc', np.float32(5.5)]),
    (b'(42;::;`foo)',                                  [np.int64(42), None, np.string_('foo')]),
    (b'(1;2h;3.234;"4")',                              [np.int64(1), np.int16(2), np.float64(3.234), '4']),
    (b'(`one;2 3;"456";(7;8 9))',                      [np.string_('one'), qlist(np.array([2, 3], dtype=np.int64), qtype=QLONG_LIST), '456', [np.int64(7), qlist(np.array([8, 9], dtype=np.int64), qtype=QLONG_LIST)]]),

    (b'`jumps`over`a`lazy`dog',                        (np.array(['jumps', 'over', 'a', 'lazy', 'dog'], dtype=np.string_),
                                                       qlist(np.array(['jumps', 'over', 'a', 'lazy', 'dog']), qtype = QSYMBOL_LIST),
                                                       qlist(['jumps', 'over', 'a', 'lazy', 'dog'], qtype = QSYMBOL_LIST))),
    (b'`the`quick`brown`fox',                          np.array([np.string_('the'), np.string_('quick'), np.string_('brown'), np.string_('fox')], dtype=np.object)),
    (b'``quick``fox',                                  qlist(np.array([qnull(QSYMBOL), np.string_('quick'), qnull(QSYMBOL), np.string_('fox')], dtype=np.object), qtype=QSYMBOL_LIST)),
    (b'``',                                            qlist(np.array([qnull(QSYMBOL), qnull(QSYMBOL)], dtype=np.object), qtype=QSYMBOL_LIST)),
    (b'("quick"; "brown"; "fox"; "jumps"; "over"; "a lazy"; "dog")',
                                                      (['quick', 'brown', 'fox', 'jumps', 'over', 'a lazy', 'dog'],
                                                       qlist(np.array(['quick', 'brown', 'fox', 'jumps', 'over', 'a lazy', 'dog']), qtype = QSTRING_LIST),
                                                       qlist(['quick', 'brown', 'fox', 'jumps', 'over', 'a lazy', 'dog'], qtype = QSTRING_LIST))),
    (b'{x+y}',                                         QLambda('{x+y}')),
    (b'{x+y}[3]',                                      QProjection([QLambda('{x+y}'), np.int64(3)])),

    (b'(enlist `a)!(enlist 1)',                        (QDictionary(qlist(np.array(['a']), qtype = QSYMBOL_LIST),
                                                                   qlist(np.array([1], dtype=np.int64), qtype=QLONG_LIST)),
                                                       QDictionary(qlist(np.array(['a']), qtype = QSYMBOL_LIST),
                                                                   qlist(np.array([1]), qtype=QLONG_LIST)))),
    (b'1 2!`abc`cdefgh',                               QDictionary(qlist(np.array([1, 2], dtype=np.int64), qtype=QLONG_LIST),
                                                                  qlist(np.array(['abc', 'cdefgh']), qtype = QSYMBOL_LIST))),
    (b'`abc`def`gh!([] one: 1 2 3; two: 4 5 6)',       QDictionary(qlist(np.array(['abc', 'def', 'gh']), qtype = QSYMBOL_LIST),
                                                                  qtable(qlist(np.array(['one', 'two']), qtype = QSYMBOL_LIST),
                                                                         [qlist(np.array([1, 2, 3]), qtype = QLONG_LIST),
                                                                          qlist(np.array([4, 5, 6]), qtype = QLONG_LIST)]))),
    (b'(`x`y!(`a;2))',                                 QDictionary(qlist(np.array(['x', 'y']), qtype = QSYMBOL_LIST),
                                                                  [np.string_('a'), np.int64(2)])),
    (b'(0 1; 2 3)!`first`second',                      QDictionary([qlist(np.array([0, 1], dtype=np.int64), qtype=QLONG_LIST), qlist(np.array([2, 3], dtype=np.int64), qtype=QLONG_LIST)],
                                                                   qlist(np.array(['first', 'second']), qtype = QSYMBOL_LIST))),
    (b'(1;2h;3.234;"4")!(`one;2 3;"456";(7;8 9))',     QDictionary([np.int64(1), np.int16(2), np.float64(3.234), '4'],
                                                                  [np.string_('one'), qlist(np.array([2, 3], dtype=np.int64), qtype=QLONG_LIST), '456', [np.int64(7), qlist(np.array([8, 9], dtype=np.int64), qtype=QLONG_LIST)]])),
    (b'`A`B`C!((1;3.234;3);(`x`y!(`a;2));5.5e)',       QDictionary(qlist(np.array(['A', 'B', 'C']), qtype = QSYMBOL_LIST),
                                                                  [[np.int64(1), np.float64(3.234), np.int64(3)], QDictionary(qlist(np.array(['x', 'y']), qtype = QSYMBOL_LIST), [np.string_('a'), np.int64(2)]), np.float32(5.5)])),

    (b'flip `abc`def!(1 2 3; 4 5 6)',                  (qtable(qlist(np.array(['abc', 'def']), qtype = QSYMBOL_LIST),
                                                             [qlist(np.array([1, 2, 3], dtype=np.int64), qtype=QLONG_LIST),
                                                              qlist(np.array([4, 5, 6], dtype=np.int64), qtype=QLONG_LIST)],
                                                             qtype=QTABLE),
                                                       qtable(qlist(np.array(['abc', 'def']), qtype = QSYMBOL_LIST),
                                                              [qlist(np.array([1, 2, 3]), qtype = QLONG_LIST),
                                                               qlist(np.array([4, 5, 6]), qtype = QLONG_LIST)]),
                                                       qtable(qlist(['abc', 'def'], qtype = QSYMBOL_LIST),
                                                              [qlist([1, 2, 3], qtype = QLONG_LIST),
                                                               qlist([4, 5, 6], qtype = QLONG_LIST)]),
                                                       qtable(qlist(['abc', 'def'], qtype = QSYMBOL_LIST),
                                                              [qlist([1, 2, 3]), qlist([4, 5, 6])],
                                                              **{'abc': QLONG_LIST, 'def': QLONG_LIST}),
                                                       qtable(['abc', 'def'],
                                                              [[1, 2, 3], [4, 5, 6]],
                                                              **{'abc': QLONG, 'def': QLONG}))),
    (b'flip `name`iq!(`Dent`Beeblebrox`Prefect;98 42 126)',
                                       (qtable(qlist(np.array(['name', 'iq']), qtype = QSYMBOL_LIST),
                                              [qlist(np.array(['Dent', 'Beeblebrox', 'Prefect']), qtype = QSYMBOL_LIST),
                                               qlist(np.array([98, 42, 126], dtype=np.int64), qtype = QLONG_LIST)]),
                                        qtable(qlist(np.array(['name', 'iq']), qtype = QSYMBOL_LIST),
                                               [qlist(np.array(['Dent', 'Beeblebrox', 'Prefect']), qtype = QSYMBOL_LIST),
                                                qlist(np.array([98, 42, 126]), qtype = QLONG_LIST)]),
                                        qtable(qlist(['name', 'iq'], qtype = QSYMBOL_LIST),
                                               [qlist(['Dent', 'Beeblebrox', 'Prefect'], qtype = QSYMBOL_LIST),
                                                qlist([98, 42, 126], qtype = QLONG_LIST)]),
                                        qtable(qlist(['name', 'iq'], qtype = QSYMBOL_LIST),
                                               [qlist(['Dent', 'Beeblebrox', 'Prefect']),
                                                qlist([98, 42, 126])],
                                               name = QSYMBOL, iq = QLONG),
                                        qtable(['name', 'iq'],
                                                              [['Dent', 'Beeblebrox', 'Prefect'],
                                                               [98, 42, 126]],
                                                              name = QSYMBOL, iq = QLONG),
                                                       qtable(['name', 'iq'],
                                                              [['Dent', 'Beeblebrox', 'Prefect'],
                                                               [98, 42, 126]],
                                                              **{'name': QSYMBOL, 'iq': QLONG}))),
    (b'flip `name`iq`grade!(`Dent`Beeblebrox`Prefect;98 42 126;"a c")',
                                                       qtable(qlist(np.array(['name', 'iq', 'grade']), qtype = QSYMBOL_LIST),
                                                              [qlist(np.array(['Dent', 'Beeblebrox', 'Prefect']), qtype = QSYMBOL_LIST),
                                                               qlist(np.array([98, 42, 126]), qtype = QLONG_LIST),
                                                               "a c"])),
    (b'flip `name`iq`fullname!(`Dent`Beeblebrox`Prefect;98 42 126;("Arthur Dent"; "Zaphod Beeblebrox"; "Ford Prefect"))',
                                                        qtable(qlist(np.array(['name', 'iq', 'fullname']), qtype = QSYMBOL_LIST),
                                                               [qlist(np.array(['Dent', 'Beeblebrox', 'Prefect']), qtype = QSYMBOL_LIST),
                                                                qlist(np.array([98, 42, 126]), qtype = QLONG_LIST),
                                                                qlist(np.array(["Arthur Dent", "Zaphod Beeblebrox", "Ford Prefect"]), qtype = QSTRING_LIST)])),
    (b'flip `name`iq`misc!(`Dent`Beeblebrox`Prefect;98 42 126;("The Hitch Hiker\'s Guide to the Galaxy"; 160; 1979.10.12))',
                                                        qtable(qlist(np.array(['name', 'iq', 'misc']), qtype = QSYMBOL_LIST),
                                                               [qlist(np.array(['Dent', 'Beeblebrox', 'Prefect']), qtype = QSYMBOL_LIST),
                                                                qlist(np.array([98, 42, 126]), qtype = QLONG_LIST),
                                                                qlist(np.array(["The Hitch Hiker\'s Guide to the Galaxy", long(160), qtemporal(np.datetime64('1979-10-12', 'D'), qtype=QDATE)]), qtype = QGENERAL_LIST)])),
    (b'([] sc:1 2 3; nsc:(1 2; 3 4; 5 6 7))',          (qtable(qlist(np.array(['sc', 'nsc']), qtype = QSYMBOL_LIST),
                                                             [qlist(np.array([1, 2, 3], dtype=np.int64), qtype = QLONG_LIST),
                                                              [qlist(np.array([1, 2], dtype=np.int64), qtype = QLONG_LIST),
                                                               qlist(np.array([3, 4], dtype=np.int64), qtype = QLONG_LIST),
                                                               qlist(np.array([5, 6, 7], dtype=np.int64), qtype = QLONG_LIST)]]),
                                                       qtable(qlist(np.array(['sc', 'nsc']), qtype = QSYMBOL_LIST),
                                                              [qlist(np.array([1, 2, 3]), qtype = QLONG_LIST),
                                                               [qlist(np.array([1, 2]), qtype = QLONG_LIST),
                                                                qlist(np.array([3, 4]), qtype = QLONG_LIST),
                                                                qlist(np.array([5, 6, 7]), qtype = QLONG_LIST)]]),
                                                       qtable(qlist(['sc', 'nsc'], qtype = QSYMBOL_LIST),
                                                              [qlist([1, 2, 3], qtype = QLONG_LIST),
                                                               [qlist([1, 2], qtype = QLONG_LIST),
                                                                qlist([3, 4], qtype = QLONG_LIST),
                                                                qlist([5, 6, 7], qtype = QLONG_LIST)]]))),
    (b'([] sc:1 2 3; nsc:(1 2; 3 4; 5 6))',            qtable(qlist(np.array(['sc', 'nsc']), qtype = QSYMBOL_LIST),
                                                              [qlist(np.array([1, 2, 3]), qtype = QLONG_LIST),
                                                               [qlist(np.array([1, 2]), qtype = QLONG_LIST),
                                                                qlist(np.array([3, 4]), qtype = QLONG_LIST),
                                                                qlist(np.array([5, 6]), qtype = QLONG_LIST)]])),
    (b'1#([] sym:`x`x`x;str:"  a")',                   {'data': qtable(qlist(np.array(['sym', 'str']), qtype = QSYMBOL_LIST),
                                                                      [qlist(np.array(['x'], dtype=np.string_), qtype = QSYMBOL_LIST),
                                                                       b" "]),
                                                        'single_char_strings': True
                                                        }),
    (b'-1#([] sym:`x`x`x;str:"  a")',                  {'data': qtable(qlist(np.array(['sym', 'str']), qtype = QSYMBOL_LIST),
                                                                      [qlist(np.array(['x'], dtype=np.string_), qtype = QSYMBOL_LIST),
                                                                       b"a"]),
                                                        'single_char_strings': True
                                                        }),
    (b'2#([] sym:`x`x`x`x;str:"  aa")',                qtable(qlist(np.array(['sym', 'str']), qtype = QSYMBOL_LIST),
                                                             [qlist(np.array(['x', 'x'], dtype=np.string_), qtype = QSYMBOL_LIST),
                                                              b"  "])),
    (b'-2#([] sym:`x`x`x`x;str:"  aa")',               qtable(qlist(np.array(['sym', 'str']), qtype = QSYMBOL_LIST),
                                                             [qlist(np.array(['x', 'x'], dtype=np.string_), qtype = QSYMBOL_LIST),
                                                              b"aa"])),
    (b'([] name:`symbol$(); iq:`int$())',              (qtable(qlist(np.array(['name', 'iq']), qtype = QSYMBOL_LIST),
                                                             [qlist(np.array([], dtype=np.string_), qtype = QSYMBOL_LIST),
                                                              qlist(np.array([], dtype=np.int32), qtype = QINT_LIST)]),
                                                       qtable(qlist(np.array(['name', 'iq']), qtype = QSYMBOL_LIST),
                                                             [qlist(np.array([]), qtype = QSYMBOL_LIST),
                                                              qlist(np.array([]), qtype = QINT_LIST)]),
                                                       qtable(qlist(['name', 'iq'], qtype = QSYMBOL_LIST),
                                                             [qlist([], qtype = QSYMBOL_LIST),
                                                              qlist([], qtype = QINT_LIST)]))),
    (b'([] pos:`d1`d2`d3;dates:(2001.01.01;2000.05.01;0Nd))',
                                                      (qtable(qlist(np.array(['pos', 'dates']), qtype = QSYMBOL_LIST),
                                                             [qlist(np.array(['d1', 'd2', 'd3']), qtype = QSYMBOL_LIST),
                                                              qlist(np.array([366, 121, qnull(QDATE)]), qtype=QDATE_LIST)]),
                                                       qtable(['pos', 'dates'],
                                                             [qlist(np.array(['d1', 'd2', 'd3']), qtype = QSYMBOL_LIST),
                                                              np.array([np.datetime64('2001-01-01'), np.datetime64('2000-05-01'), np.datetime64('NaT')], dtype='datetime64[D]')])
                                                       )),
    (b'([eid:1001 1002 1003] pos:`d1`d2`d3;dates:(2001.01.01;2000.05.01;0Nd))',
                                                       QKeyedTable(qtable(qlist(np.array(['eid']), qtype = QSYMBOL_LIST),
                                                                          [qlist(np.array([1001, 1002, 1003]), qtype = QLONG_LIST)]),
                                                                   qtable(qlist(np.array(['pos', 'dates']), qtype = QSYMBOL_LIST),
                                                                          [qlist(np.array(['d1', 'd2', 'd3']), qtype = QSYMBOL_LIST),
                                                                           qlist(np.array([366, 121, qnull(QDATE)]), qtype = QDATE_LIST)]))
                                                       ),
))



def init():
    with open('tests/QExpressions3.out', 'rb') as f:
        while True:
            query = f.readline().strip()
            binary = f.readline().strip()

            if not binary:
                break

            BINARY[query] = binary



def test_writing():
    w = qwriter.QWriter(None, 3)

    for query, value in iter(EXPRESSIONS.items()):
        sys.stdout.write( '%-75s' % query )
        if isinstance(value, tuple):
            for obj in value:
                sys.stdout.write( '.' )
                serialized = binascii.hexlify(w.write(obj, 1))[16:].lower()
                assert serialized == BINARY[query].lower(), 'serialization failed: %s, expected: %s actual: %s' % (query,  BINARY[query].lower(), serialized)
        elif isinstance(value, dict):
            sys.stdout.write( '.' )
            single_char_strings = value['single_char_strings'] if 'single_char_strings' in value else False
            serialized = binascii.hexlify(w.write(value['data'], 1, single_char_strings = single_char_strings))[16:].lower()
            assert serialized == BINARY[query].lower(), 'serialization failed: %s, expected: %s actual: %s' % (query,  BINARY[query].lower(), serialized)
        else:
            sys.stdout.write( '.' )
            serialized = binascii.hexlify(w.write(value, 1))[16:].lower()
            assert serialized == BINARY[query].lower(), 'serialization failed: %s, expected: %s actual: %s' % (query,  BINARY[query].lower(), serialized)

        print('')

def test_write_single_char_string():
    w = qwriter.QWriter(None, 3)

    for obj in (['one', 'two', '3'], qlist(['one', 'two', '3'], qtype = QSTRING_LIST)):
        single_char_strings = False
        for query in (b'("one"; "two"; "3")', b'("one"; "two"; enlist "3")'):
            serialized = binascii.hexlify(w.write(obj, 1, single_char_strings = single_char_strings ))[16:].lower()
            assert serialized == BINARY[query].lower(), 'serialization failed: %s, expected: %s actual: %s' % (query,  BINARY[query].lower(), serialized)
            single_char_strings = not single_char_strings


init()
test_writing()
test_write_single_char_string()
