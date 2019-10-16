from collections import OrderedDict
from datetime import datetime

import pytz

import kobuddy
from kobuddy import Highlight, Book, Books

TEST_BOOK = Book(title='test title', author='test author', content_id='fwfwf', isbn='2424')

def test_hl_no_datecreated():
    row = OrderedDict([
        ('BookmarkID', 'bbbbb'),
        ('VolumeID', 'vvvv'),
        ('ContentID', 'cccc'),
        ('StartContainerPath', 'span#kobo\\.31\\.4'),
        ('StartContainerChildIndex', -99),
        ('StartOffset', 117),
        ('EndContainerPath', 'span#kobo\\.31\\.5'),
        ('EndContainerChildIndex', -99),
        ('EndOffset', 141),
        ('Text', '<blah blah quote>'),
        ('Annotation', None),
        ('ExtraAnnotationData', None),
        ('DateCreated', None),
        ('ChapterProgress', 0.75),
        ('Hidden', 'false'),
        ('Version', ''),
        ('DateModified', '2014-05-17T21:05:35Z'),
        ('Creator', None),
        ('UUID', None),
        ('UserID', '6fc7'),
        ('SyncTime', '2019-05-21T16:46:17Z'),
        ('Published', 'false'),
    ])
    hl = Highlight(row, TEST_BOOK)
    # TODO can we automate this?
    for attr in [a for a in dir(Highlight) if not a.startswith('_')]:
        value = getattr(hl, attr)
        assert value is not None


def test_iter_events_aux_Event():
    from kobuddy import _iter_events_aux_Event
    books = Books()
    books.add(TEST_BOOK)

    row = OrderedDict([
        ('EventType', 3),
        ('EventCount', 35),
        ('LastOccurrence', '2019-01-22T23:07:47.000'),
        ('ContentID', 'fwfwf'),
        ('Checksum', 'bd0fda782920dbaa57d593fa70bcf3de'),
        ('hex(ExtraData)', '000000010000001E006500760065006E007400540069006D0065007300740061006D0070007300000009000000002300000003005C17566E00000003005C175B2400000003005C175D0C00000003005C175E1F00000003005C1967C300000003005C196FE800000003005C20EA0300000003005C20EE4100000003005C20F5C100000003005C22684300000003005C27F06A00000003005C27F92300000003005C28C9C300000003005C28CC6B00000003005C291EE500000003005C2E27FF00000003005C2F75B100000003005C31B2FE00000003005C3758DD00000003005C389B4800000003005C38E45600000003005C3C9E9300000003005C3F31FB00000003005C40BB7200000003005C419BA300000003005C419BE400000003005C419C1800000003005C44555F00000003005C460FA100000003005C460FD500000003005C47A15000000003005C47A16500000003005C47A18800000003005C47A19500000003005C47A243'),
    ])
    res = list(_iter_events_aux_Event(row=row, books=books))
    assert len(res) == 35
    assert res[0].dt  == datetime(year=2018, month=12, day=17, hour=7 , minute=55, second=26, tzinfo=pytz.utc)
    assert res[-1].dt == datetime(year=2019, month=1 , day=22, hour=23, minute=7 , second=47, tzinfo=pytz.utc)
