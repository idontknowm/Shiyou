"""
Author: Yinqin Zhao
Date: 2024-2-27
Mail: zyq21@mails.tsinghua.edu.cn
"""

import sys

def replace_chars(string, k):
    last_seen = {}  # Dictionary to track the last occurrence of each character
    result = ''
    
    for i, char in enumerate(string):
        if char in last_seen and i - last_seen[char] <= k:
            result += '-'
        else:
            result += char
        last_seen[char] = i

    return result

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_string> <k>")
        sys.exit(1)

    input_str = sys.argv[1]
    k = int(sys.argv[2])

    output_str = replace_chars(input_str, k)
    print(output_str)
