# Copyright (C) 2026 Bryan A. Jones.
#
# This file is part of the Literate Programming Book.
#
# The Literate Programming Book is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# The Literate Programming Book is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a [copy](../../LICENSE.md) of the GNU General Public
# License along with the Literate Programming Book. If not, see
# [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/).
#
# `my_truncate.py` - holds LLM-generated code for the
# [warmup\_truncate.py](warmup_truncate.py) test bench
# ====================================================
#
# Paste the LLM's answer here, replacing everything below.
#
# Do not edit its code, and do not ask it a follow-up question. The point of the
# warm-up is to see what one sentence bought you. The editor lints as you type,
# so expect underlines under the pasted code; those are style opinions, and
# fixing them is editing.
#
# Your function must be named `truncate`. If the LLM named it something else,
# add an alias at the bottom of the file:
#
# ```
#   truncate = shorten_string
# ```
#
# Code
# ----
#
# The follwoing code was generated using GPT 5.6 luna
#
# I want you to write a python function named truncate that takes an input
# string and truncates after 100 characters with an ellipsis. Ideally the
# function would truncate in a manner that makes sense grammatically. The
# following list shows more detailed specifications to facilitate this. 
#
# * no ellipsis in the middle of a word unless the word is very long
# * ignore leading or trailing whitespace
# * do not put an ellipsis after punctuation.
# * use the ellipsis character, not three periods
# * I want 'character' to refer to a grapheme
# * The ellipsis will also be the 101st character not the 100th character
# * Both the amount of characters before the elipsis and the length of a "long word" 
#   should be input arguments
#
# Afterwards review this spec and list potential problem areas, and solutions

import regex


def truncate(text: str, max_chars: int = 100, long_word: int = 20) -> str:
    """
    Truncate text to max_chars graphemes, adding '…' as the next grapheme.

    Parameters
    ----------
    text : str
        The input string.
    max_chars : int
        Number of graphemes allowed before the ellipsis.
    long_word : int
        A word at least this many graphemes long may be split.

    Returns
    -------
    str
        The truncated string, with '…' as the (max_chars + 1)th grapheme.
    """

    # Remove leading/trailing whitespace.
    text = text.strip()

    # Split into Unicode grapheme clusters.
    graphemes = regex.findall(r"\X", text)

    # No truncation necessary.
    if len(graphemes) <= max_chars:
        return text

    # Candidate cutoff.
    cutoff = max_chars

    # Don't leave trailing whitespace before the ellipsis.
    while cutoff > 0 and graphemes[cutoff - 1].isspace():
        cutoff -= 1

    # Find the beginning of the word containing the cutoff.
    splits_word = (
        cutoff > 0
        and cutoff < len(graphemes)
        and not graphemes[cutoff - 1].isspace()
        and not graphemes[cutoff].isspace()
    )

    if splits_word:
        word_start = cutoff
        while word_start > 0 and not graphemes[word_start - 1].isspace():
            word_start -= 1

        word_end = cutoff
        while word_end < len(graphemes) and not graphemes[word_end].isspace():
            word_end += 1

        if word_end - word_start < long_word and word_start > 0:
            cutoff = word_start

    # Remove trailing whitespace.
    while cutoff > 0 and graphemes[cutoff - 1].isspace():
        cutoff -= 1

    # Do not put an ellipsis immediately after punctuation.
    punctuation = set(".,!?;:")
    if cutoff > 0 and graphemes[cutoff - 1] in punctuation:
        cutoff -= 1

    return "".join(graphemes[:cutoff]) + "…"

import pytest

def test_short_string_is_unchanged():
    assert truncate("Hello, world!") == "Hello, world!"


def test_exactly_max_chars_is_unchanged():
    text = "a" * 100
    assert truncate(text) == text


def test_string_longer_than_max_chars_is_truncated():
    text = "a" * 101
    assert truncate(text) == "a" * 100 + "…"


def test_ellipsis_is_101st_grapheme():
    text = "a" * 150
    result = truncate(text)

    assert len(result) == 101
    assert result[-1] == "…"


def test_custom_max_chars():
    text = "a" * 20

    assert truncate(text, max_chars=10) == "a" * 10 + "…"


def test_custom_long_word():
    text = "a" * 30

    assert truncate(text, max_chars=20, long_word=25) == "a" * 20 + "…"


def test_long_word_can_be_split():
    text = "ThisIsAVeryLongWordThatShouldBeSplit"

    result = truncate(text, max_chars=20, long_word=20)

    assert result == text[:20] + "…"


