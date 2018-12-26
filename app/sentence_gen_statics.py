''' Static stuff for sentence_generator '''

VOWELS = ['a', 'e', 'i', 'o', 'u', 'y']

# PRONOUNS CAN'T CURRENTLY HANDLE PLURAL 'YOU' :(
PRONOUNS = {'I':{
                    'obj':'me',
                    'poss_adj': 'my',
                    'poss_pronoun': 'mine',
                    'reflex': 'myself'
                },
            'you':{
                    'obj':'you',
                    'poss_adj': 'your',
                    'poss_pronoun': 'yours',
                    'reflex': 'yourself'
                }, 
            'he':{
                    'obj':'him',
                    'poss_adj': 'his',
                    'poss_pronoun': 'his',
                    'reflex': 'himself'
                },
            'she':{
                    'obj':'her',
                    'poss_adj': 'her',
                    'poss_pronoun': 'hers',
                    'reflex': 'herself'
                },
            'it':{
                    'obj':'it',
                    'poss_adj': 'its',
                    'poss_pronoun': 'its',  # INACCURATE. doesn't exist. Deal with it?
                    'reflex': 'itself'
                },
            'we':{
                    'obj':'us',
                    'poss_adj': 'our',
                    'poss_pronoun': 'ours',
                    'reflex': 'ourselves'
                },
            'they':{
                    'obj':'them',
                    'poss_adj': 'their',
                    'poss_pronoun': 'theirs',
                    'reflex': 'themselves'
                }
            }

# allowed sentence model tag characters
ALLOWED_CHARS = 'A-Za-z0-9\$.'

# Add words to WordList, tags allowed
WORDLIST_TAGS_ALLOWED = {

    'NN': 'Noun',

    'NP': 'Proper noun',

    'JJ': 'Adjective',

    'VB': 'Verb',

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
    'BUT': 'but'
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