""" Static stuff for sentence_generator.py """

VOWELS = ['a', 'e', 'i', 'o', 'u', 'y']

NOUN = 'NN'
PROPER_NOUN = 'NP'
PRONOUN = 'PN'
ADJECTIVE = 'JJ'
VERB = 'VB'
ADVERB = 'RB'
PREPOSITION = 'IN'
CONJUNCTION = 'CN'
MOD_AUX = 'MD'  # Modal auxiliary
CARDINAL = 'CD'
ORDINAL = 'OD'
DEF_ARTICLE = 'AD'
INDEF_ARTICLE = 'AI'
SPECIAL = 'SPEC'

SINGULAR, PLURAL = 'S', 'P'
POSITIVE, COMPARATIVE, SUPERLATIVE = 'P', 'C', 'S'
INHERIT = 'IN'
MALE, FEMALE, NEUTRAL = 'MM', 'FF', 'NN'

INFINITIVE = 'I'
PRESENT_TENSE = 'Z'
PRESENT_PART = 'G'
PAST_TENSE = 'D'
PAST_PART = 'N'  # past participle
PAST_CONT = 'C'  # past continuous
FUTURE = 'F'

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

# Common modal auxiliaries.
MOD_AUXS = [
    'can',
    'could',
    'may',
    'might',
    'must',
    'shall',
    'should',
    'will',
    'would'
]

# Dictionary of valid options for subtags, used for random selection.
TAG_OPTIONS = {
    # Nouns, can be random: singular/plural
    NOUN:{
        2: [SINGULAR, PLURAL]
    },
    # Pronouns, can be random: singular/plural, 1st/2nd/3rd person 
    # and gender
    PRONOUN:{  
        2: [SINGULAR, PLURAL],
        3: ['1', '2', '3'],
        4: [MALE, FEMALE, NEUTRAL]
    },
    # Proper nouns, can be random: gender - male/female
    PROPER_NOUN:{
        2: [MALE, FEMALE]
    },
    # Adjectives, can be random: 
    # positive/comparative/superlative
    ADJECTIVE:{  
        1: [POSITIVE, COMPARATIVE, SUPERLATIVE]
    },
    # Adverbs, can be random: 
    # positive/comparative/superlative
    ADVERB:{
        1: [POSITIVE, COMPARATIVE, SUPERLATIVE]
    },
    # Cardinal numbers, can be random: length(1-4)
    CARDINAL:{
        1: ['1', '2', '3', '4']
    },
    # Prepositions, get random word from prepositions list
    PREPOSITION:{
        1: PREPOSITIONS
    },
    # Conjunctions, get random word from conjunctions list
    CONJUNCTION:{
        1: CONJUNCTIONS
    },
    # Modal auxiliaries, get random word from mod aux list
    MOD_AUX:{
        1: MOD_AUXS
    }
}

# Pronouns and their forms
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
                    'poss_pronoun': 'its',  # INACCURATE
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

