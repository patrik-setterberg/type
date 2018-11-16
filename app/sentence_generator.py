import random # maybe not required?
from app import app, db
from sqlalchemy.sql.expression import func, select
from sqlalchemy import or_
from app.models import SentenceModel, WordList

VOWELS = ['a', 'e', 'i', 'o', 'u', 'y']


# List of allowed part-of-speech tags
# Based on Brown Corpus part-of-speech tags
# https://en.wikipedia.org/wiki/Brown_Corpus
ALLOWED_TAGS = {
    # nouns
    'NN': 'Singular noun',   
    'NNS': 'Plural noun',
    'NP': 'Proper noun (or name)',

    # verbs
    'VB1': 'Verb base form 1 syllable',
    'VB+': 'Verb base form multiple syllables',
    'VBD': 'Verb past tense simple',
    'VBG': 'Verb, present participle (ing-form)',
    'VBZ': 'Verb 3rd person singular present',

    # adjectives
    'JJ1': 'Adjective 1 syllable',
    'JJ+': 'Adjective more syllables than 1',
    'JJR': 'Adjective comparative',
    'JJT': 'Adjective morphologically superlative',

    # adverbs
    'RB': 'Adverb',
    'RBR': 'Adverb comparative',
    'RBT': 'Adverb superlative',
    'RBPL': 'Adverb of place', # e.g. indoors, outside, everywhere, abroad, here, upstairs
    'RBTM': 'Adverb of time', # e.g. later, yesterday, now, tomorrow
    'RBFR': 'Adverb of frequency', # e.g. often, seldom, rarely, daily, always, never, occasionally, soon

    # numbers, ordinals
    'CD': 'Cardinal numbers', # one, two, 5 etc
    'OD': 'Ordinal numbers', # first, third etc
    
    'IN': 'Preposition',
    'MD': 'Modal auxiliary', # e.g. can, could, may, might, must, ought to, shall, should, will, and would

    # special words
    'BEZ': 'is',
    'BER': 'are',
    'BED': 'were',
    'BEDZ': 'was',
    'HS': 'has',
    'HV': 'have',
    'HVD': 'had',
    'NOT': 'not',
    
    'HE': 'he',
    'SHE': 'she',
    'HIM': 'him',
    'HIS': 'his',
    'HER': 'her',
    'THEY': 'they',
    'THR': 'their',
    'WE': 'we',
    
    'TO': 'to',

    # articles
    'AI': 'article indefinite (a/an)',
    'AD': 'article definite (the)'
}

# maybe also move this?
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


# (incomplete) List of adverbs that don't change
# from their adjective form
# HÄR ÄR NÅGRA
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

WORD_BLACKLIST = []


# Main function
def generate_sentence():

    # get random sentence model from database
    sentence_model = random_sentence_model()
    
    # split model string into array
    model_arr = sentence_model.sentence.split('/')

    sentence = ''

    # loop through model array
    for tag in model_arr:

        # get word
        word = get_word(tag)

        # append word to sentence
        sentence += word + ' '  # hantera sista ordet, dvs mellanslag efter sista ordet kanske inte ska va med


    return sentence.capitalize()[:-1] + '.'


# Get random sentence model from database
def random_sentence_model():

    sentence_model = SentenceModel.query.order_by(func.random()).first()

    return sentence_model


# Ask database for a word, process and return it to main function
def get_word(tag):

    # Get a word from database
    word = random_word(tag)

    # Process VERBs (all verb forms start with V)
    if tag.startswith('V'):
        return process_verb(word.word, word.tag, tag)

    # Process NOUNs
    elif tag.startswith('NN'):
        return process_noun(word.word, tag)

    # Process PROPER NOUNS
    elif tag == 'NP':
        return word.word.capitalize()

    # Process ADJECTIVES
    elif tag.startswith('JJ'):
        return process_adj(word.word, word.tag, tag)

    # Process ADVERBS
    elif tag.startswith('RB'):
        return process_adv(word.word, tag)

    # else just return the word
    else:
        return word.word


