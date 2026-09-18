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
#       truncate = shorten_string
#
# Code
# ----
# Specification Below
# ~~~~~~~~~~~~~~~~~~~~
# Given a string `text`, produce a string `result` such that:

# `text`: the input string to (possibly) truncate. May be empty, may
# contain leading/trailing whitespace, and may contain codepoints
# outside the Basic Multilingual Plane (e.g., emoji) or combining
# marks.
#
# Returns: `text` unchanged if it has fewer than 100 codepoints;
# otherwise a string consisting of the first 97 codepoints of `text`
# (with any trailing whitespace run stripped) followed by the literal
# three-character sequence "...".
#
# 1. A "character" is defined as a single Unicode codepoint (not a byte,
#    grapheme cluster, or UTF-16 code unit). All lengths below are measured
#    in codepoints.
# 2. If `len(text) < 100`, then `result == text`: the string is returned
#    completely unmodified, including any leading or trailing whitespace.
# 3. If len(text) >= 100, result is formed by taking the first 97 codepoints 
#    of text, removing any trailing whitespace from that slice, and appending 
#    the literal three-character sequence "...".
#    a. Taking the first 97 codepoints of `text`.
#    b. If the 97th (last) codepoint of that slice is whitespace (as
#       determined by `str.isspace()`, which covers spaces, tabs,
#       newlines, and other Unicode whitespace codepoints), removing that
#       codepoint and every whitespace codepoint immediately preceding it
#       (i.e., stripping the entire trailing run of whitespace), in a
#       single pass -- this check is not repeated after the strip.
#    c. Appending the literal three-character sequence "..." (three ASCII
#       period characters, not the single Unicode ellipsis codepoint
#       U+2026) to the end of the (possibly whitespace-stripped) slice.
# 4. Truncation may fall in the middle of a word, and `truncate` performs
#    no word-boundary detection: it is acceptable for the result to end
#    mid-word (e.g., "testing" -> "test...").
# 5. Truncation may also fall in the middle of a multi-codepoint grapheme
#    cluster (e.g., separating a base character from a combining mark or
#    modifier); this is explicitly acceptable and `truncate` performs no
#    grapheme-cluster-boundary detection.

def truncate(text):
    if len(text) < 100:
        return text

    kept = text[:97]

    if kept and kept[-1].isspace():
        kept = kept.rstrip()

    return kept + "..."

# Tests
# -----
# Strings under 100 codepoints are returned completely unchanged,
# including any trailing whitespace.
def test_1():
    assert truncate("one") == "one"

def test_2():
    assert truncate("") == ""

def test_3():
    text = "a" * 50 + "   "
    assert truncate(text) == text

# A string of exactly 100 codepoints, with no whitespace at the cut
# point, is truncated to 97 original characters plus "...".
def test_4():
    result = truncate("a" * 100)
    assert result == "a" * 97 + "..."
    assert len(result) == 100

# A string of exactly 99 codepoints is left untouched (it is not >= 100).
def test_5():
    text = "a" * 99
    assert truncate(text) == text

# Truncation may cut in the middle of a word; no word-boundary seeking
# is performed.
def test_6():
    result = truncate("testing" * 20)
    assert result == ("testing" * 20)[:97] + "..."
    assert len(result) == 100

# A single whitespace codepoint sitting exactly at the cut point is
# stripped before the ellipsis is appended.
def test_7():
    text = "a" * 96 + " " + "bcd" + "x" * 50
    result = truncate(text)
    assert result == "a" * 96 + "..."
    assert len(result) == 99

# Multiple consecutive whitespace codepoints sitting at the cut point
# are all stripped (the whole trailing run, not just one character).
def test_8():
    text = "a" * 94 + "   " + "bcd" + "x" * 50
    result = truncate(text)
    assert result == "a" * 94 + "..."
    assert len(result) == 97

# Non-space whitespace (tabs, newlines) is recognized and stripped too,
# not just the ASCII space character.
def test_9():
    text = "a" * 96 + "\t\n" + "bcd" + "x" * 50
    result = truncate(text)
    assert result == "a" * 96 + "..."
    assert len(result) == 99

# The appended ellipsis is always the literal three-period sequence,
# never the single Unicode ellipsis codepoint.
def test_10():
    result = truncate("a" * 150)
    assert result.endswith("...")
    assert "\u2026" not in result

# Combining marks are counted as separate Unicode codepoints.
def test_11():
    text = "e\u0301" * 60  # "e" + combining acute accent, repeated
    result = truncate(text)
    assert len(result) == 100
    assert result.endswith("...")

def test_12():
    text = "\U0001F600" * 150  # grinning face emoji, repeated
    result = truncate(text)
    assert len(result) == 100
    assert result.endswith("...")

if __name__ == "__main__":
    tests = [obj for name, obj in list(globals().items())
             if name.startswith("test_") and callable(obj)]
    for test in tests:
        test()
        print(f"{test.__name__}: passed")
    print(f"All {len(tests)} tests passed!")