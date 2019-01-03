''' Static stuff for sentence_generator '''

VOWELS = ['a', 'e', 'i', 'o', 'u', 'y']


NOUN = 'NN'
PROPER_NOUN = 'NP'
PRONOUN = 'PN'
ADJECTIVE = 'JJ'
VERB = 'VB'
ADVERB = 'RB'
PREPOSITION = 'IN'
CONJUNCTION = 'CN'
CARDINAL = 'CD'
ORDINAL = 'OD'
DEF_ARTICLE = 'AD'
INDEF_ARTICLE = 'AI'
SPECIAL = 'SPEC'


SINGULAR, PLURAL = 'S', 'P'
POSITIVE, COMPARATIVE, SUPERLATIVE = 'P', 'C', 'S'
INHERIT = 'IN'  # ÄNDRA TILL 'INH' ÖVERALLT??? 'IH'?

MALE, FEMALE, NEUTRAL = 'MM', 'FF', 'NN'  # ändra till lowercase för att fixa ambiguity?

INFINITIVE = 'I'
PRESENT_TENSE = 'Z'
PRESENT_PART = 'G'
PAST_TENSE = 'D'
PAST_PART = 'N'  # past participle

# List of common prepositions
PREPOSITIONS = [    
    'of',
    'in',
    'to',
    'for',
    'with',
    'on',
    'at',
    'from',
    'by',
    'about',
    'as',
    'into',
    'like',
    'through',
    'after',
    'over',
    'between',
    'out',
    'against',
    'during',
    'without',
    'before',
    'under',
    'around',
    'among'
]

# List of common conjunctions
CONJUNCTIONS = [
    'and',
    'that',
    'but',
    'or',
    'as',
    'if',
    'when',
    'than',
    'because',
    'while',
    'where',
    'after',
    'so',
    'though',
    'since',
    'until',
    'whether',
    'before',
    'although',
    'like',
    'once',
    'unless',
    'now',
    'except'
]

# Dictionary of valid options for subtags, used for random selection.
TAG_OPTIONS = {
    'NN':{  # Nouns, can be random: singular/plural
        2: ['S', 'P']
    },
    'PN':{  # Pronouns, can be random: singular/plural, 1st/2nd/3rd person, gender
        2: ['S', 'P'],
        3: ['1', '2', '3'],
        4: ['MM', 'FF', 'NN']
    },
    'JJ':{  # Adjectives, can be random: positive/comparative/superlative
        1: ['P', 'C', 'S']
    },
    'RB':{  # Adverbs, can be random: positive/comparative/superlative
        1: ['P', 'C', 'S']
    },
    'CD':{  # Cardinal numbers, can be random: length(1-4)
        1: ['1', '2', '3', '4']
    },
    'IN':{  # Prepositions, get random word from prepositions list
        1: PREPOSITIONS
    },
    'CN':{  # Conjunctions, get random word from conjunctions list
        1: CONJUNCTIONS
    }
}

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

# Common irregular verbs
IRREGULAR_VERBS = {
    """ From: https://www.englisch-hilfen.de/en/grammar/unreg_verben.htm """
    'beat':{
        'D':'beat',
        'N':'beaten'
    },
    'become':{
        'D':'became',
        'N':'become'
    },
    'begin':{
        'D':'began',
        'N':'begun'
    },
    'blow':{
        'D':'blew',
        'N':'blown'
    },
    'break':{
        'D':'broke',
        'N':'broken'
    },
    'bring':{
        'D':'brought',
        'N':'brought'
    },
    'build':{
        'D':'built',
        'N':'built'
    },
    'burst':{
        'D':'burst',
        'N':'burst'
    },
    'buy':{
        'D':'bought',
        'N':'bought'
    },
    'catch':{
        'D':'caught',
        'N':'caught'
    },
    'choose':{
        'D':'chose',
        'N':'chosen'
    },
    'come':{
        'D':'came',
        'N':'come'
    },
    'cost':{
        'D':'cost',
        'N':'cost'
    },
    'cut':{
        'D':'cut',
        'N':'cut'
    },
    'deal':{
        'D':'dealt',
        'N':'dealt'
    },
    'do':{
        'D':'did',
        'N':'done'
    },
    'draw':{
        'D':'drew',
        'N':'drawn'
    },
    'drink':{
        'D':'drank',
        'N':'drunk'
    },
    'eat':{
        'D':'ate',
        'N':'eaten'
    },
    'fall':{
        'D':'fell',
        'N':'fallen'
    },
    'feed':{
        'D':'fed',
        'N':'fed'
    },
    'feel':{
        'D':'felt',
        'N':'felt'
    },
    'fight':{
        'D':'fought',
        'N':'fought'
    },
    'find':{
        'D':'found',
        'N':'found'
    },
    'fly':{
        'D':'flew',
        'N':'flown'
    },
    'forget':{
        'D':'forgot',
        'N':'forgotten'
    },
    'freeze':{
        'D':'froze',
        'N':'frozen'
    },
    'get':{
        'D':'got',
        'N':'gotten'
    },
    '':{
        PAST_TENSE:'',
        PAST_PART:''
    },






    '':{
        'D':'',
        'N':''
    },
}

# cardinal numbers
CARDINALS = {
    1:'one',
    2:'two',
    3:'three',
    4:'four',
    5:'five',
    6:'six',
    7:'seven',
    8:'eight',
    9:'nine',
    10:'ten',
    11:'eleven',
    12:'twelve',
    13:'thirteen',
    14:'fourteen',
    15:'fifteen',
    16:'sixteen',
    17:'seventeen',
    18:'eighteen',
    19:'nineteen',
    20:'twenty',
    30:'thirty',
    40:'forty',
    50:'fifty',
    60:'sixty',
    70:'seventy',
    80:'eighty',
    90:'ninety'
}

# Some ordinal numbers
ORDINALS = [
    'first',
    'second',
    'third',
    'fourth',
    'fifth',
    'sixth',
    'seventh',
    'eighth',
    'ninth',
    'tenth',
    'eleventh',
    'twelfth',
    'thirteenth',
    'fifteenth',
    'sixteenth',
    'seventeenth',
    'eighteenth',
    'nineteenth',
    'twentieth',
    'twenty-first',
    'twenty-second',
    'twenty-third',
    'twenty-fourth',
    'twenty-fifth',
    'forty-second',
    'fiftieth',
    'seventy-fifth',
    'hundredth'
]

# allowed sentence model tag characters
ALLOWED_CHARS = 'A-Za-z0-9$.?'

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
# MAD EDITS REQUIRED
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
# HOW DO WE EVEN
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