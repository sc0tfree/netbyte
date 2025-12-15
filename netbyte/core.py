"""Core helpers for netbyte.

This module is intentionally free of socket/CLI code so it can be unit tested.
"""

_SYMBOLS = set("~`!@#$%^&*()_-+={}[]:>;',</?*-+")


def is_symbol(ch: str) -> bool:
    return ch in _SYMBOLS


def _is_printable_reference_byte(b: int) -> bool:
    # Keep the original tool's intent: annotate common readable bytes.
    if b < 0x20 or b >= 0x7F:
        return False
    ch = chr(b)
    return ch.isalpha() or ch.isdigit() or is_symbol(ch)


def to_hex(data: bytes) -> str:
    """Convert bytes to formatted hex with lightweight ASCII references.

    Output is similar to the original Python 2 implementation, e.g.:
        48(H) 65(e) 6C(l) 6C(l) 6F(o) 0D 0A(\n)

    Newlines (0x0A) are rendered with an explicit (\n) marker and a real newline.
    """

    results: list[str] = []
    new_line = True

    for b in data:
        hex_value = f"{b:02X}"

        if _is_printable_reference_byte(b):
            hex_value = f"{hex_value}({chr(b)})"

        if not new_line:
            hex_value = " " + hex_value

        if b == 0x0A and not data.isspace():
            hex_value = hex_value + "(\\n)\n"
            new_line = True
        else:
            new_line = False

        results.append(hex_value)

    return "".join(results)


_HEX_PAIR = set("0123456789abcdefABCDEF")


def parse_hex_bytes(text: str) -> bytes:
    """Parse a user-supplied hex string into bytes.

    Accepts common separators/spaces and optional 0x prefixes.

    Examples:
        "DE AD BE EF" -> b"\xDE\xAD\xBE\xEF"
        "0xDE,0xAD"   -> b"\xDE\xAD"
        "deadbeef"    -> b"\xDE\xAD\xBE\xEF"
    """

    # Strip 0x prefixes and keep only hex digits.
    cleaned_chars = []
    i = 0
    while i < len(text):
        if text[i : i + 2].lower() == "0x":
            i += 2
            continue
        ch = text[i]
        if ch in _HEX_PAIR:
            cleaned_chars.append(ch)
        i += 1

    cleaned = "".join(cleaned_chars)

    if len(cleaned) == 0:
        return b""

    if len(cleaned) % 2 != 0:
        raise ValueError("hex input must contain an even number of hex digits")

    return bytes(int(cleaned[i : i + 2], 16) for i in range(0, len(cleaned), 2))
