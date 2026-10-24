"""
Longest Palindromic Substring :
Given a string s, return the longest palindromic substring in s

Example 1:
Input: s = "babad"
Output: "bab"
Explanation: "aba" is also a valid answer.

Example 2:
Input: s = "cbbd"
Output: "bb"
"""
s = input("Enter the string: ")
longest = ""
for i in range(len(s)):
    for j in range(i, len(s)):
        sub = s[i : j + 1]
        if sub == sub[::-1] and len(sub) > len(longest):
            longest = sub

print(longest)