# Common irregular verbs. From: 
# https://www.englisch-hilfen.de/en/grammar/unreg_verben.htm
IRREGULAR_VERBS = {
    'beat':{
        PAST_TENSE:'beat',
        PAST_PART:'beaten'
    },
    'become':{
        PAST_TENSE:'became',
        PAST_PART:'become'
    },
    'begin':{
        PAST_TENSE:'began',
        PAST_PART:'begun'
    },
    'blow':{
        PAST_TENSE:'blew',
        PAST_PART:'blown'
    },
    'break':{
        PAST_TENSE:'broke',
        PAST_PART:'broken'
    },
    'bring':{
        PAST_TENSE:'brought',
        PAST_PART:'brought'
    },
    'build':{
        PAST_TENSE:'built',
        PAST_PART:'built'
    },
    'burst':{
        PAST_TENSE:'burst',
        PAST_PART:'burst'
    },
    'buy':{
        PAST_TENSE:'bought',
        PAST_PART:'bought'
    },
    'catch':{
        PAST_TENSE:'caught',
        PAST_PART:'caught'
    },
    'choose':{
        PAST_TENSE:'chose',
        PAST_PART:'chosen'
    },
    'come':{
        PAST_TENSE:'came',
        PAST_PART:'come'
    },
    'cost':{
        PAST_TENSE:'cost',
        PAST_PART:'cost'
    },
    'cut':{
        PAST_TENSE:'cut',
        PAST_PART:'cut'
    },
    'deal':{
        PAST_TENSE:'dealt',
        PAST_PART:'dealt'
    },
    'do':{
        PAST_TENSE:'did',
        PAST_PART:'done'
    },
    'draw':{
        PAST_TENSE:'drew',
        PAST_PART:'drawn'
    },
    'drink':{
        PAST_TENSE:'drank',
        PAST_PART:'drunk'
    },
    'eat':{
        PAST_TENSE:'ate',
        PAST_PART:'eaten'
    },
    'fall':{
        PAST_TENSE:'fell',
        PAST_PART:'fallen'
    },
    'feed':{
        PAST_TENSE:'fed',
        PAST_PART:'fed'
    },
    'feel':{
        PAST_TENSE:'felt',
        PAST_PART:'felt'
    },
    'fight':{
        PAST_TENSE:'fought',
        PAST_PART:'fought'
    },
    'find':{
        PAST_TENSE:'found',
        PAST_PART:'found'
    },
    'fly':{
        PAST_TENSE:'flew',
        PAST_PART:'flown'
    },
    'forget':{
        PAST_TENSE:'forgot',
        PAST_PART:'forgotten'
    },
    'freeze':{
        PAST_TENSE:'froze',
        PAST_PART:'frozen'
    },
    'get':{
        PAST_TENSE:'got',
        PAST_PART:'gotten'
    },
    'give':{
        PAST_TENSE:'gave',
        PAST_PART:'given'
    },
    'go':{
        PAST_TENSE:'went',
        PAST_PART:'gone'
    },
    'grown':{
        PAST_TENSE:'grew',
        PAST_PART:'grown'
    },
    'hang':{
        PAST_TENSE:'hung',
        PAST_PART:'hung'
    },
    'have':{
        PAST_TENSE:'had',
        PAST_PART:'had'
    },
    'hear':{
        PAST_TENSE:'heard',
        PAST_PART:'heard'
    },
    'hide':{
        PAST_TENSE:'hid',
        PAST_PART:'hidden'
    },
    'hit':{
        PAST_TENSE:'hit',
        PAST_PART:'hit'
    },
    'hold':{
        PAST_TENSE:'held',
        PAST_PART:'held'
    },
    'hurt':{
        PAST_TENSE:'hurt',
        PAST_PART:'hurt'
    },
    'keep':{
        PAST_TENSE:'kept',
        PAST_PART:'kept'
    },
    'know':{
        PAST_TENSE:'knew',
        PAST_PART:'known'
    },
    'lead':{
        PAST_TENSE:'led',
        PAST_PART:'led'
    },
    'leave':{
        PAST_TENSE:'left',
        PAST_PART:'left'
    },
    'lie':{
        PAST_TENSE:'lay',
        PAST_PART:'lain'
    },
    'light':{
        PAST_TENSE:'lit',
        PAST_PART:'llit'
    },
    'lose':{
        PAST_TENSE:'lost',
        PAST_PART:'lost'
    },
    'make':{
        PAST_TENSE:'made',
        PAST_PART:'made'
    },
    'mean':{
        PAST_TENSE:'meant',
        PAST_PART:'meant'
    },
    'meet':{
        PAST_TENSE:'met',
        PAST_PART:'met'
    },
    'pay':{
        PAST_TENSE:'paid',
        PAST_PART:'paid'
    },
    'put':{
        PAST_TENSE:'put',
        PAST_PART:'put'
    },
    'read':{
        PAST_TENSE:'read',
        PAST_PART:'read'
    },
    'ride':{
        PAST_TENSE:'rode',
        PAST_PART:'ridden'
    },
    'ring':{
        PAST_TENSE:'rang',
        PAST_PART:'rung'
    },
    'rise':{
        PAST_TENSE:'rose',
        PAST_PART:'risen'
    },
    'run':{
        PAST_TENSE:'ran',
        PAST_PART:'run'
    },
    'say':{
        PAST_TENSE:'said',
        PAST_PART:'said'
    },
    'see':{
        PAST_TENSE:'saw',
        PAST_PART:'seen'
    },
    'sell':{
        PAST_TENSE:'sold',
        PAST_PART:'sold'
    },
    'send':{
        PAST_TENSE:'sent',
        PAST_PART:'sent'
    },
    'shake':{
        PAST_TENSE:'shook',
        PAST_PART:'shaken'
    },
    'steal':{
        PAST_TENSE:'stole',
        PAST_PART:'stolen'
    },
    'shine':{
        PAST_TENSE:'shone',
        PAST_PART:'shone'
    },
    'shoot':{
        PAST_TENSE:'shot',
        PAST_PART:'shot'
    },
    'sing':{
        PAST_TENSE:'sang',
        PAST_PART:'sung'
    },
    'sink':{
        PAST_TENSE:'sank',
        PAST_PART:'sunk'
    },
    'sit':{
        PAST_TENSE:'sat',
        PAST_PART:'sat'
    },
    'sleep':{
        PAST_TENSE:'slept',
        PAST_PART:'slept'
    },
    'speak':{
        PAST_TENSE:'spoke',
        PAST_PART:'spoken'
    },
    'stand':{
        PAST_TENSE:'stood',
        PAST_PART:'stood'
    },
    'swear':{
        PAST_TENSE:'swore',
        PAST_PART:'sworn'
    },
    'swim':{
        PAST_TENSE:'swam',
        PAST_PART:'swum'
    },
    'take':{
        PAST_TENSE:'took',
        PAST_PART:'taken'
    },
    'teach':{
        PAST_TENSE:'taught',
        PAST_PART:'taught'
    },
    'tear':{
        PAST_TENSE:'torn',
        PAST_PART:'torn'
    },
    'tell':{
        PAST_TENSE:'told',
        PAST_PART:'told'
    },
    'think':{
        PAST_TENSE:'thought',
        PAST_PART:'thought'
    },
    'throw':{
        PAST_TENSE:'threw',
        PAST_PART:'thrown'
    },
    'understand':{
        PAST_TENSE:'understood',
        PAST_PART:'understood'
    },
    'wake':{
        PAST_TENSE:'woke',
        PAST_PART:'woken'
    },
    'wear':{
        PAST_TENSE:'worn',
        PAST_PART:'worn'
    },
    'win':{
        PAST_TENSE:'won',
        PAST_PART:'won'
    },
    'write':{
        PAST_TENSE:'wrote',
        PAST_PART:'written'
    }
}

