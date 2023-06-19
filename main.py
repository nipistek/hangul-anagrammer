import itertools

from pprint import pprint
from hgtk.letter import compose, decompose
# from jamo import h2j, j2hcj
# # from hangul_romanize import Transliter
# from korean_romanizer import Romanizer
# from hangul_utils import join_jamos, split_syllables

def transliterate_hangul(text):
    table = {
        'ㅏ': 'a',
        'ㅑ': 'ya',
        'ㅓ': 'eo',
        'ㅕ': 'yeo',
        'ㅗ': 'o',
        'ㅛ': 'yo',
        'ㅜ': 'u',
        'ㅠ': 'yu',
        'ㅡ': 'eu',
        'ㅣ': 'i',
        'ㅐ': 'ae',
        'ㅒ': 'yae',
        'ㅔ': 'e',
        'ㅖ': 'ye',
        'ㅘ': 'wa',
        'ㅙ': 'wae',
        'ㅚ': 'oe',
        'ㅝ': 'wo',
        'ㅞ': 'we',
        'ㅟ': 'wi',
        'ㅢ': 'ui',
        'ㄱ': 'g',
        'ㄲ': 'kk',
        'ㄴ': 'n',
        'ㄷ': 'd',
        'ㄸ': 'tt',
        'ㄹ': 'r',
        'ㅁ': 'm',
        'ㅂ': 'b',
        'ㅃ': 'pp',
        'ㅅ': 's',
        'ㅆ': 'ss',
        'ㅇ': '',
        'ㅈ': 'j',
        'ㅉ': 'jj',
        'ㅊ': 'ch',
        'ㅋ': 'k',
        'ㅌ': 't',
        'ㅍ': 'p',
        'ㅎ': 'h',
    }

    result = ''
    for char in text:
        result += table[char]
    return result


def roman_to_hangul(text):
    organized = {
        'half-vowels': {
            'yeo': 'ㅕ',
            'ye': 'ㅖ',
            'yo': 'ㅛ',
            'yu': 'ㅠ',
            'ya': 'ㅑ',
            'wa': 'ㅘ',
            'we': 'ㅞ',
            'wi': 'ㅟ',
            'weo': 'ㅝ',
        },
        'vowels': {
            'ae': 'ㅐ',
            'e': 'ㅔ',
            'i': 'ㅣ',
            'o': 'ㅗ',
            'u': 'ㅜ',
            'a': 'ㅏ',
            'eo': 'ㅓ',
            'eu': 'ㅡ',
        },
        'consonants': {
            'ng': 'ㅇ',
            'kk': 'ㄲ',
            'tt': 'ㄸ',
            'dd': 'ㄸ',
            'pp': 'ㅃ',
            'ss': 'ㅆ',
            'jj': 'ㅉ',
            'ch': 'ㅊ',
            'sha': 'ㅅㅑ',
            'k': 'ㅋ',
            't': 'ㅌ',
            'p': 'ㅍ',
            'h': 'ㅎ',
            'b': 'ㅂ',
            'd': 'ㄷ',
            'g': 'ㄱ',
            'j': 'ㅈ',
            's': 'ㅅ',
            'm': 'ㅁ',
            'n': 'ㄴ',
            'r': 'ㄹ',
            'l': 'ㄹ',
        },
    }

    conversion_table = {
        **organized['half-vowels'],
        **organized['vowels'],
        **organized['consonants'],
    }

    result = ''
    i = 0
    while i < len(text):
        # Check for longer syllables first
        if i < len(text) - 2 and text[i:i + 3].lower() in conversion_table:
            result += conversion_table[text[i:i + 3].lower()]
            i += 3
        elif i < len(text) - 1 and text[i:i + 2].lower() in conversion_table:
            result += conversion_table[text[i:i + 2].lower()]
            i += 2
        elif text[i].lower() in conversion_table:
            result += conversion_table[text[i].lower()]
            i += 1
        else:
            result += text[i]
            i += 1

    total_vowels = list(organized['vowels'].values()) + list(organized['half-vowels'].values())
    # Add filler consonant if the first character of each split words is a vowel
    for words in result.split(' '):
        if words[0] in total_vowels:
            result = result.replace(words, 'ㅇ' + words)


    for i in range(len(result) - 1):
        # if two vowel jamos consecute, add a filler consonant
        if result[i] in total_vowels and result[i + 1] in total_vowels:
            result = result[:i + 1] + 'ㅇ' + result[i + 1:]

    return result


# Define the decomposition of the word into jamos
word = '굠문'
jamos = [transliterate_hangul(x) for x in [char for tup in [decompose(x) for x in word] for sub_tup in tup for char in sub_tup]]
print(jamos)

# Separate vowels and consonants
vowels = [x for x in jamos if x in ['yo', 'u']]
consonants = [x for x in jamos if x not in vowels]
print(vowels)
print(consonants)

# Get all permutations of 3 consonants and 2 vowels
consonant_perms = list(itertools.permutations(consonants))
vowel_perms = list(itertools.permutations(vowels))
print(consonant_perms)
print(vowel_perms)

valid_combinations = []

# Iterate through all permutations
for c in consonant_perms:
    for v in vowel_perms:
        # Create potential words
        word1 = [c[0], v[0], c[1]]
        word2 = [c[2], v[1], c[3]]
        valid_combinations.append((''.join(word1), ''.join(word2)))

# Print the valid combinations
for comb in valid_combinations:
    print(comb[0], comb[1])


complete = []
for comb in valid_combinations:
    complete.append((comb[0], comb[1], compose(*roman_to_hangul(comb[0])) + compose(*roman_to_hangul(comb[1]))))
    print(compose(*roman_to_hangul(comb[0])) + compose(*roman_to_hangul(comb[1])) )

pprint(sorted(complete, key=lambda x: x[2]))
print(len(complete))
