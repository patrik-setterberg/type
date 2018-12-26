import random 
from app import app, db
from sqlalchemy.sql.expression import func, select
from sqlalchemy import or_
from app.models import SentenceModel, WordList
from app.sentence_gen_statics import VOWELS, PRONOUNS, NOUN_EXCEPTIONS, SAME_IN_PLURAL, SAME_AS_ADJ
from app.sentence_gen_statics import WORDLIST_TAGS_ALLOWED, MODEL_TAGS_ALLOWED
from app.sentence_gen_statics import WORD_BLACKLIST, SPECIAL_WORDS


'''
    sentence_generator.py
    A sentence generator that generates pseudo-random sentences from sentence models.
    Words as well as sentence models are saved manually in database tables and later
    retrieved for sentence generation.

    Sentence models consist of tags, for the most part parts-of-speech or word 
    classes, based on The Brown University Standard Corpus of Present-Day American 
    English (https://en.wikipedia.org/wiki/Brown_Corpus) but customized to fit
    application, see sentence_gen_statics.py for full list of tags.
    

    Notes on usage:
    * Save words and their tags in database in all lowercase, even proper nouns
    such as people's names (capitalized automatically by program).

    * Save only words in their base form (nouns in singular, verbs in infinitive form).
    
    * Don't save regular adverbs (handled by program).
    
    * Don't save pronouns (handled by program).
    
    * Extra care is required when saving ADJECTIVES and VERBS. Correct transformation
    of certain of these requires knowing the number of syllables the word has,
    specifically if the word has one syllable or if it has more than one syllable.
    Inform program of this by adding '1' for one or '+' for more than one syllable
    to words' tags, e.g. 'VB+' for a verb with more than one syllable or 'JJ1' for
    an adjective with one syllable. Note that this is only required when saving new
    words in database, not when constructing and storing new sentence models.
    
    * Save sentence models in format: TAG/TAG/TAG/TAG..., e.g. 'NN/BEZ/JJ' which 
    translates to 'noun/is/adjective' which could, if the words are saved in database
    generate e.g. 'cake/is/delicious' -> Cake is delicious.
    
    * English is full of exceptions. Some of these are handled by the program. For
    example, some nouns (e.g. 'deer') is the same in plural (not 'deers'), some 
    adverbs look the same as their adjective counterparts (e.g. 'late' in 
    'I will be late', not 'I will be lately'). A number of these exceptions are stored
    in sentence_gen_statics.py. If you discover more words that don't look right
    when chewed by the generator, see if they fit in any of the exceptions lists
    or add them to the blacklist.

    * Not all word forms are saved explicitly in database:
        * Nouns are only saved in singular form, plural form is generated by 
          process_noun().
        * Adjectives are stored in base (positive) form only. Their comparative
          and superlative forms are generated by process_adj()
        * Verbs are stored in their base (infinitive) form and conjugated as needed 
          by process_verb().
        * Regular adverbs are not stored but instead generated from their adjective
          versions. Certain adverbs are stored, however, such as adverbs of place,
          e.g. 'indoors'.
        * Some special words are stored in a dictionary in sentence_gen_statics.py,
          they include pronouns and forms of 'be' and 'have'.

    * Sentence_generator aims to be able to generate grammatically correct sentences
    but it has several limitations and might fail. If a word is misbehaving,
    it can be added to WORD_BLACKLIST and forbidden from future entry. Current
    limitations, possibly subject to change include:
        * Program is limited to regular verbs. Entered irregular verbs
          will not conjugate correctly.
        * Program has no semantic component, i.e. sentences will probably not make
          any sense.
        * Pronouns are handled poorly. Program has no way of knowing who or what
          the pronoun is referring to, and therefore it can't know what gender
          pronoun to select.
        * Fails to pluralize certain nouns (ending in -i in plural, e.g.
          cactus - cacti)
'''