# Forms of word 'be'
BE = {
    NOUN: {
        PRESENT_TENSE: {
            SINGULAR: 'is',
            PLURAL: 'are'
        },
        PAST_TENSE: {
            SINGULAR: 'was',
            PLURAL: 'were'
        }
    },
    PROPER_NOUN: {
        PRESENT_TENSE: 'is',
        PAST_TENSE: 'was'
    },
    PRONOUN: {
        'I': {
            PRESENT_TENSE: 'am',
            PAST_TENSE: 'was'
        },
        'you': {
            PRESENT_TENSE: 'are',
            PAST_TENSE: 'were'
        },
        'he': {
            PRESENT_TENSE: 'is',
            PAST_TENSE: 'was'
        },
        'she': {
            PRESENT_TENSE: 'is',
            PAST_TENSE: 'was'
        },
        'it': {
            PRESENT_TENSE: 'is',
            PAST_TENSE: 'was'
        },
        'we': {
            PRESENT_TENSE: 'are',
            PAST_TENSE: 'were'
        },
        'they': {
            PRESENT_TENSE: 'are',
            PAST_TENSE: 'were'
        }
    }
}

# Cardinal numbers
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

# Allowed sentence model tag characters
ALLOWED_CHARS = 'A-Za-z0-9$.?'

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

# (incomplete) List of adverbs that don't change from their 
# adjective form. Some here: 
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

# Words that don't play well with sentence generator, probably due to
# poor implementation of e.g. verb conjugation, but possibly also due 
# to weird exceptions to grammatical rules or peculiarities of the 
# English language
WORD_BLACKLIST = []