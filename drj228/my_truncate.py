# Copyright (C) 2026 Bryan A. Jones.
#
# This file is part of the Literate Programming Book.
#
# The Literate Programming Book is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# The Literate Programming Book is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a [copy](../../LICENSE.md) of the GNU General Public
# License along with the Literate Programming Book. If not,
# see [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/).
#
# `my_truncate.py` - holds LLM-generated code for the
# [warmup_truncate.py](warmup_truncate.py) test bench
# ====================================================
#
# Code
# ----

# Specification
# =============
#
# The purpose of truncate() is to limit a string to a maximum length of
# 100 characters while clearly showing when truncation has occurred.
#
# The function signature is:
#
#     truncate(text)
#
# The function accepts exactly one argument, text. The 100-character limit
# is fixed and is not supplied as a parameter.
#
#
# Question 1:
# What happens if the input string contains 100 characters or fewer?
#
# Answer:
# The original string is returned unchanged.
#
# Reason:
# A string that is already within the allowed size does not need to be
# shortened or marked with an ellipsis.
#
#
# Question 2:
# What happens if the input string contains more than 100 characters?
#
# Answer:
# The string is shortened so that the final returned value is exactly
# 100 characters long.
#
# Reason:
# This guarantees that the returned string will always fit within a
# 100-character maximum.
#
#
# Question 3:
# Does the 100-character maximum include the ellipsis?
#
# Answer:
# Yes. The ellipsis is included in the 100-character maximum.
#
# Reason:
# If the ellipsis were added after 100 characters, the returned string
# would exceed the stated maximum length.
#
#
# Question 4:
# What is considered an ellipsis?
#
# Answer:
# An ellipsis is represented by three ASCII period characters: "...".
#
# Reason:
# Three periods are simple, widely recognized, and do not require special
# Unicode handling.
#
#
# Question 5:
# How many characters from the original string are kept when truncation
# occurs?
#
# Answer:
# The number of characters kept is the 100-character limit minus the
# length of the ellipsis. Since "..." contains three characters, the
# first 97 characters are kept.
#
# Reason:
# The 97 original characters plus the 3 characters in the ellipsis
# produce a final length of exactly 100 characters.
#
#
# Question 6:
# Can truncation occur in the middle of a word?
#
# Answer:
# Yes. The function may truncate in the middle of a word.
#
# Reason:
# Maintaining an exact maximum length of 100 characters is more important
# for this function than preserving complete words.
#
#
# Question 7:
# Does the function search backward for a space or word boundary?
#
# Answer:
# No. The function does not search for a word boundary before truncating.
#
# Reason:
# Doing so would add behavior that is not required and could make the final
# result shorter than necessary.
#
#
# Question 8:
# How is whitespace handled?
#
# Answer:
# Leading whitespace, trailing whitespace, and whitespace inside the string
# are preserved. The truncated prefix is not stripped.
#
# Reason:
# The function should not modify the content of the string except when
# truncation is necessary. If the 97th character is whitespace, that
# whitespace remains directly before the ellipsis.
#
#
# Question 9:
# Does whitespace count toward the 100-character limit?
#
# Answer:
# Yes. Whitespace counts toward the limit just like any other character.
#
# Reason:
# Python strings include whitespace as part of their length.
#
#
# Question 10:
# What exactly is considered a character?
#
# Answer:
# Characters are counted using Python's built-in len() function.
#
# Reason:
# Using len() provides a simple and consistent definition that matches
# normal Python string behavior.
#
#
# Question 11:
# Does the function perform special grapheme or emoji handling?
#
# Answer:
# No. The function does not perform special Unicode grapheme handling.
# Truncation may therefore occur in the middle of a grapheme cluster.
#
# Reason:
# The specification uses Python's len() and normal string slicing.
# No repair is performed if the cut separates a Unicode sequence.
#
#
# Question 12:
# What happens if the input is an empty string?
#
# Answer:
# The empty string is returned unchanged.
#
# Reason:
# Its length is already below the 100-character maximum.
#
#
# Question 13:
# Is the 100-character limit inclusive?
#
# Answer:
# Yes. A string containing exactly 100 characters is valid and is returned
# unchanged. Truncation begins only when the length is greater than 100.
#
# Reason:
# The stated maximum allows strings up to and including 100 characters.
#
#
# Question 14:
# What happens if text is not a string?
#
# Answer:
# The function raises TypeError. It does not convert the value to a string
# or return a special value.
#
# Reason:
# Silent conversion could hide an error made by the caller. Values such as
# None and bytes are therefore rejected.
#
#
# Question 15:
# Is the maximum length configurable?
#
# Answer:
# No. truncate() accepts only text, and the maximum length is fixed at
# 100 characters.
#
# Reason:
# The purpose of this function is specifically to enforce the
# 100-character limit.
#
#
# Question 16:
# What happens when whitespace occurs exactly at the truncation point?
#
# Answer:
# The whitespace is preserved. The function does not call strip() or
# rstrip() before adding the ellipsis.
#
# Reason:
# Removing the whitespace would alter the original content and would also
# cause the returned value to be shorter than the required 100 characters.
#
#
# Question 17:
# What happens if truncation splits a Unicode grapheme cluster?
#
# Answer:
# The function keeps the first 97 values counted by Python's normal string
# slicing even if this splits a visible grapheme cluster.
#
# Reason:
# No special grapheme-processing or repair is performed.
#
#
# Question 18:
# Does the function perform Unicode normalization?
#
# Answer:
# No. The input is counted and sliced exactly as received.
#
# Reason:
# Visually identical strings may have different lengths depending on their
# Unicode representation. The function does not alter that representation.
#
#
# Additional behavior:
#
# truncate() is a pure function. It performs no input/output, logging, or
# mutation. For valid string input it does not intentionally raise an
# exception.
#
#
# Parameter:
# text - The string that will be checked and, if necessary, truncated.
#
# Return value:
# The function returns the original string if its length is 100 characters
# or fewer. If its length is greater than 100 characters, the function
# returns the first 97 characters followed by "...", producing a string
# with a total length of 100 characters.
#
#
# Worked examples:
#
# truncate("")
# returns ""
#
# truncate("hello")
# returns "hello"
#
# truncate("a" * 100)
# returns the original 100-character string.
#
# truncate("a" * 101)
# returns 97 "a" characters followed by "...".
#
# If character 97 is a space, that space is preserved immediately before
# the ellipsis.
#
# truncate(None)
# raises TypeError.