class Sentence:
    ''' Creates new sentence object. Actual sentence is a list (self.sentence)
        of word objects accessible through self.sentence[index].word (I THINK) '''

    def __init__(self, model):
        # gets model as string, convert to list
        self.mod_list = model.split('/')
    

        # store subject, verb, object indices in dictionary
        self.SVO_ind = self.get_SVO_ind(self.mod_list)

        # /hmm, kanske najs?
        # self.SUBJECT = SVO_ind['subj']
        # self.VERB = SVO_ind['verb']
        # self.OBJECT = SVO_ind['obj']

        # make sure there's a subject
        # if self.SVO_ind['subj'] == None:
        #     # RAISE HELL
        #     pass

        # initialize sentence
        self.sentence = list('x' * len(self.mod_list))
        
        # get subject
        self.sentence[self.SVO_ind['subj']] = self.get_word(self.mod_list[self.SVO_ind['subj']])

        # get verb
        self.sentence[self.SVO_ind['verb']] = self.get_word(self.mod_list[self.SVO_ind['verb']])
            
        # get object
        if 'obj' in self.SVO_ind.keys():
            self.sentence[self.SVO_ind['obj']] = self.get_word(self.mod_list[self.SVO_ind['obj']])

        # initialize list of indefinite article indices
        self.ai_inds = []

        # get rest of words
        for i in range(len(self.sentence)):
            if self.sentence[i] == 'x':

                # get indefinite article index
                if self.mod_list[i].split('.')[0] == 'AI':
                    self.ai_inds.append(i)
                # else get a word
                else:
                    self.sentence[i] = get_word(self.mod_list[i])

        # get any indefinite articles
        if self.ai_inds:
            for ind in self.ai_inds:
                self.sentence[ind] = self.get_indef_article(ind)

        # try to get an object:
            # check if verb is associated with any categories:
                # get object from category 
                # (e.g.) if verb is "eat" and object is a noun, select random
                # noun from nouns with category tag "food"
            # else just get an object
        
        # if we need adjectives, check what word it serves to describe, see if
        # that word has any associations that might be relevant, then possibly
        # get fitting adjective (from right category)

        # maybe something similar for adverbs?

        # get remaining words



    def get_SVO_ind(self, tag_list):
        ''' create a dictionary storing indices of subject, verb, object '''
        
        indices = {}

        for tag in tag_list:
            if 's' in tag:
                indices['subj'] = tag_list.index(tag)
            elif 'o' in tag:
                indices['obj'] = tag_list.index(tag)
            elif tag.startswith('VB'):
                indices['verb'] = tag_list.index(tag)
        
        return indices


    def get_word(self, tag):

        get_func_dict = {
            'NN': self.get_noun,
            'NP': self.get_proper_noun,     # FINNS E J  ÄNNU
            'PN': self.get_pronoun,
            'JJ': self.get_adj,             # SAMMA
            'VB': self.get_verb,
            'RB': self.get_adv,             # MMMMmmmm
            # NUMBERS, ORDINALS
            # PREPOSITIONS
            # CONJUNCTIONS
            # ALLA SÅNNA HÄR FÅR BLI SINA EGNA WordList-objects som inte committas bara
            'AD': self.get_def_article,
            # 'AI': self.get_indef_article,
            'SPEC': self.get_spec
        }

        word = get_func_dict[tag.split('.')[0]](tag)

        return word
        

    def get_verb(self, tag):
        ''' Get a verb from database, conjugate it properly and return it.
                
            Verb sentence model rules:
            0: Always 'VB' 
            1: 'I', 'Z', 'D', 'G'
            2: TYPE KANSKE? ACTION, 
            '''            

        tags = tag.split('.')

        verb = (WordList.query
            .filter_by(tag=tags[0])
            .order_by(func.random()).first())

        # if not infinitive form, conjugate
        if tags[1] != 'I':
            verb.word = self.conjugate(verb.word, tags[1])

        # IRREGULAR VERBS???

        return verb

    
    def conjugate(self, verb, tag):
        ''' Conjugate and return correct form of verb. '''

        # Present 3rd person singular
        if tag == 'Z':
            if self.end_cons_y(verb):
                verb = verb[:-1] + 'i'
                return verb + 'es'
            else:
                return verb + 's'
        
        # Else either past tense or present participle
        else:
            # if last char is consonant and preceded by vowel, double consonant
            if verb[-1] not in VOWELS and verb[-2] in VOWELS:
                # WARNING NOT REALLY GOOD, ALSO HAS TO DO WITH SYLLABLE STRESS
                #  SO BEWARE WHEN ADDING WORDS
                if not verb[-3] in VOWELS and verb.mult_syll == '0':
                    if verb.endswith('c'):
                        verb += 'k'
                    elif verb[-1] not in ['h', 'w', 'x', 'y']:
                        verb += verb[-1]
            # remove last letter if it is 'e'
            elif verb[-1] == 'e' and verb[-2] not in VOWELS:
                verb = verb[:-1]
            
            # past tense
            if tag == 'D':
                if self.end_cons_y(verb):
                    # if last char is 'y' and preceded by a consonant, replace with 'i'
                    verb = verb[:-1] + 'i' 
                return verb + 'ed'
            
            # else it will be 'G' (present participle)
            else:
                return verb + 'ing'


    def get_noun(self, tag):
        ''' Get a noun word object from database, check if it needs to be pluralized
            or transformed for possession and then return it.
            
            Noun sentence model rules:
            0: Always 'NN'
            1: 's', 'o', '$', 'n'   # subject, object, possessive, neutral
            2: 'S', 'P'             # singular, plural '''


        tags = tag.split('.')

        noun = (WordList.query.filter_by(tag=tags[0])
                              .order_by(func.random()).first())

        # pluralize
        if tags[2] == 'P':
            noun.word = self.pluralize(noun.word)

        # handle possessive case
        if tags[1] == '$':
             noun.word += "'" if noun.word[-1] == 's' else "'s"

        return noun


    def pluralize(self, noun):
        ''' Find and return proper plural form for noun '''

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
        elif self.end_cons_y(noun):
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

        # if nothing funky is going on, pluralize by just adding 's'
        else:
            return noun + 's'


    def end_cons_y(self, word):
        ''' Check if last character is 'y' and is preceded by a consonant '''

        if word[-1] == 'y' and word[-2] not in VOWELS:
            return True
        else:
            return False


    def get_proper_noun(self, tag):
        """ Create proper noun object. 
            Get a word, transform for possession if needed and return
            
            proper noun sentence model rules:
            0: Always 'NP'
            1: 's', 'o', '$', 'n'   # subject, object, possessive, neutral """

        proper_noun = (WordList.query.filter_by(tag=tag.split('.')[0])
                                     .order_by(func.random()).first())

        # handle possessive case
        if tag.split('.')[1] == '$':
             proper_noun.word += "'" if proper_noun.word[-1] == 's' else "'s"

        return proper_noun

                
    def get_pronoun(self, tags):
        """ Pronouns aren't stored in database. Instead they're statically stored 
            in application (sentence_gen_statics.py), in nested dictionary form.

            First get base pronoun, then figure out the correct form.
        
            Pronoun sentence model rules:
            0: Always 'PN'                          
            1: 's', 'o', 'ref_s', 'ref_o', 'reflex' # subject, object or referencing them (actually called possessive adjective and possessive pronouns) and reflexive
            2: 'S', 'P', 'IN'                       # singular or plural, inherit (IN)
            3: '1', '2', '3', 'IN'                  # first, second or third person or inherit
            4: 'MM', 'FF', 'NN', 'IN'               # gender or inherit """


        # establish base pronoun
        pronoun = self.get_base_pronoun(tags)

        # get correct form
        if tags[1] == 'o':
            pronoun.word = PRONOUNS[pronoun.word]['obj']
        elif tags[1] == 'ref_s':
            pronoun.word = PRONOUNS[pronoun.word]['poss_adj']
        elif tags[1] == 'ref_o':
            pronoun.word = PRONOUNS[pronoun.word]['poss_pronoun']
        elif tags[1] == 'reflex':
            pronoun.word = PRONOUNS[pronoun.word]['reflex']

        # ? == RANDOM???????????????????

        return pronoun

    def get_base_pronoun(self, tags):

        pronoun = WordList(word='', gender='NN', tag='PN')

        # if referencing a word, get that word object
        if tags[1] == 'ref_s':
            ref = self.sentence[SVO_ind['subj']]
        elif tags[1] == 'ref_o':
            ref = self.sentence[SVO_ind['obj']]

        # check inheritance
        if tags[2] == 'IN':
            # Inherit
            pronoun = self.inherit_pronoun(tags, ref, pronoun)

        # singular, i.e. I, you, he, she, it
        elif tags[2] == 'S':
            # first person
            if tags[3] == '1':
                pronoun.word = 'I'
            # second person
            elif tags[3] == '2':
                pronoun.word = 'you'
            # third person
            else:
                # male
                if tags[4] == 'MM':
                    pronoun.word = 'he'
                    pronoun.gender = 'MM'
                # female
                elif tags[4] == 'FF':
                    pronoun.word = 'she'
                    pronoun.gender = 'FF'
                # neutral
                else:
                    pronoun.word == 'it'                

        # plural, i.e. either we, you, they
        elif tags[2] == 'P':
            # first person
            if tags[3] == '1':
                pronoun.word = 'we'
            # second person
            elif tags[3] == '2':
                pronoun.word = 'you'
            # third person
            else:
                pronoun.word = 'they'

        # default to random
        else:
            pronoun.word = random.choice(PRONOUNS.keys())

            if pronoun.word == 'he':
                pronoun.gender = 'MM'
            elif pronoun.word == 'she':
                pronoun.gender = 'FF'

        return pronoun


    def inherit_pronoun(self, tags, ref, pronoun):
        ''' First checks if referenced word is a pronoun. If it is, return it.
            If it isn't a pronoun, it will be either a proper noun or a noun,
            so a gender check will suffice to select proper pronoun. If not
            male or female, function defaults to neutral, i.e. 'it'. '''

        if ref.word in PRONOUNS.keys():
            pronoun.word = ref.word
            pronoun.gender = ref.gender
        elif ref.gender == 'MM':
            pronoun.word = 'he'
            pronoun.gender = 'MM'
        elif ref.gender == 'FF':
            pronoun.word = 'she'
            pronoun.gender = 'FF'
        else:
            pronoun.word = 'it'
            pronoun.gender = 'NN'

        return pronoun


    def get_adj(self, tag):
        """ Adjective object
        
            Sentence model rules:
            0: 'JJ'
            1: 'P', 'C', 'S'                # positive, comparative, superlative
            2: 'ref_s', 'ref_o', 'ref_n'    # describing subject, object, neutral """

        tags = tag.split('.')

        adj = (WordList.query.filter_by(tag=tags[0])
                        .order_by(func.random()).first())

        return adj

    
    def get_def_article(self, tag):
        """ Create word object for definite article, i.e. 'the'. """

        article = WordList(tag=tag, word='the')

        return article


    def get_indef_article(self, i):
        """ Create indefinite article object and choose the right one """

        article = WordList(tag='AI')

        # if next word is noun, get its article
        if self.sentence[i].tag == 'NN':
            article.word = self.sentence[i].article
        # else check if next word starts with a vowel (not great solution but oh well)
        elif self.sentence[i+1].word[0] in VOWELS:
            article.word = 'an'
        # default to 'a'
        else:
            article.word = 'a'

        return article

    
    def get_spec(self, tag):
        """ Special words function simply sets second subtag to word and
            returns object.
            
            Rules:
            0: 'SPEC'
            1: any word """

        tags = tag.split('.')
        special_word = WordList(tag=tags[0], word=tags[1])
        return special_word