# Get random word from database matching part-of-speech tag
def random_word(tag):
    '''
        Some word forms are not stored in database explicitly,
        instead they're stored in base forms and transformed as needed,
        i.e. verbs are stored in infinitive form and conjugated 
        programmatically by process_verb()
    '''
    # Verbs - Get infinitive verb for all verb forms
    # All (and only) verb forms' tags start with 'V'
    if tag.startswith('V'):
        word = WordList.query.filter(or_(WordList.tag == 'VB1', WordList.tag == 'VB+')) \
            .order_by(func.random()).first()
    # Nouns - Get noun base form for all forms (singular and plural)
    elif tag.startswith('NN'):
        word = WordList.query.filter_by(tag='NN').order_by(func.random()).first()
    # Adverbs - Many adverbs are generated from adjectives (JJ)
    elif tag == 'RB' or tag.startswith('JJ'):
        word = WordList.query.filter(or_(WordList.tag == 'JJ1', WordList.tag == 'JJ+')) \
            .order_by(func.random()).first()
    else:
        word = WordList.query.filter_by(tag=tag).order_by(func.random()).first()

    return word


# Process verbs
def process_verb(verb, verb_tag, tag):
    '''
        Gets tempus from tag argument, transforms verb accordingly
        gets verb_tag from database, used for conjugation
        (1 syllable verbs get doubled ending consonants under
        certain conditions...)
        
    '''
    # if requested tag is verb base form (VB), simply return word
    if tag == 'VB':
        return verb
    else:

        # Present 3rd person singular
        if tag == 'VBZ':
            if end_cons_y(verb):
                verb = verb[:-1] + 'i'
                return verb + 'es'
            else:
                return verb + 's'
        else:
            # if last char is consonant and preceded by vowel, double consonant
            if verb[-1] not in VOWELS and verb[-2] in VOWELS:
                # WARNING NOT REALLY GOOD, ALSO HAS TO DO WITH SYLLABLE STRESS
                #  SO BEWARE WHEN ADDING WORDS
                if not verb[-3] in VOWELS and verb_tag == 'VB1':
                    if verb.endswith('c'):
                        verb += 'k'
                    elif verb[-1] not in ['h', 'w', 'x', 'y']:
                        verb += verb[-1]
            # remove last letter if it is 'e'
            elif verb[-1] == 'e' and verb[-2] not in VOWELS:
                verb = verb[:-1]

            if tag == 'VBD':
                if end_cons_y(verb):
                    # if last char is 'y' and preceded by a consonant, replace with 'i'
                    verb = verb[:-1] + 'i' 
                return verb + 'ed'
            # else if will be VBG (present participle)
            else:
                return verb + 'ing'


# Check if last character is 'y' and is preceded by a consonant
def end_cons_y(word):
    if word[-1] == 'y' and word[-2] not in VOWELS:
        return True
    else:
        return False