def test_normal_word_is_not_split():
    text = "The quick brown fox jumps over the lazy dog."

    result = truncate(text, max_chars=20)

    assert result == "The quick brown fox…"


def test_leading_whitespace_is_ignored():
    text = "     Hello world"

    assert truncate(text) == "Hello world"


def test_trailing_whitespace_is_ignored():
    text = "Hello world     "

    assert truncate(text) == "Hello world"


def test_leading_and_trailing_whitespace_are_ignored():
    text = "     Hello world     "

    assert truncate(text) == "Hello world"


def test_whitespace_before_ellipsis_is_removed():
    text = "The quick brown fox jumps over the lazy dog"

    result = truncate(text, max_chars=20)

    assert not result[-2].isspace()
    assert result[-1] == "…"


def test_does_not_put_ellipsis_after_period():
    text = "This is a sentence. " + "a" * 100

    result = truncate(text, max_chars=20)

    assert not result.endswith(".…")


def test_does_not_put_ellipsis_after_comma():
    text = "This is a sentence, " + "a" * 100

    result = truncate(text, max_chars=20)

    assert not result.endswith(",…")


def test_does_not_put_ellipsis_after_exclamation_mark():
    text = "This is exciting! " + "a" * 100

    result = truncate(text, max_chars=20)

    assert not result.endswith("!…")


def test_does_not_put_ellipsis_after_question_mark():
    text = "Is this working? " + "a" * 100

    result = truncate(text, max_chars=20)

    assert not result.endswith("?…")


def test_does_not_put_ellipsis_after_colon():
    text = "Here is the answer: " + "a" * 100

    result = truncate(text, max_chars=20)

    assert not result.endswith(":…")


def test_does_not_put_ellipsis_after_semicolon():
    text = "Here is the answer; " + "a" * 100

    result = truncate(text, max_chars=20)

    assert not result.endswith(";…")


def test_ellipsis_character_is_used():
    text = "a" * 150

    result = truncate(text)

    assert result.endswith("…")
    assert "..." not in result


def test_unicode_graphemes_are_not_split():
    # Each "é" consists of two Unicode code points but one grapheme.
    text = "e\u0301" * 150

    result = truncate(text, max_chars=100)

    assert result.endswith("…")
    assert len(result) > 100
    assert result[:-1] == "e\u0301" * 100


def test_emoji_graphemes_are_not_split():
    text = "👍" * 150

    result = truncate(text, max_chars=100)

    assert result == "👍" * 100 + "…"


def test_emoji_with_skin_tone_is_one_grapheme():
    text = "👍🏽" * 150

    result = truncate(text, max_chars=100)

    assert result == "👍🏽" * 100 + "…"


def test_zwj_emoji_is_not_split():
    # Family emoji is composed of multiple Unicode code points
    # but should be treated as one grapheme.
    family = "👨‍👩‍👧‍👦"
    text = family * 150

    result = truncate(text, max_chars=100)

    assert result == family * 100 + "…"


def test_newline_counts_as_whitespace():
    text = "Hello world\n\n" + "a" * 100

    result = truncate(text, max_chars=12)

    assert not result.endswith("\n…")


def test_tab_counts_as_whitespace():
    text = "Hello\tworld\t" + "a" * 100

    result = truncate(text, max_chars=12)

    assert not result.endswith("\t…")


def test_empty_string():
    assert truncate("") == ""


def test_whitespace_only_string():
    assert truncate("     \t\n   ") == ""


def test_custom_max_chars_one():
    result = truncate("Hello world", max_chars=1)

    assert result == "H…"


def test_custom_max_chars_with_unicode():
    text = "👍🏽" * 10

    result = truncate(text, max_chars=3)

    assert result == "👍🏽" * 3 + "…"


@pytest.mark.parametrize(
    "punctuation",
    [".", ",", "!", "?", ";", ":"],
)
def test_punctuation_is_not_immediately_before_ellipsis(punctuation):
    text = ("word" + punctuation + " ") * 30

    result = truncate(text, max_chars=20)

    assert not result.endswith(punctuation + "…")


@pytest.mark.parametrize(
    "max_chars",
    [1, 2, 5, 10, 25, 50, 99, 100],
)
def test_result_never_exceeds_max_chars_plus_ellipsis(max_chars):
    text = "a" * 500

    result = truncate(text, max_chars=max_chars)

    assert len(result) == max_chars + 1
    assert result[-1] == "…"


@pytest.mark.parametrize(
    "long_word",
    [1, 5, 10, 20, 50],
)
def test_long_word_parameter_is_respected(long_word):
    text = "a" * 100

    result = truncate(text, max_chars=50, long_word=long_word)

    assert result == "a" * 50 + "…"