# Main function
def generate_sentence():

    # get random sentence model from database
    sentence_model = random_sentence_model()

    # create new sentence object 
    new_sentence = Sentence(sentence_model.sentence)

    # return sentence (list of word objects)
    return new_sentence.sentence


# Get random sentence model from database
def random_sentence_model():
    sentence_model = SentenceModel.query.order_by(func.random()).first()
    return sentence_model


# Ask database for a word, process and return it to main function
def get_word(tag):

    # First check if word is in hardcoded special
    # words list or is a hardcoded PRONOUN
    if tag in SPECIAL_WORDS:
        return SPECIAL_WORDS[tag]
    else:
        # Get a word from database
        word = random_word(tag)
   
    # Process VERBs (all verb forms start with V)
    if tag.startswith('V'):
        return process_verb(word.word, word.tag, tag)

    # Process NOUNs
    elif tag.startswith('NN'):
        return process_noun(word.word, tag)

    # Process PROPER NOUNS
    elif tag.startswith('NP'):
        word = word.word.capitalize()
        # possessive
        if tag[-1] == '$':
            word = word + "'" if word.endswith('s') else word + "'s"
        return word
    
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
    
    # Proper nouns
    elif tag.startswith('NP'):
        # remove '$' if present
        NP_tag = tag[:-1] if tag.endswith('$') else tag
        word = WordList.query.filter_by(tag=NP_tag).order_by(func.random()).first()
    
    # if no special tense or anything is required, just query using tag argument
    else:
        word = WordList.query.filter_by(tag=tag).order_by(func.random()).first()

    # return word object
    return word