# Process nouns
def process_noun(noun, tag):
    '''
        Pluralize semi-properly if necessary:
        Handles some exceptions but beware of errors,
        e.g. does not pluralize with 'i' as in
        cactus - cacti
    '''

    # Singular form
    if tag == 'NN':
        return noun

    # Plural form
    elif tag == 'NNS':
        # some nouns don't change in plural form
        if noun in SAME_IN_PLURAL:
            return noun
        # if noun ends in 's', 'sh', 'ch', 'x', or 'z', 
        # add 'es' instead of 's'
        elif noun.endswith('s') or noun.endswith('sh') or \
            noun.endswith('ch') or noun.endswith('x') or \
            noun.endswith('z'):
            return noun + 'es'
        # if noun ends in 'f' or 'fe', usually 'f' is changed
        # to 've' before adding 's'
        elif noun.endswith('f'):
            if noun not in NOUN_EXCEPTIONS:
                noun = noun[:-1]
                return noun + 'ves'
        elif noun.endswith('fe'):
            if noun not in NOUN_EXCEPTIONS:
                return noun[:-2] + 'ves'
        # if last letter is 'y' and preceding letter is a 
        # consonant, replace 'y' with 'i', pluralize with 'es'
        elif end_cons_y(noun):
            noun = noun[:-1]
            return noun + 'ies'
        # if noun ends in 'o', usually pluralize with 'es'
        elif noun.endswith('o') and noun not in NOUN_EXCEPTIONS:
            return noun + 'es'
        # if noun ends in 'on' or 'um', remove and pluralize with 'a',
        # e.g. 'phenomenon' - 'phenomena'
        elif noun.endswith('on') or noun.endswith('um'):
            if noun not in NOUN_EXCEPTIONS:
                noun = noun[:-2]
                return noun + 'a'
            else:
                return noun + 's'
        else:
            return noun + 's'


# Process adjectives
def process_adj(adj, adj_tag, tag):
    '''
        Unlike the other word processing functions, process_adj
        takes adj_tag which is the word's tag in the database, used
        to determine comparative & superlative forms (prefix or suffix)
    '''

    # if base form (positive) is requested, simply return word
    if tag == 'JJ':
        return adj

    # else it will be either comparative (JJR) or superlative (JJT)
    else:
        # set prefix for comparative and superlative forms
        adj_prefix = 'more ' if tag == 'JJR' else 'most '
        adj_suffix = 'er' if tag == 'JJR' else 'est'

        # one syllable adjectives
        if adj_tag == 'JJ1':
            # if word ends in 'e', remove 'e'
            if adj[-1:] == 'e':
                adj = adj[:-1]
            # if word ends in vowel and consonant, double consonant
            elif adj[-1] not in VOWELS and adj[-2] in VOWELS:
                adj += adj[-1]
            # add suffix and return
            return adj + adj_suffix
            
        # two or more syllable adjectives
        elif adj_tag == 'JJ+':
            # if word ends in 'y' replace with 'i'
            if adj.endswith('y'):
                adj = adj[:-1] + 'i'
                # add suffix and return
                return adj + adj_suffix
            # else add prefix ('more ' or 'most ') and return
            else:
                return adj_prefix + adj


# Process adverbs
def process_adv(adv, tag):

    TRANSFORMABLE = ['RB', 'RBR', 'RBT']

    if tag in TRANSFORMABLE and adv not in SAME_AS_ADJ:
        # MAYBE FUNCTION FOR COMMON IRREGULAR ADVERBS?
        # if adv == 'good':
        #     return 'well'
        if end_cons_y(adv):
            adv = adv[:-1] + 'ily'
        elif adv.endswith('le') and adv[-3] not in VOWELS:
            adv = adv[:-1] + 'y'
        elif adv.endswith('ic'):
            if adv == 'public':
                adv += 'ly'
            else:
                adv += 'ally'
        else:
            if not adv.endswith('ly'):
                adv += 'ly'

    # else tag will be RBTM, RBPL or RBFR
    else:
        return adv

    # comparative adverb    
    if tag == 'RBR':
        # either add prefix or suffix
        if adv in SAME_AS_ADJ:
            if adv[-1:] == 'y':
                adv = adv[:-1] + 'i'
            return adv + 'er'
        else:
            return 'more ' + adv
    
    # superlative adverbs
    elif tag == 'RBT':
        if adv in SAME_AS_ADJ:
            if adv[-1:] == 'y':
                adv = adv[:-1] + 'i'
            return adv + 'est'
        else:
            return 'most ' + adv

    # else: RB
    else:
        return adv


# Check if tag is valid, used in WordForm to validate tag field
def check_tag(tag):
    if tag in ALLOWED_TAGS.keys():
        return True
    else:
        return False