import pytest
from xeger.xeger import Xeger


def test_xeger_instantiation():
    x = Xeger()
    assert isinstance(x, Xeger)


def test_xeger_generate():
    x = Xeger()
    result = x.generate("abcd")
    assert result == "abcd"


def test_xeger_generate_with_check():
    x = Xeger()
    result = x.generate("abcd", check=True)
    assert result == "abcd"


def test_xeger_generate_any_word():
    x = Xeger()
    result = x.generate(r"\w+")
    assert result.isalnum() or result == "_"


def test_xeger_generate_any_word_inverted():
    x = Xeger()
    result = x.generate(r"\W+")
    assert not (result.isalnum() or result == "_")


def test_xeger_generate_any_digit():
    x = Xeger()
    result = x.generate(r"\d+")
    assert result.isdigit()


def test_xeger_generate_any_digit_inverted():
    x = Xeger()
    result = x.generate(r"\D+")
    assert not result.isdigit()


def test_xeger_generate_any_whitespace():
    x = Xeger()
    result = x.generate(r"\s+")
    assert result.isspace()


def test_xeger_generate_any_whitespace_inverted():
    x = Xeger()
    result = x.generate(r"\S+")
    assert not result.isspace()


def test_xeger_generate_any_alnum():
    x = Xeger()
    result = x.generate(r"[[:alnum:]]+")
    assert result.isalnum()


def test_xeger_generate_any_alpha():
    x = Xeger()
    result = x.generate(r"[[:alpha:]]+")
    assert result.isalpha()


def test_xeger_generate_any_ascii():
    x = Xeger()
    result = x.generate(r"[[:ascii:]]+")
    assert all(ord(c) < 128 for c in result)


def test_xeger_generate_any_blank():
    x = Xeger()
    result = x.generate(r"[[:blank:]]+")
    assert result.isspace()


def test_xeger_generate_any_cntrl():
    x = Xeger()
    result = x.generate(r"[[:cntrl:]]+")
    assert all(ord(c) < 32 or ord(c) == 127 for c in result)


def test_xeger_generate_any_graph():
    x = Xeger()
    result = x.generate(r"[[:graph:]]+")
    assert all(c.isprintable() and c != " " for c in result)


def test_xeger_generate_any_lower():
    x = Xeger()
    result = x.generate(r"[[:lower:]]+")
    assert result.islower()


def test_xeger_generate_any_print():
    x = Xeger()
    result = x.generate(r"[[:print:]]+")
    assert all(c.isprintable() for c in result)


def test_xeger_generate_any_punct():
    x = Xeger()
    result = x.generate(r"[[:punct:]]+")
    assert not result.isalnum() and not result.isspace() and result.isprintable()


def test_xeger_generate_any_upper():
    x = Xeger()
    result = x.generate(r"[[:upper:]]+")
    assert result.isupper()


def test_xeger_generate_any_xdigit():
    x = Xeger()
    result = x.generate(r"[[:xdigit:]]+")
    assert all(c in "0123456789abcdefABCDEF" for c in result)


def test_xeger_character_range_lower():
    x = Xeger()
    result = x.generate(r"[a-z]+")
    assert result.islower()


def test_xeger_character_range_upper():
    x = Xeger()
    result = x.generate(r"[A-Z]+")
    assert result.isupper()


def test_xeger_character_range_span():
    x = Xeger()
    result = x.generate(r"[A-z]+", check=True)
    assert all(ord(c) >= 65 and ord(c) <= 122 for c in result)


def test_xeger_character_group_items_multiple():
    x = Xeger()
    result = x.generate(r"[abc]+")
    assert all(c in "abc" for c in result)


def test_xeger_character_group_negative_modifier():
    x = Xeger()
    result = x.generate(r"[^abc]+")
    assert all(c not in "abc" for c in result)


def test_xeger_character_group_negative_range():
    x = Xeger()
    result = x.generate(r"[^a-z]+")
    assert all(ord(c) < 97 or ord(c) > 122 for c in result)


def test_xeger_any_character():
    x = Xeger()
    result = x.generate(r".")
    assert len(result) == 1


def test_xeger_group():
    x = Xeger()
    result = x.generate(r"(abc)+")
    assert result == "abc"


def test_xeger_group_with_range():
    x = Xeger()
    result = x.generate(r"([a-z])+")
    assert result.islower()


def test_xeger_group_with_multiple_items():
    x = Xeger()
    result = x.generate(r"(abc|def)+")
    assert result in ("abc", "def")


def test_xeger_quantifier_range():
    x = Xeger()
    result = x.generate(r"a{2,4}")
    assert result in ("aa", "aaa", "aaaa")


def test_xeger_quantifier_range_single():
    x = Xeger()
    result = x.generate(r"a{2}")
    assert result == "aa"


def test_xeger_quantifier_zero_or_more():
    x = Xeger()
    result = x.generate(r"a*")
    assert result == ""


def test_xeger_quantifier_one_or_more():
    x = Xeger()
    result = x.generate(r"a+")
    assert result == "a"


def test_xeger_quantifier_zero_or_one():
    x = Xeger()
    result = x.generate(r"a?")
    assert result == ""


def test_xeger_many_groups():
    x = Xeger()
    result = x.generate(r"(abc)+def(ghi)+")
    assert result == "abcdefghi"


def test_xeger_many_character_classes():
    x = Xeger()
    result = x.generate(r"[[:word:]][[:digit:]][[:blank:]][[:cntrl:]][[:graph:]]")
    assert len(result) == 5
    assert result[0].isalnum()
    assert result[1].isdigit()
    assert result[2].isspace()
    assert not result[3].isprintable()
    assert result[4].isprintable() and result[4] != " "
