import pytest
import requests
import logging

import album
from settings import (MOCK_ALBUM_ID, INPUT_WARNING_MESSAGE,
                     SERVER_ERROR_MESSAGE, URL, MOCK_JSON, MOCK_OUTPUT)

def test_validate_input_non_numeric_value(monkeypatch, caplog):
    monkeypatch.setattr("builtins.input", lambda x: 'asdfa')
    assert album.validate_input() == -1
    assert caplog.record_tuples == [("root", logging.WARNING,
                                    INPUT_WARNING_MESSAGE)]


def test_validate_input_negative_integer_value(monkeypatch, caplog):
    monkeypatch.setattr("builtins.input", lambda x: '-1')
    assert album.validate_input() == -1
    assert caplog.record_tuples == [("root", logging.WARNING,
                                    INPUT_WARNING_MESSAGE)]


def test_validate_input_non_integer_value(monkeypatch, caplog):
    monkeypatch.setattr("builtins.input", lambda x: '1.5')
    assert album.validate_input() == -1
    assert caplog.record_tuples == [("root", logging.WARNING,
                                    INPUT_WARNING_MESSAGE)]


def test_validate_input_less_than_one(monkeypatch, caplog):
    monkeypatch.setattr("builtins.input", lambda x: '0')
    assert album.validate_input() == -1
    assert caplog.record_tuples == [("root", logging.WARNING,
                                    INPUT_WARNING_MESSAGE)]


def test_validate_input_equal_to_one(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda x: '1')
    assert album.validate_input() == 1

def test_validate_input_greater_than_one(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda x: '2')
    assert album.validate_input() == 2


def test_validate_input_between_one_and_one_hundred(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda x: '46')
    assert album.validate_input() == 46


def test_validate_input_less_than_one_hundred(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda x: '99')
    assert album.validate_input() == 99


def test_validate_input_equal_to_one_hundred(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda x: '100')
    assert album.validate_input() == 100


def test_validate_input_greater_than_one_hundred(monkeypatch, caplog):
    monkeypatch.setattr("builtins.input", lambda x: '101')
    assert album.validate_input() == -1
    assert caplog.record_tuples == [("root", logging.WARNING,
                                    INPUT_WARNING_MESSAGE)]


def test_main_server_unexpected_behavior(monkeypatch, requests_mock, caplog):
    monkeypatch.setattr("album.validate_input", lambda: MOCK_ALBUM_ID)
    requests_mock.get(URL.format(MOCK_ALBUM_ID), json=[])
    with pytest.raises(RuntimeError, match=SERVER_ERROR_MESSAGE):
        album.main()
    assert caplog.record_tuples == [("root", logging.ERROR,
                                    SERVER_ERROR_MESSAGE)]


def test_main_expected_behavior(monkeypatch, requests_mock, capsys):
    monkeypatch.setattr("album.validate_input", lambda: MOCK_ALBUM_ID)
    requests_mock.get(URL.format(MOCK_ALBUM_ID), json=MOCK_JSON)
    album.main()
    captured = capsys.readouterr()
    assert captured.out == MOCK_OUTPUT


def test_main_expected_behavior_with_loop(monkeypatch, requests_mock, capsys):
    inputs = [-1, MOCK_ALBUM_ID]
    monkeypatch.setattr("album.validate_input", lambda: inputs.pop(0))
    requests_mock.get(URL.format(MOCK_ALBUM_ID), json=MOCK_JSON)
    album.main()
    captured = capsys.readouterr()
    assert captured.out == MOCK_OUTPUT
