# LeetCode — Longest Palindromic Substring

A focused Python implementation of **LeetCode's Longest Palindromic Substring (Medium)** that **finds the longest substring reading the same forwards and backwards** by checking **every possible substring**. Clean, minimal, and correct — this solution is the entry point to understanding substring enumeration with `s[i : j + 1]`, the reverse-and-compare palindrome test (`sub == sub[::-1]`), and why a brute-force O(n³) solution leads naturally to the **expand-around-center** idea that interviewers expect.

🔗 **Problem link:** [leetcode.com/problems/longest-palindromic-substring](https://leetcode.com/problems/longest-palindromic-substring/)

---

## Problem Statement

Given a string `s`, return the **longest palindromic substring** in `s`.

A **palindrome** reads the same forwards and backwards. A **substring** is a contiguous sequence of characters within the string.

**Example 1:**

```
Input:  s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.
```

**Example 2:**

```
Input:  s = "cbbd"
Output: "bb"
```

**Official Constraints:**

- `1 <= s.length <= 1000`
- `s` consists of only digits and English letters

---

## The Code

```python
s = input("Enter the string: ")
longest = ""
for i in range(len(s)):
    for j in range(i, len(s)):
        sub = s[i : j + 1]
        if sub == sub[::-1] and len(sub) > len(longest):
            longest = sub

print(longest)
```

---

## The Critical Idea — Check Every Substring, Keep the Longest Palindrome

This is the most important thing to understand about this solution.

**The string `s` is never modified.** The two nested loops pick a **start index `i`** and an **end index `j`**, which together identify one substring. Each substring is tested: if it equals its own reverse, it is a palindrome, and it replaces `longest` only if it is **strictly longer**.

For `s = "babad"` (`n = 5`), every substring is visited:

```
i=0:  b   ba   bab   baba   babad
i=1:      a    ab    aba    abad
i=2:           b     ba     bad
i=3:                 a      ad
i=4:                        d
```

That is `n(n+1)/2 = 15` substrings, and each one costs up to O(n) to slice, reverse, and compare.

| Approach                    | Extra space | Time  |
| --------------------------- | ----------- | ----- |
| **Brute force (this code)** | O(n)        | O(n³) |
| Dynamic programming table   | O(n²)       | O(n²) |
| Expand around center        | O(1)        | O(n²) |
| Manacher's algorithm        | O(n)        | O(n)  |

Brute force is the simplest to write and to trust. It is the right _first_ solution, and the baseline every faster approach is compared against.

---

## How the Loops Work

```python
for i in range(len(s)):
    for j in range(i, len(s)):
        sub = s[i : j + 1]
        if sub == sub[::-1] and len(sub) > len(longest):
            longest = sub
```

- **Outer loop:** `i` runs `0 … n-1` — the **start** of the substring
- **Inner loop:** `j` runs `i … n-1` — the **end** of the substring (inclusive)
- **Slice:** `s[i : j + 1]` — the characters from index `i` through index `j`
- **Palindrome test:** `sub == sub[::-1]` — a string is a palindrome exactly when it equals its reverse
- **Update rule:** `len(sub) > len(longest)` — replace only when strictly longer
- **Result:** after both loops finish, `longest` holds the answer

> **Off-by-one note:** The slice is `s[i : j + 1]`, not `s[i : j]`. Python slices exclude the end index, so `s[i : j]` would drop the character at `j`, and the single-character substring (`j == i`) would be an empty string. The inner loop starts at `i`, not `i + 1`, so that one-character substrings are included. Every single character is a palindrome, which guarantees a valid answer for any non-empty string.

> **Tie-breaking:** the comparison is `>`, not `>=`. When two palindromes have the same length, the **first one found** is kept. That is why `"babad"` gives `"bab"` rather than `"aba"`, matching Example 1. Both are accepted by the problem.

---

## Algorithm (Pseudocode)

```
read s
longest = ""

for i from 0 to n-1:
    for j from i to n-1:
        sub = s[i..j]
        if sub equals reverse(sub) and length(sub) > length(longest):
            longest = sub

print longest
```

---

## Dry Run

**Input:** `s = "cbbd"`

| `i` | `j` | `sub`  | Palindrome? | Longer than `longest`? | `longest` after |
| --- | --- | ------ | ----------- | ---------------------- | --------------- |
| 0   | 0   | `c`    | Yes         | Yes (1 > 0)            | `c`             |
| 0   | 1   | `cb`   | No          | —                      | `c`             |
| 0   | 2   | `cbb`  | No          | —                      | `c`             |
| 0   | 3   | `cbbd` | No          | —                      | `c`             |
| 1   | 1   | `b`    | Yes         | No (1 > 1 is false)    | `c`             |
| 1   | 2   | `bb`   | Yes         | Yes (2 > 1)            | `bb`            |
| 1   | 3   | `bbd`  | No          | —                      | `bb`            |
| 2   | 2   | `b`    | Yes         | No                     | `bb`            |
| 2   | 3   | `bd`   | No          | —                      | `bb`            |
| 3   | 3   | `d`    | Yes         | No                     | `bb`            |

**Output:** `bb` ✅

---

## Complexity Analysis

| Metric | Complexity                                                                                          |
| ------ | --------------------------------------------------------------------------------------------------- |
| Time   | **O(n³)** — about `n²/2` substrings, and each one is sliced, reversed, and compared in O(n)         |
| Space  | **O(n)** — the temporary substring, its reversed copy, and `longest` each hold up to `n` characters |

For the upper limit of `n = 1000`, this means hundreds of thousands of substrings, each up to 1000 characters long. It is fine for learning and small inputs, but it can be slow on the largest inputs, which is why the expand-around-center solution below is the one to rely on.

---

## Edge Cases

| Scenario                                  | Behavior                                                                           |
| ----------------------------------------- | ---------------------------------------------------------------------------------- |
| Single character `"a"`                    | One substring, it is a palindrome — returns `"a"` ✅                               |
| Entire string is a palindrome `"racecar"` | The full-length substring is found and kept — returns `"racecar"` ✅               |
| All characters equal `"aaaa"`             | Returns `"aaaa"` ✅                                                                |
| Even-length palindrome `"cbbd"`           | Returns `"bb"` ✅                                                                  |
| No palindrome longer than 1 `"abc"`       | Returns `"a"` — the first single character found ✅                                |
| Two equally long answers `"babad"`        | Returns the first found, `"bab"` ✅                                                |
| Digits `"12321"`                          | Works on any characters — returns `"12321"` ✅                                     |
| Mixed case `"Aa"`                         | `'A'` and `'a'` differ, so returns `"A"` ✅                                        |
| Empty string `""`                         | Loops never run — prints an empty line ⚠️ (the problem guarantees `n >= 1`)        |
| Spaces typed into the input               | Treated as ordinary characters ⚠️ (the problem guarantees letters and digits only) |

---

## Code-Quality Notes

**This is a script, not a LeetCode submission.** The code reads the string with `input()` and prints the result at the top level. LeetCode instead calls a method on a class, so this code will not run in the LeetCode editor as it is. The submittable version is in the next section.

**Check the cheap condition first.** The test `sub == sub[::-1] and len(sub) > len(longest)` reverses and compares the substring even when it is too short to matter. Swapping the two conditions skips that work for any substring that cannot beat the current answer:

```python
if len(sub) > len(longest) and sub == sub[::-1]:
    longest = sub
```

It gives the same results, but `and` evaluates left to right and stops early, so the expensive comparison runs far less often.

**Wrapping it in a function.** Putting the loops inside a function makes the code reusable and testable, and is required for the LeetCode format.

---

## The Natural Extension — Expand Around Center

A palindrome **mirrors around its center**. Instead of testing every substring, pick every possible **center** and **grow outwards** while the characters on both sides match. There are `2n - 1` centers: `n` single characters (odd-length palindromes) and `n - 1` gaps between neighbors (even-length palindromes).

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        start, end = 0, 0

        def expand(left, right):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return left + 1, right - 1      # the last valid palindrome bounds

        for i in range(len(s)):
            l1, r1 = expand(i, i)           # odd length, centered on i
            l2, r2 = expand(i, i + 1)       # even length, centered between i and i+1
            if r1 - l1 > end - start:
                start, end = l1, r1
            if r2 - l2 > end - start:
                start, end = l2, r2

        return s[start:end + 1]
```

**Trace for `"babad"`:**

| Center `i` | Odd expansion | Even expansion      | Best so far                     |
| ---------- | ------------- | ------------------- | ------------------------------- |
| 0          | `b`           | none (`b` ≠ `a`)    | `b`                             |
| 1          | `bab`         | none (`a` ≠ `b`)    | `bab`                           |
| 2          | `aba`         | none (`b` ≠ `a`)    | `bab` (same length, not longer) |
| 3          | `a`           | none (`a` ≠ `d`)    | `bab`                           |
| 4          | `d`           | none (past the end) | `bab`                           |

**Result:** `"bab"` ✅ — the same answer, without checking every substring.

| Property                       | Brute force (this code)                   | Expand around center          |
| ------------------------------ | ----------------------------------------- | ----------------------------- |
| Time                           | O(n³)                                     | **O(n²)**                     |
| Extra space                    | O(n)                                      | **O(1)**                      |
| Works as a LeetCode submission | ❌ No (script)                            | ✅ Yes                        |
| Complexity of the idea         | Very simple                               | Slightly more to reason about |
| When to use                    | Learning, small inputs, correctness check | Interviews and LeetCode       |

---

## Repository Structure

```
LeetCode-Longest-Palindromic-Substring/
│
├── longest_palindromic_substring.py    # Main Python implementation
└── README.md                           # Project documentation
```

---

## How to Compile and Run

**Prerequisites:** Python 3.8+

```bash
# Clone the repository
git clone https://github.com/rishita-ops/LeetCode-Longest-Palindromic-Substring.git
cd LeetCode-Longest-Palindromic-Substring

# Run
python3 longest_palindromic_substring.py
```

**On Windows:**

```bash
python longest_palindromic_substring.py
```

**Sample session:**

```
Enter the string: babad
bab
```

---

## Key Concepts Covered

- **Palindrome** — a string that equals its own reverse
- **Substring enumeration** — nested loops over start `i` and end `j`
- **Python slicing** — `s[i : j + 1]` for an inclusive end, and `sub[::-1]` to reverse
- **Strict `>` comparison** — keeps the first longest palindrome on ties
- **Brute force cost** — O(n²) substrings times O(n) per check gives O(n³)
- **Short-circuit evaluation** — put the cheap condition first in an `and`
- **Center expansion** — `2n - 1` centers cover both odd and even palindromes
- **Time/space trade-off** — brute force, DP, center expansion, and Manacher's algorithm

---

## Why This Problem Matters in DSA

The palindrome-around-a-center pattern appears across a broad family of problems:

| Problem / Concept                                   | Connection                                                                       |
| --------------------------------------------------- | -------------------------------------------------------------------------------- |
| **Palindromic Substrings** (LeetCode #647)          | Same center expansion, but count every palindrome instead of keeping the longest |
| **Valid Palindrome** (LeetCode #125)                | Two pointers moving inwards from both ends                                       |
| **Valid Palindrome II** (LeetCode #680)             | Two pointers with one allowed mismatch                                           |
| **Longest Palindromic Subsequence** (LeetCode #516) | Dynamic programming where characters need not be contiguous                      |
| **Palindrome Partitioning** (LeetCode #131)         | Backtracking, using a palindrome check on each piece                             |
| **Shortest Palindrome** (LeetCode #214)             | Finds the longest palindromic prefix, then builds on it                          |

Every problem that involves symmetry or mirroring in a string traces back to the center-and-compare idea introduced here.

---

## Contributing

Contributions are welcome. Consider adding:

- The **expand-around-center** version as a separate, submittable file
- A **dynamic programming** version for comparison
- A version that returns **all** longest palindromes instead of the first
- A version that prints the **start and end indices** of the answer
- Input validation for empty strings
- Implementations in C++, Java, or JavaScript

```bash
git checkout -b feature/your-feature
git commit -m "Add: your feature description"
git push origin feature/your-feature
# Then open a Pull Request
```

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

_Part of a structured LeetCode practice series — fundamentals, done right._
