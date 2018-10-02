import photo_album
import pytest
import sys
from contextlib import contextmanager
from io import StringIO

@contextmanager
def replace_stdin(target):
    orig = sys.stdin
    sys.stdin = target
    yield
    sys.stdin = orig

def test_CA1():
    with pytest.raises(NameError), replace_stdin(StringIO("123")):
        photo_album.Check_Acceptance()

def test_CA2():
    with pytest.raises(NameError), replace_stdin(StringIO("asdf")):
        photo_album.Check_Acceptance()

def test_CA_3():
    with replace_stdin(StringIO("12")):
        assert photo_album.Check_Acceptance() == 12

def test_FA_1():
    with pytest.raises(Exception):
        photo_album.Fetch_Album(1234)

def test_FA_2():
    assert (photo_album.Fetch_Album(1))[0]['id'] == 1

def test_PA_1():
    json = [{"albumId": 14, "id": 651, "title": "fugiat quos ullam aut ducimus saepe", "url": "https://via.placeholder.com/600/b9173d", "thumbnailUrl": "https://via.placeholder.com/150/b9173d"}, {"albumId": 14, "id": 652, "title": "tempore et sit cum aut", "url": "https://via.placeholder.com/600/a8b15c","thumbnailUrl": "https://via.placeholder.com/150/a8b15c"}]
    a = (photo_album.Parse_Album(json))[0]
    b = [651, 'fugiat quos ullam aut ducimus saepe']
    if not list(set(a) - set(b)):
        assert 1
    else:
        assert 0