'''
# Process nouns
def process_noun(noun, tag):
    
    # Singular form
    if tag == 'NN':
        return noun
    
    # Singular possessive
    elif tag == 'NN$':
        return noun + "'" if noun[-1] == 's' else noun + "'s"
    
    else:
        noun = pluralize(noun)
        # Plural form
        if tag == 'NNS':
            return noun
        # Plural possessive
        else:
            return noun + "'" if noun[-1] == 's' else noun + "'s"


def pluralize(noun):
    
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

    # if nothing funky is going on, pluralize by just adding 's'
    else:
        return noun + 's' '''


# Process adjectives
def process_adj(adj, adj_tag, tag):
    '''
        Takes adj_tag which is the word's tag in the database, used
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
                if not adj[-1] == 'n':
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


'''
# Process verbs
def process_verb(verb, verb_tag, tag):

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
            
            # past tense
            if tag == 'VBD':
                if end_cons_y(verb):
                    # if last char is 'y' and preceded by a consonant, replace with 'i'
                    verb = verb[:-1] + 'i' 
                return verb + 'ed'
            
            # else it will be VBG (present participle)
            else:
                return verb + 'ing' '''


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

    # else: RB (base form)
    else:
        return adv


'''
# Check if last character is 'y' and is preceded by a consonant
def end_cons_y(word):
    if word[-1] == 'y' and word[-2] not in VOWELS:
        return True
    else:
        return False '''


# Check if tag is valid, used in WordForm to validate tag field
def check_word_tag(tag):
    if tag in WORDLIST_TAGS_ALLOWED.keys():
        return True
    else:
        return False


# Check sentence tags, used to validate SentenceForm tags
def check_sentence_tags(sentence):
    tags = sentence.split('/')
    for tag in tags:
        if tag not in MODEL_TAGS_ALLOWED and tag not in SPECIAL_WORDS:
            return tag
    return 'allowed'