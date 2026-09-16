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
# Question:
# Write a Python function that truncates a string to 100 characters
# and adds an ellipsis.
# Code
# fingerprint: 6142bb82
# ----
# Specifications:
# 1: Strip any trailing whitespace from 's' and strip trailing
# whitespace from the truncated segment and append U+2026(...)
# 2. If len(s) <= 100, return s + "..." (use U+2026)
# 3. If len(s) > 100:
# 3a. Look at the first 100 characters (s[:100])
# 3b. If s[:100] contains no spaces, return s[:100].rstrip() + "..."
# 3c. If s[:100] ends inside a word, drop that partial word back to the last space.
# 4. Strip any trailing whitespace from the truncated text and append "..."
# 5. Ensure the final output is <= 101 characters
# 6. Grapheme clusters are supported and treat each instance as one character
# text (str): truncate the input string
# If len(s) <=0; then raise a type error.
# Parameter: text(str) - The input string to be truncated.
# Returns: str with the truncated string appended to the ellipsis (U+2026).


import unicodedata

def truncate(text: str) -> str:
    # Handle the length <= 0 requirement and type checking
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    if len(text) <= 0:
        raise TypeError("Input string length must be greater than 0.")

    # 1: Strip trailing whitespace from 's' (original string)
    s = text.rstrip()

    # 6: Grapheme clusters are supported and treated as one character
    # We build clusters by combining base characters with their marks (diacritics)
    clusters = []
    for char in s:
        # If the character is a combining mark and we have a base character
        if unicodedata.category(char).startswith('M') and clusters:
            clusters[-1] += char
        else:
            clusters.append(char)
    ellipsis = "\u2026"  # U+2026 (...)

    # 2: If len(s) <= 100, return s + "..."
    if len(clusters) <= 100:
        return "".join(clusters) + ellipsis

    # 3: If len(s) > 100
    # 3a: Look at the first 100 characters
    first_100 = clusters[:100]

    # Check if there are any spaces in the first 100 characters
    # We check the first character of the cluster in case a space has a combining mark
    has_space = any(c[0].isspace() for c in first_100)

    if not has_space:
        # 3b: If s[:100] contains no spaces, return s[:100].rstrip() + "..."
        truncated = "".join(first_100).rstrip()
    else:
        # 3c: If s[:100] ends inside a word, drop that partial word back to the last space.
        # It ends inside a word if the 100th char (index 99) is NOT a space 
        # AND the 101st char (index 100) is NOT a space
        if not first_100[-1][0].isspace() and not clusters[100][0].isspace():
            # Drop partial word back to the last space
            last_space_idx = 99
            while last_space_idx >= 0 and not first_100[last_space_idx][0].isspace():
                last_space_idx -= 1
            # Slice up to the last space found
            if last_space_idx >= 0:
                first_100 = first_100[:last_space_idx]

        # 4: Strip any trailing whitespace from the truncated text
        truncated = "".join(first_100).rstrip()

    # 5: Ensure the final output is <= 101 characters (appends 1 char ellipsis)
    return truncated + ellipsis
