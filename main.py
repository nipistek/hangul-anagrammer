import dataclasses
import logging
import itertools
from typing import List, Dict, Any

from hgtk.letter import compose, decompose

organized = {
    'half-vowels-roman': {
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
    'vowels-roman': {
        'ae': 'ㅐ',
        'e': 'ㅔ',
        'i': 'ㅣ',
        'o': 'ㅗ',
        'u': 'ㅜ',
        'a': 'ㅏ',
        'eo': 'ㅓ',
        'eu': 'ㅡ',
    },
    'consonants-roman': {
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

combinations = {
    'vowels': {
        ('ㅗ', 'ㅏ'): 'ㅘ',
        ('ㅗ', 'ㅐ'): 'ㅙ',
        ('ㅗ', 'ㅣ'): 'ㅚ',
        ('ㅜ', 'ㅓ'): 'ㅝ',
        ('ㅜ', 'ㅔ'): 'ㅞ',
        ('ㅜ', 'ㅣ'): 'ㅟ',
        ('ㅡ', 'ㅣ'): 'ㅢ',
        ('ㅏ', 'ㅣ'): 'ㅐ',
        ('ㅑ', 'ㅣ'): 'ㅒ',
        ('ㅓ', 'ㅣ'): 'ㅔ',
        ('ㅕ', 'ㅣ'): 'ㅖ',
    },
    'consonants': {
        ('ㄱ', 'ㅅ'): 'ㄳ',
        ('ㄴ', 'ㅈ'): 'ㄵ',
        ('ㄴ', 'ㅎ'): 'ㄶ',
        ('ㄹ', 'ㄱ'): 'ㄺ',
        ('ㄹ', 'ㅁ'): 'ㄻ',
        ('ㄹ', 'ㅂ'): 'ㄼ',
        ('ㄹ', 'ㅅ'): 'ㄽ',
        ('ㄹ', 'ㅌ'): 'ㄾ',
        ('ㄹ', 'ㅍ'): 'ㄿ',
        ('ㄹ', 'ㅎ'): 'ㅀ',
        ('ㅂ', 'ㅅ'): 'ㅄ',
        ('ㄱ', 'ㄱ'): 'ㄲ',
        ('ㄷ', 'ㄷ'): 'ㄸ',
        ('ㅂ', 'ㅂ'): 'ㅃ',
        ('ㅅ', 'ㅅ'): 'ㅆ',
        ('ㅈ', 'ㅈ'): 'ㅉ',
    },
    'special': { # 약간 억지
        ('ㅗ', 'ㅏ', 'ㅣ'): 'ㅙ',
        ('ㅜ', 'ㅓ', 'ㅣ'): 'ㅞ',
    }
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

total_vowels = list(organized['vowels-roman'].values()) + list(organized['half-vowels-roman'].values())
total_consonants = list(organized['consonants-roman'].values())
total_double_consonants = list(organized['common_double_consonants'].keys()) + list(organized['uncommon_double_consontant_batchim'].keys())
total_double_vowels = list(organized['common_double_vowels'].keys()) + list(organized['uncommon_double_vowels'].keys())

sum_of_doublers = total_double_consonants + total_double_vowels

total_conversion_table = { **organized['common_double_consonants'], **organized['uncommon_double_consontant_batchim'], **organized['common_double_vowels'], **organized['uncommon_double_vowels'] }
total_combinations = { **combinations['consonants'], **combinations['vowels'], **combinations['special'] }

def transliterate_hangul(text):
    result = ''
    for char in text:
        result += table[char]
    return result


def roman_to_hangul(text):
    conversion_table = {
        **organized['half-vowels-roman'],
        **organized['vowels-roman'],
        **organized['consonants-roman'],
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
    return [perm for perm in itertools.permutations(elements, n)] if n > 1 else elements


def decompose_word(word):
    # Decompose each character in the word
    decomposed_word = [decompose(char) for char in word]

    # Flatten the list of tuples into a list of jamos
    jamos = [jam for tup in decomposed_word for jam in tup]

    return jamos


def is_palindrome(word):
    return word == word[::-1] if len(word) > 1 else False


class HangulAnagrammer: # TODO: create class for this
    pass

# NEARLY-IMPOSSIBLE-TODO: add support for sentences
# NEARLY-IMPOSSIBLE-TODO: finding 'real' anagrams by using a dictionary? (maybe not), or by using a certain combination that looks like a word
# word = "간사"
# word = "무긍늑"
# word = '노사'
# word = "국화"
# word = "뷁" # TODO: 2. set the level of the anagram by using 3 options (allow_batchim_consonant_exchange, allow_double_vowel_exchange, allow_partial_anagrams)
# word = "쁡"
# word = "찰흙"
# word = "눅눅"
# word = "김흥국"
# word = "으하하"
# word = "흐갸" # TODO: 1. add support for brain-freezing vowel combinations
# jamos = [transliterate_hangul(x) for x in [char for tup in [decompose(x) for x in word] for sub_tup in tup for char in sub_tup]]
# jamos = [x for x in [char for tup in [decompose(x) for x in word] for sub_tup in tup for char in sub_tup]]

ALLOW_BATCHIM_CONSONANT_EXCHANGE = False
ALLOW_DOUBLE_VOWEL_EXCHANGE = False
ALLOW_PARTIAL_ANAGRAMS = True


if is_palindrome(word):
    print('Palindrome detected!')


class Jamos(list):

    # info: Dict[str, Any]

    jamos: List[str]
    true_consonants: List[str]
    consonants: List[str]
    vowels: List[str]

    alternative_consonants: List[str]
    alternative_vowels: List[str]

    has_double_consonant: bool
    has_double_vowel: bool

    def __init__(self, word):
        super().__init__()
        self.jamos = ['!' if x == '' else x for x in decompose_word(word)]
        self.has_double_consonant = any(x in self.jamos for x in total_double_consonants)
        self.has_double_vowel = any(x in self.jamos for x in total_double_vowels)

        self.true_consonants = [x for x in self.jamos if x in total_consonants]
        self.consonants = [x for x in self.jamos if x in total_consonants or x == '!' or x in total_double_consonants]
        self.vowels = [x for x in self.jamos if x in total_vowels]

        self.alternative_vowels = []
        self.alternative_consonants = []

        # self.info = {
        #     'jamos': self.jamos,
        #     'true_consonants': self.true_consonants,
        #     'consonants': self.consonants,
        #     'vowels': self.vowels,
        #     'has_double_consonant': self.has_double_consonant,
        # }

    def __iadd__(self, other):
        self.jamos += other
        return self

    def __iter__(self):
        return iter(self.jamos)

    def __repr__(self):
        # return ''.join(self.jamos)
        return str(self.jamos)


jamos = Jamos(word)

print(f"{jamos=}")


# suggested class method. not sure if it's a good idea
# def checking_settings(j: Jamos):

if ALLOW_PARTIAL_ANAGRAMS:
    print('Partial anagrams allowed!')

    # if any of the elements in total_double_consonants is in jamos

    if jamos.has_double_consonant:
        print('Double consonant detected!')
        # replace the detected double consonants with the alternative consonants
        detected_double_consonants = {k: v for k, v in total_conversion_table.items() if k in jamos.consonants}
        print(f'{detected_double_consonants=}')
        for element in jamos.consonants:
            if element in detected_double_consonants:
                jamos.alternative_consonants.extend(detected_double_consonants[element])
            else:
                jamos.alternative_consonants.append(element)
        print(f'{jamos.consonants=}')
        print(f'{jamos.alternative_consonants=}')

    # if any of the elements in total_double_vowels is in jamos
    if jamos.has_double_vowel:
        print('Double vowel detected!')
        # replace the detected double vowels with the alternative vowels
        detected_double_vowels = {k: v for k, v in total_conversion_table.items() if k in jamos.vowels}
        print(f'{detected_double_vowels=}')
        if len(detected_double_vowels) >= 1:
            for element in jamos.vowels:
                if element in detected_double_vowels:
                    jamos.alternative_vowels.extend(detected_double_vowels[element])
                else:
                    jamos.alternative_vowels.append(element)
        else:
            jamos.alternative_vowels = jamos.vowels
        print(f'{jamos.vowels=}')
        print(f'{jamos.alternative_vowels=}')

    if ALLOW_BATCHIM_CONSONANT_EXCHANGE:
        pass
    if ALLOW_DOUBLE_VOWEL_EXCHANGE:
        pass


# # starting from 2 syllables
# for c1, c2, fc1, fc2 in itertools.permutations(consonants, 4):
#     for v1, v2 in itertools.permutations(vowels, 2):
#         # Form the syllables
#         syllable1 = compose(c1, v1, fc1)
#         syllable2 = compose(c2, v2, fc2)
#
#         # Append to the list of valid syllables
#         valid_syllables.append(syllable1 + syllable2)

def do_anagram(
        jamos: Jamos, num_syllables: int, vowel_perms: List[str], consonant_perms: List[str],
        IS_ALLOW_DOUBLE_CONSONANT_EXCHANGE: bool = False ,
        IS_ALLOW_DOUBLE_VOWEL_EXCHANGE: bool = False,
        IS_ALLOW_PARTIAL_ANAGRAMS: bool = False,
    ) -> List[{str, str}]:

    valid_syllables = []

    for consonant_perm in consonant_perms:
        # skipping when the first consonant is a double consonant or is null
        skip = False
        for i in range(0, len(consonant_perm) - 1, 2):
            if consonant_perm[i] == "!" or consonant_perm[i] in organized['uncommon_double_consontant_batchim'].keys():
                skip = True
                break
            if consonant_perm[i+1] in organized['common_double_consonants'].keys():
                skip = True
                break
        if skip:
            continue

        is_partial_anagram = False

        for vowel_perm in vowel_perms:
            print(f'{vowel_perm=}')
            print(f'{consonant_perm=}')
            syllable = ""

            # determining if the current permutation is a partial anagram
            if [x for x in vowel_perm]+[x for x in consonant_perm] not in jamos and IS_ALLOW_PARTIAL_ANAGRAMS:
                is_partial_anagram = True

            for i in range(num_syllables):
                # if consonant_perm[i*2] == "!" or consonant_perm[i*2] in total_double_consonants:
                #     # skip = True
                #     continue
                # Form the syllable
                # IMPROVED FILTERING ABOVE
                print("SPLITTED : ", consonant_perm[i * 2], vowel_perm[i], consonant_perm[i * 2 + 1])
                if consonant_perm[i * 2 + 1] == "!":
                    syllable += compose(
                        consonant_perm[i * 2],  # Initial consonant
                        vowel_perm[i],  # Vowel
                        ""
                    )
                else:
                    syllable += compose(
                        consonant_perm[i * 2],  # Initial consonant
                        vowel_perm[i],  # Vowel
                        consonant_perm[i * 2 + 1]  # Final consonant
                    )

            # Append to the list of valid syllables
            print("syllable : ", syllable)
            if len(syllable) == num_syllables:
                if IS_ALLOW_PARTIAL_ANAGRAMS and is_partial_anagram and word != syllable:
                    print("adding partial anagram")
                    valid_syllables.append({"syllable": syllable, "is_partial_anagram": is_partial_anagram})
                else:
                    valid_syllables.append({"syllable": syllable, "is_partial_anagram": is_partial_anagram})
            else:
                print("incomplete, skip", syllable)

    return valid_syllables


num_syllables = len(word)
num_consonants_per_syllable = num_syllables * 2  # 2 consonants per syllable (initial and final)
num_vowels_per_syllable = num_syllables  # 1 vowel per syllable (initial and final)

# get all permutations of the vowels and consonants
vowel_perms = get_permutations(jamos.vowels, num_vowels_per_syllable)
consonant_perms = get_permutations(jamos.consonants, num_consonants_per_syllable)
alternative_vowel_perms = get_permutations(jamos.vowels+[x for x in jamos.alternative_vowels if x not in jamos.vowels], num_vowels_per_syllable)
alternative_consontant_perms = get_permutations(jamos.consonants+[x for x in jamos.alternative_consonants if x not in jamos.consonants], num_consonants_per_syllable)

print(f'{alternative_consontant_perms=}')
print(f'{alternative_vowel_perms=}')
# match(???, ???):
#     case (???, ???):

# check if true consonants are odd and if the vowels has duplicates
if len(jamos.true_consonants) % 2 == 1 and len(set(vowel_perms)) != len(vowel_perms):
    vowel_perms = list(set(vowel_perms))
print(f'{vowel_perms=}')

valid_syllables = []

if ALLOW_PARTIAL_ANAGRAMS:
    print("allowing partial anagrams")
    result1 = do_anagram(
        jamos,
        num_syllables,
        alternative_vowel_perms,
        alternative_consontant_perms,
        ALLOW_BATCHIM_CONSONANT_EXCHANGE,
        ALLOW_DOUBLE_VOWEL_EXCHANGE,
        ALLOW_PARTIAL_ANAGRAMS,
    )
    result2 = do_anagram(
        jamos,
        num_syllables,
        vowel_perms,
        consonant_perms,
    )
    for e in sorted(result2+result1, key=lambda x: x['syllable']):
        # print(e)
        if e['syllable'] not in [x['syllable'] for x in valid_syllables]:
            valid_syllables.append(e)

else:
    print("not allowing partial anagrams")
    valid_syllables += do_anagram(
        jamos,
        num_syllables,
        vowel_perms,
        consonant_perms,
    )


'''

'''

''' old code 2
print(" ====== ")
# check if true consonants are odd and if the vowels has duplicates
if len(jamos.true_consonants) % 2 == 1 and len(set(vowel_perms)) != len(vowel_perms):
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
        print(f'{vowel_perm=}')
        syllable = ""

        exist_double_consonant_in_part = True if any(x in consonant_perm for x in total_double_consonants) else False
        print(f'{exist_double_consonant_in_part=}')

        exist_double_vowel_in_part = True if any(x in vowel_perm for x in total_double_vowels) else False
        print(f'{exist_double_vowel_in_part=}')

        exist_batchim_double_consonant_in_part = True if any(x in consonant_perm for x in total_double_consonants) else False
        print(f'{exist_batchim_double_consonant_in_part=}')

        if (exist_double_consonant_in_part or exist_double_vowel_in_part) or (jamos.has_double_consonant or jamos.has_double_vowel):
            is_partial_anagram = True
        else:
            is_partial_anagram = False
        print(f'{is_partial_anagram=}')

        for i in range(num_syllables):
            # if consonant_perm[i*2] == "!" or consonant_perm[i*2] in total_double_consonants:
            #     # skip = True
            #     continue
            # Form the syllable
            # IMPROVED FILTERING ABOVE
            print("SPLITTED : ", consonant_perm[i * 2], vowel_perm[i], consonant_perm[i * 2 + 1])
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

        # Append to the list of valid syllables
        if len(syllable) == num_syllables:
            if ALLOW_PARTIAL_ANAGRAMS:
                if is_partial_anagram and jamos.has_double_consonant:
                    valid_syllables.append(syllable + "* (partial anagram)")
            else:
                if not is_partial_anagram:
                    valid_syllables.append(syllable)

            print("append", syllable)
        else: # this never happens? maybe it does
            print("incomplete, skip", syllable)

    # print(f'{valid_syllables=}') # TODO: add logging
'''

final = []
for e in valid_syllables:
    if e not in final:
        final.append(e)

count = 0
for fi in final:
    # print(fi)
    count += 1
    if fi['is_partial_anagram']:
        print(fi['syllable'] + "*")
    else:
        print(fi['syllable'])

print(count)


""" old file

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
