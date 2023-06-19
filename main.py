import itertools
from hgtk.letter import compose, decompose

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
    'common_double_consonants': {
        'ㄲ': ['ㄱ', 'ㄱ'],
        'ㄸ': ['ㄷ', 'ㄷ'],
        'ㅃ': ['ㅂ', 'ㅂ'],
        'ㅆ': ['ㅅ', 'ㅅ'],
        'ㅉ': ['ㅈ', 'ㅈ'],
    },
    'uncommon_double_consontant_batchim': {
        'ㄳ': ['ㄱ', 'ㅅ'],
        'ㄵ': ['ㄴ', 'ㅈ'],
        'ㄶ': ['ㄴ', 'ㅎ'],
        'ㄺ': ['ㄹ', 'ㄱ'],
        'ㄻ': ['ㄹ', 'ㅁ'],
        'ㄼ': ['ㄹ', 'ㅂ'],
        'ㄽ': ['ㄹ', 'ㅅ'],
        'ㄾ': ['ㄹ', 'ㅌ'],
        'ㄿ': ['ㄹ', 'ㅍ'],
        'ㅀ': ['ㄹ', 'ㅎ'],
        'ㅄ': ['ㅂ', 'ㅅ'],
    },
    'common_double_vowels': {
        'ㅘ': ['ㅗ', 'ㅏ'],
        'ㅙ': ['ㅗ', 'ㅐ'],
        'ㅚ': ['ㅗ', 'ㅣ'],
        'ㅝ': ['ㅜ', 'ㅓ'],
        'ㅞ': ['ㅜ', 'ㅔ'],
        'ㅟ': ['ㅜ', 'ㅣ'],
        'ㅢ': ['ㅡ', 'ㅣ'],
        'ㅐ': ['ㅏ', 'ㅣ'],
        'ㅒ': ['ㅑ', 'ㅣ'],
        'ㅔ': ['ㅓ', 'ㅣ'],
        'ㅖ': ['ㅕ', 'ㅣ']
    },
    'uncommon_double_vowels': {
        # ㅑ => ㅣ + ㅏ 까지 하면 뇌절인가?
        'ㅘ': ['ㅗ', 'ㅏ'],
        'ㅙ': ['ㅗ', 'ㅏ', 'ㅣ'],
        'ㅚ': ['ㅗ', 'ㅣ'],
        'ㅝ': ['ㅜ', 'ㅓ'],
        'ㅞ': ['ㅜ', 'ㅓ', 'ㅣ'],
        'ㅟ': ['ㅜ', 'ㅣ'],
        'ㅢ': ['ㅡ', 'ㅣ'],
        'ㅐ': ['ㅏ', 'ㅣ'],
        'ㅒ': ['ㅑ', 'ㅣ'],
        'ㅔ': ['ㅓ', 'ㅣ'],
        'ㅖ': ['ㅕ', 'ㅣ']
    },

}

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

total_vowels = list(organized['vowels'].values()) + list(organized['half-vowels'].values())
total_consonants = list(organized['consonants'].values())
total_double_consonants = list(organized['common_double_consonants'].keys()) + list(organized['uncommon_double_consontant_batchim'].keys())
total_conversion_table = {**organized['half-vowels'], **organized['vowels'], **organized['consonants'], **organized['common_double_consonants'], **organized['uncommon_double_consontant_batchim'], **organized['common_double_vowels']}

def transliterate_hangul(text):
    result = ''
    for char in text:
        result += table[char]
    return result


def roman_to_hangul(text):
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

    # Add filler consonant if the first character of each split words is a vowel
    for words in result.split(' '):
        if words[0] in total_vowels:
            result = result.replace(words, 'ㅇ' + words)

    for i in range(len(result) - 1):
        # if two vowel jamos consecute, add a filler consonant
        if result[i] in total_vowels and result[i + 1] in total_vowels:
            result = result[:i + 1] + 'ㅇ' + result[i + 1:]

    return result


def get_permutations(elements, n):
    return [perm for perm in itertools.permutations(elements, n)]


class HangulAnagrammer: # TODO: create class for this
    pass

def decompose_word(word):
    # Decompose each character in the word
    decomposed_word = [decompose(char) for char in word]

    # Flatten the list of tuples into a list of jamos
    jamos = [jam for tup in decomposed_word for jam in tup]

    return jamos


def is_palindrome(word):
    return word == word[::-1]

