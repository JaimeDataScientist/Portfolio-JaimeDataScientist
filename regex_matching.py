from functools import lru_cache

def is_match(s: str, p: str) -> bool:
    """Return True if string s matches pattern p."""
    @lru_cache(None)
    def dp(i: int, j: int) -> bool:
        if j == len(p):
            return i == len(s)
        first_match = i < len(s) and (p[j] == s[i] or p[j] == '.')
        if j + 1 < len(p) and p[j + 1] == '*':
            # Two possibilities: skip the star or consume a matching char
            return dp(i, j + 2) or (first_match and dp(i + 1, j))
        else:
            return first_match and dp(i + 1, j + 1)
    return dp(0, 0)

if __name__ == "__main__":
    examples = [
        ("aa", "a", False),
        ("aa", "a*", True),
        ("ab", ".*", True),
    ]
    for s, p, expected in examples:
        result = is_match(s, p)
        print(f"{s!r} {p!r} -> {result} (expected {expected})")
