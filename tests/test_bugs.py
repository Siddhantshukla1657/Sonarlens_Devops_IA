import pytest

from app.bugs import average_score, get_item, normalize_titles, print_value


def test_average_score_zero_division():
    # Intentionally seeded ZeroDivisionError when count is zero (S3518)
    with pytest.raises(ZeroDivisionError):
        average_score(10, 0)


def test_get_item_respects_bounds():
    # Valid index returns task
    assert get_item(["a", "b"], 1) == "b"
    # Out of bounds index raises IndexError
    with pytest.raises(IndexError):
        get_item(["a", "b"], 2)


def test_normalize_titles_demonstrates_ignored_return():
    # S2201: sorted() without assignment does not mutate titles in place
    titles = ["b", "a", "c"]
    result = normalize_titles(titles)
    assert result == ["b", "a", "c"]


def test_print_value_handles_valid_string(capsys):
    print_value("hello")
    captured = capsys.readouterr()
    assert "HELLO" in captured.out


def test_print_value_null_dereference():
    # S2259: None causes value.upper() to fail with AttributeError
    with pytest.raises(AttributeError):
        print_value(None)
