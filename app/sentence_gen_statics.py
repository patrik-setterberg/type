''' Static stuff for sentence_generator '''

VOWELS = ['a', 'e', 'i', 'o', 'u', 'y']


# Add words to WordList, tags allowed
WORDLIST_TAGS_ALLOWED = {
    # Nouns
    'NN': 'Noun, singular',
    'NNS': 'Noun, plural',

    # Proper nouns
    'NPM': 'Proper noun, male',
    'NPF': 'Proper noun, female',
    'NPN': 'Proper noun, neutral',  # e.g. cities, countries

    # Adjectives
    'JJ1': 'Adjective, one syllable',
    'JJ+': 'Adjective, more than one syllable',

    # Verbs
    'VB1': 'Verb, one syllable',
    'VB+': 'Verb, more than one syllable',

    # Adverbs
    'RBPL': 'Adverb of place', # e.g. indoors, outside, everywhere, abroad, here, upstairs
    'RBTM': 'Adverb of time', # e.g. later, yesterday, now, tomorrow
    'RBFR': 'Adverb of frequency', # e.g. often, seldom, rarely, daily, always, never, occasionally, soon

    # Numbers, ordinals
    'CD': 'Cardinal numbers', # one, two, 5 etc
    'OD': 'Ordinal numbers', # first, third etc

    # Modal auxiliiaries
    'MD': 'Modal auxiliary', # e.g. can, could, may, might, must, ought to, shall, should, will, and would

    # Prepositions
    'IN': 'Preposition',

    # Articles
    'AI': 'Indefinite article (a/an)',
    'AD': 'Definite article'
}


# Add sentence model, tags allowed
MODEL_TAGS_ALLOWED = {
    # Nouns
    'NN': 'Noun, singular',
    'NN$': 'Noun, singular, possessive',
    'NNS': 'Noun, plural',
    'NNS$': 'Noun, plural, possessive',

    # Proper nouns
    'NPM': 'Proper noun, male',
    'NPM$': 'Proper noun, male, possessive',
    'NPF': 'Proper noun, female',
    'NPF$': 'Proper noun, female, possessive',
    'NPN': 'Proper noun, neutral',
    'NPN$': 'Proper noun, neutral, possessive',

    # Adjectives
    'JJ': 'Adjective, base (positive) form',
    'JJR': 'Adjective, comparative form',
    'JJT': 'Adjective, superlative form (morphologically)',

    # Verbs
    'VB': 'Verb, base form (also 3rd pers. plural, present)',
    'VBZ': 'Verb, 3rd pers. singular, present',
    'VBD': 'Verb, simple past tense',
    'VBG': 'Verb, present participle',

    # Adverbs
    'RB': 'Adverb', # ALSO ALLOW IN WORDLIST???
    'RBR': 'Adverb, comparative',
    'RBT': 'Adverb, superlative',
    'RBPL': 'Adverb of place', # e.g. indoors, outside, everywhere, abroad, here, upstairs
    'RBTM': 'Adverb of time', # e.g. later, yesterday, now, tomorrow
    'RBFR': 'Adverb of frequency', # e.g. often, seldom, rarely, daily, always, never, occasionally, soon

    # Numbers, ordinals
    'CD': 'Cardinal numbers', # one, two, 5 etc
    'OD': 'Ordinal numbers', # first, third etc

    # Modal auxiliaries
    'MD': 'Modal auxiliary', # e.g. can, could, may, might, must, ought to, shall, should, will, and would

    # Prepositions
    'IN': 'Preposition',

    # Articles
    'AI': 'Indefinite article (a/an)',
    'AD': 'Definite article (the)'
}


# Special words need not be stored in database
SPECIAL_WORDS = {
    'BEZ': 'is',
    'BER': 'are',
    'BED': 'were',
    'BEDZ': 'was',
    'HS': 'has',
    'HV': 'have',
    'HVD': 'had',
    'NOT': 'not',
    'TO': 'to',
    'OF': 'of',
    'BUT': 'but',

    # Pronouns
    'I': 'I',
    'ME': 'me',
    'YOU': 'you',
    'YOUR': 'your',
    'HE': 'he',
    'HIM': 'him',
    'HIS': 'his',
    'SHE': 'she',
    'HER': 'her',
    'HERS': 'hers',
    'THEY': 'they',
    'THEM': 'them',
    'THR': 'their',
    'WE': 'we',
    'OUR': 'our',
    'IT': 'it',
    'ITS': 'its'
}


# (incomplete) List of exceptions to grammatical rules, processed differently
NOUN_EXCEPTIONS = [
    'reef',
    'roof',
    'belief',
    'chef',
    'chief',
    'photo',
    'piano',
    'halo',
    'spoon',
    'moon',
    'zero'
]


# (incomplete) List of nouns that don't change in plural form
SAME_IN_PLURAL = [
    'aircraft',
    'hovercraft',
    'spacecraft',
    'cod',
    'fish',
    'deer',
    'offspring',
    'moose',
    'salmon',
    'sheep',
    'shrimp',
    'swine',
    'trout',
    'buffalo'
]


# (incomplete) List of adverbs that don't change from their adjective form
###### OBS ###### # HÄR ÄR NÅGRA
# https://www.englisch-hilfen.de/en/grammar/adverbien2.htm
SAME_AS_ADJ = [
    'early',
    'fast',
    'hard',
    'high',
    'late',
    'long',
    'low',
    'near',
    'soon',
    'straight',
    'wrong'
]


# Words that don't play well with sentence generator, probably due to poor 
# implementation of e.g. verb conjugation, but possibly also due to weird 
# exceptions to grammatical rules or peculiarities of the English language
WORD_BLACKLIST = []