# NEARLY-IMPOSSIBLE-TODO: add support for sentences
# NEARLY-IMPOSSIBLE-TODO: finding 'real' anagrams
# word = "간사"
# word = "무긍늑"
# word = '노사'
word = "국화" # TODO: 1. add support for combined vowels
# word = "뷁" # TODO: 2. set the level of the anagram by using 3 options (allow_combined_consonant_exchange, allow_vowel_exchange, allow_partial_anagrams)
# word = "찰흙"
# word = "눅눅"
# word = "김흥국"
# jamos = [transliterate_hangul(x) for x in [char for tup in [decompose(x) for x in word] for sub_tup in tup for char in sub_tup]]
# jamos = [x for x in [char for tup in [decompose(x) for x in word] for sub_tup in tup for char in sub_tup]]
if is_palindrome(word):
    print('Palindrome detected! The results are going to be doubled!')

jamos = ['!' if x == '' else x for x in decompose_word(word)]
print(jamos)

# if any of the elements in total_double_consonants is in jamos
has_double_consonant = any(x in jamos for x in total_double_consonants)
if has_double_consonant:
    print('Double consonant detected!')
    if len(word) == 1:
        pass
        # check if convertible, any of the consonant in batchim with the initial consonant
    else:
        jamos += total_conversion_table[jamos[jamos.index([x for x in jamos if x in total_double_consonants][0])]]
print(jamos, "after")

true_consonants = [x for x in jamos if x in total_consonants]
consonants = [x for x in jamos if x in total_consonants or x == '!' or x in total_double_consonants]
print(f'{consonants=}')
vowels = [x for x in jamos if x in total_vowels]
print(f'{vowels=}')

# All valid syllables
valid_syllables = []

# # starting from 2 syllables
# for c1, c2, fc1, fc2 in itertools.permutations(consonants, 4):
#     for v1, v2 in itertools.permutations(vowels, 2):
#         # Form the syllables
#         syllable1 = compose(c1, v1, fc1)
#         syllable2 = compose(c2, v2, fc2)
#
#         # Append to the list of valid syllables
#         valid_syllables.append(syllable1 + syllable2)
num_syllables = len(word)
num_consonants_per_syllable = num_syllables * 2  # 2 consonants per syllable (initial and final)
num_vowels_per_syllable = num_syllables  # 1 vowel per syllable

consonant_perms = get_permutations(consonants, num_consonants_per_syllable)
vowel_perms = get_permutations(vowels, num_vowels_per_syllable)

if len(true_consonants) % 2 == 1 and len(set(vowel_perms)) != len(vowel_perms):
    vowel_perms = list(set(vowel_perms))
print(f'{vowel_perms=}')

for consonant_perm in consonant_perms:
    print(f'{consonant_perm=}')
    if consonant_perm[0] == "!" or consonant_perm[0] in total_double_consonants:
        continue
    skip = False
    for i in range(0,len(consonant_perm)-1, 2):
        if consonant_perm[i] == "!" or consonant_perm[i] in total_double_consonants:
            skip = True
            break
    if skip:
        continue

    for vowel_perm in vowel_perms:
        syllable = ""
        is_partial_anagram = False
        # check if true consonants are odd and if the vowels has duplicates
        for i in range(num_syllables):
            # if consonant_perm[i*2] == "!" or consonant_perm[i*2] in total_double_consonants:
            #     # skip = True
            #     continue
            # Form the syllable
            # IMPROVED FILTERING ABOVE
            if consonant_perm[i * 2 + 1] in total_double_consonants:
                # print("batchim double consonant detected")
                is_partial_anagram = True
            print(consonant_perm[i * 2], vowel_perm[i], consonant_perm[i * 2 + 1])
            if consonant_perm[i*2+1] == "!":
                syllable += compose(
                    consonant_perm[i*2],  # Initial consonant
                    vowel_perm[i],  # Vowel
                    ""
                )
            else:
                syllable += compose(
                    consonant_perm[i*2],  # Initial consonant
                    vowel_perm[i],  # Vowel
                    consonant_perm[i*2 + 1]  # Final consonant
                )
            # syllable += compose(
        # Append to the list of valid syllables
        if len(syllable) == num_syllables:
            if not is_partial_anagram and has_double_consonant:
                syllable += "* (partial anagram)"
            valid_syllables.append(syllable)
            print("append", syllable)
        else: # this never happens? maybe it does
            print("incomplete, skip", syllable)

    # print(f'{valid_syllables=}') # TODO: add logging

final = []
# Print all valid syllables
for syllable in valid_syllables:
    final.append(syllable)
    print(syllable)

print(len(final))


""" old file

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

"""
