"""sentence-splitter-lite — 健壮的中英文分句。

处理边界：英文缩写（Mr. Dr. U.S.）、小数点（3.14）、引号、省略号（... / ……）、
感叹/问号叠加（！？!!?）等。输出句子列表，零第三方依赖。
"""
from __future__ import annotations

import re

# 标题/专有缩写：其后的 . 永远不算句末（Dr. Smith、U.S.、3 p.m.）
# 注意：etc / e.g / i.e 等「句末即新句」型缩写刻意不列入，
#       它们后面若跟大写开头则正常断句。
ABBREVIATIONS = {
    "mr", "mrs", "ms", "dr", "prof", "sr", "jr", "st",
    "u", "s", "am", "pm", "inc", "ltd", "co", "corp",
    "no", "vol", "pp", "pg", "fig", "ca", "approx",
}

# 句末标点（中英文）
_TERMINAL = ".!?"
_TERMINAL_CN = "。！？"
_ALL_TERMINAL = _TERMINAL + _TERMINAL_CN


def _is_cjk(ch: str) -> bool:
    return "\u4e00" <= ch <= "\u9fff"


def split_sentences(text: str) -> list[str]:
    """把一段文本切分为句子列表，保留句子内原始标点，去除首尾空白。"""
    if not text or not text.strip():
        return []

    chars = list(text)
    n = len(chars)
    is_break = [False] * n

    ellipsis = [False] * n
    for m in re.finditer(r"…+|\.{3,}", text):
        for i in range(m.start(), m.end()):
            ellipsis[i] = True

    i = 0
    while i < n:
        ch = chars[i]
        if ch in _ALL_TERMINAL and not ellipsis[i]:
            if ch == ".":
                if _dot_is_terminal(chars, i):
                    is_break[i] = True
            else:
                is_break[i] = True
        i += 1

    sentences: list[str] = []
    start = 0
    i = 0
    while i < n:
        if is_break[i]:
            end = i + 1
            while end < n and chars[end] in _ALL_TERMINAL:
                end += 1
            while end < n and chars[end] in '”"\'）)】』':
                end += 1
            sent = "".join(chars[start:end]).strip()
            if sent:
                sentences.append(sent)
            start = end
            while start < n and chars[start] in " \t":
                start += 1
            i = start
            continue
        i += 1
    tail = "".join(chars[start:]).strip()
    if tail:
        sentences.append(tail)
    return sentences


def _dot_is_terminal(chars: list[str], i: int) -> bool:
    """判断位置 i 处的 '.' 是否为句末点。"""
    n = len(chars)
    left = i - 1
    right = i + 1
    if left >= 0 and chars[left].isdigit() and right < n and chars[right].isdigit():
        return False

    j = i - 1
    while j >= 0 and chars[j].isalpha():
        j -= 1
    word = "".join(chars[j + 1:i]).lower()
    if word in ABBREVIATIONS:
        return False

    if right >= n:
        return True
    nxt = chars[right]
    if _is_cjk(nxt):
        return True
    k = right
    while k < n and chars[k] == " ":
        k += 1
    if k < n:
        after = chars[k]
        if after.isupper() or _is_cjk(after):
            return True
        if after.islower():
            return False
    return True
