from __future__ import annotations

import ply.lex as lex


tokens = (
    "TYPE",
    "RELATION",
    "RELATION_TYPE",
    "PERMISSION_TYPE",
)


def t_TYPE(t):
    r"""(?<=type\s)[a-zA-Z_][a-zA-Z0-9_]*"""
    t.value = t.value.strip()
    return t


def t_PERMISSION_TYPE(t):
    r""":\s*(?![^\n]*\[)([^\n]+)"""
    t.value = [
        v.strip().strip(":").strip() for v in t.value.split(" or ") if len(v) > 1
    ]
    return t


def t_RELATION(t):
    r"""\s*define\s+([a-zA-Z_][a-zA-Z0-9_]*)"""

    t.value = t.value.strip().lstrip("define").strip()
    return t


def t_RELATION_TYPE(t):
    r""":\s*\[([^\]]+)\]"""

    t.value = [v.strip() for v in t.value.strip().strip(": [").strip("]").split(",")]
    return t


def t_error(t):
    t.lexer.skip(1)


lexer = lex.lex()