def truncate(text):
    """Return text unchanged or truncate it to 100 characters."""

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    limit = 100
    ellipsis = "..."

    if len(text) <= limit:
        return text

    prefix_length = limit - len(ellipsis)
    return text[:prefix_length] + ellipsis


# Tests
# =====


def test_short_string():
    assert truncate("one") == "one"


def test_empty_string():
    assert truncate("") == ""


def test_99_characters():
    text = "a" * 99
    assert truncate(text) == text


def test_100_characters():
    text = "a" * 100
    result = truncate(text)

    assert result == text
    assert len(result) == 100


def test_101_characters():
    text = "a" * 101
    result = truncate(text)

    assert result == ("a" * 97) + "..."
    assert len(result) == 100


def test_long_string():
    text = "b" * 500
    result = truncate(text)

    assert result == ("b" * 97) + "..."
    assert len(result) == 100


def test_whitespace():
    text = ("a" * 96) + " " + ("b" * 20)
    result = truncate(text)

    assert result == ("a" * 96) + " " + "..."
    assert len(result) == 100


def test_leading_whitespace():
    text = (" " * 5) + ("a" * 96)
    result = truncate(text)

    assert result == text[:97] + "..."
    assert result.startswith(" " * 5)
    assert len(result) == 100


def test_trailing_whitespace():
    text = "hello     "
    result = truncate(text)

    assert result == text
    assert len(result) == 10


def test_middle_of_word():
    text = "abcdefghij" * 11
    result = truncate(text)

    assert result == text[:97] + "..."
    assert len(result) == 100


def test_ellipsis():
    text = "x" * 150
    result = truncate(text)

    assert result[-3:] == "..."
    assert len(result) == 100


def test_exact_cutoff():
    text = ("a" * 97) + "XYZ123"
    result = truncate(text)

    assert result == ("a" * 97) + "..."
    assert len(result) == 100


def test_tab_character():
    text = ("a" * 96) + "\t" + ("b" * 10)
    result = truncate(text)

    assert result == ("a" * 96) + "\t" + "..."
    assert len(result) == 100


def test_newline_character():
    text = ("a" * 96) + "\n" + ("b" * 10)
    result = truncate(text)

    assert result == ("a" * 96) + "\n" + "..."
    assert len(result) == 100


def test_unicode():
    text = "é" * 101
    result = truncate(text)

    assert result == ("é" * 97) + "..."
    assert len(result) == 100


def test_non_string():
    try:
        truncate(None)
        assert False, "Expected TypeError"
    except TypeError:
        pass


def test_bytes_rejected():
    try:
        truncate(b"a" * 101)
        assert False, "Expected TypeError"
    except TypeError:
        pass