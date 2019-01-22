import random 
from app import app, db
from sqlalchemy.sql.expression import func, select
from sqlalchemy import or_
from app.models import SentenceModel, WordList

# Static assets
from app.sentence_gen_statics import VOWELS, PRONOUNS, NOUN_EXCEPTIONS 
from app.sentence_gen_statics import SAME_IN_PLURAL, SAME_AS_ADJ
from app.sentence_gen_statics import WORD_BLACKLIST, CONJUNCTIONS
from app.sentence_gen_statics import PREPOSITIONS, BE, MOD_AUXS
from app.sentence_gen_statics import CARDINALS, ORDINALS, IRREGULAR_VERBS
from app.sentence_gen_statics import TAG_OPTIONS

from app.sentence_gen_statics import NOUN, PROPER_NOUN, PRONOUN, ADJECTIVE
from app.sentence_gen_statics import VERB, ADVERB, PREPOSITION, CONJUNCTION
from app.sentence_gen_statics import CARDINAL, ORDINAL, DEF_ARTICLE 
from app.sentence_gen_statics import INDEF_ARTICLE, MOD_AUX, SPECIAL

from app.sentence_gen_statics import SINGULAR, PLURAL, INHERIT
from app.sentence_gen_statics import POSITIVE, COMPARATIVE, SUPERLATIVE
from app.sentence_gen_statics import MALE, FEMALE, NEUTRAL
from app.sentence_gen_statics import INFINITIVE, PRESENT_TENSE, PRESENT_PART
from app.sentence_gen_statics import PAST_TENSE, PAST_PART, PAST_CONT, FUTURE


"""
    sentence_generator.py
    A sentence generator that generates pseudo-random sentences from 
    sentence models. Words as well as sentence models are saved
    manually in database tables and later retrieved for sentence
    generation.

    Sentence models consist of tags, for the most part parts-of-speech
    or word classes, based on The Brown University Standard Corpus of 
    Present-Day American English
    (https://en.wikipedia.org/wiki/Brown_Corpus) but customized to fit
    application, see sentence_gen_statics.py for full list of tags.
    

    Notes on usage:
    * Save words and their tags in database in all lowercase, even 
    proper nouns such as people's names (capitalized automatically
    by program).

    * Save only words in their base form (nouns in singular, verbs in
    infinitive form).
    
    * Don't save regular adverbs (handled by program).
    
    * Don't save pronouns, prepositions or conjunctions (handled by 
    program).
    
    * English is full of exceptions. Some of these are handled by the 
    program. For example, some nouns (e.g. 'deer') is the same in
    plural (not 'deers'), some adverbs look the same as their adjective
    counterparts (e.g. 'late' in 'I will be late', not 'I will be 
    lately'). A number of these exceptions are stored in 
    sentence_gen_statics.py. If you discover more words that don't look
    right when chewed by the generator, see if they fit in any of the 
    exceptions lists or add them to the WORD_BLACKLIST.

    * Not all word forms are saved explicitly in database:
        * Nouns are only saved in singular form, plural form is 
        generated by application.
        * Adjectives are stored in base (positive) form only. Their 
        comparative.
          and superlative forms are generated by application.
        * Verbs are stored in their base (infinitive) form and 
        conjugated as needed.
        * Regular adverbs are not stored but instead generated from 
        their adjective
          versions. Certain adverbs are stored, however, such as 
          adverbs of place, e.g. 'indoors'.

    * Sentence_generator aims to be able to generate grammatically 
    correct sentences but it has several limitations and might fail. 
    If a word is misbehaving, it can be added to WORD_BLACKLIST and 
    forbidden from future entry. Current limitations, possibly subject
    to change include:
        * Program has no semantic component, i.e. sentences will 
        probably not make any sense.
        * Fails to pluralize certain nouns (ending in -i in plural, 
        e.g. cactus - cacti)

    Sentence model formatting rules:
    Sentence models consist of tags separated by forward slashes (/) 
    where each tag represents a word, e.g. "TAG/TAG/TAG/TAG/TAG". Each 
    tag in turn consists of subtags, separated by periods (.) that 
    represent properties of each word, e.g. singular vs plural for 
    nouns or whether a verb is regular or irregular. See each word 
    class' word-getter-functions' doc strings or instructions on 
    manage_sentences admin page for details.
"""


class Sentence:
    """ Creates new sentence object. Actual sentence is a list
        (self.sentence) of word objects accessible through 
        self.sentence[index].word. """

    def __init__(self, model):

        # Gets model as string, convert to list
        self.mod_list = model.split('/')
    
        # Randomly generate subtags if needed (if tags contain '??')
        self.mod_list = self.set_random_tags(self.mod_list)

        # Store subject, verb, object indices in dictionary
        self.SVO_ind = self.get_SVO_ind(self.mod_list)

        # Initialize sentence (list of 'x', to be replaced)
        self.sentence = list('x' * len(self.mod_list))
        
        # Get subject
        self.current_word = self.SVO_ind['subj']
        self.sentence[self.SVO_ind['subj']] = self.get_word(
            self.mod_list[self.SVO_ind['subj']])

        # Get verb
        if 'verb' in self.SVO_ind.keys():
            self.current_word = self.SVO_ind['verb']
            self.sentence[self.SVO_ind['verb']] = self.get_word(
                self.mod_list[self.SVO_ind['verb']])
            
        # Get object
        if 'obj' in self.SVO_ind.keys():
            self.current_word = self.SVO_ind['obj']
            self.sentence[self.SVO_ind['obj']] = self.get_word(
                self.mod_list[self.SVO_ind['obj']])

        # Initialize list of indefinite article indices
        self.ai_inds = []

        # Get rest of words
        for i in range(len(self.sentence)):

            # Update current working word index
            self.current_word = i

            if self.sentence[i] == 'x':
                # Get indefinite article index (because we need all 
                # nouns before we can choose correct articles for them)
                if self.mod_list[i].split('.')[0] == INDEF_ARTICLE:
                    self.ai_inds.append(i)
                # Else get a word
                else:
                    self.sentence[i] = self.get_word(self.mod_list[i])

        # Get any indefinite articles
        if self.ai_inds:
            for ind in self.ai_inds:
                self.current_word = ind
                self.sentence[ind] = self.get_indef_article(ind)

        
    def set_random_tags(self, mod_list):
        """ Checks model for '??' and replaces with random fitting tag,
            stored in dict TAG_OPTIONS in statics. """

        for tag, i in zip(mod_list, range(len(mod_list))):
            subtags = tag.split('.')
            # loop through list of subtags, replace '??' with
            # value from dictionary in statics
            for subtag, j in zip(subtags, range(len(subtags))):
                if subtag == '??':
                    self.mod_list[i] = self.mod_list[i].replace(
                        self.mod_list[i].split('.')[j],
                        random.choice(TAG_OPTIONS[subtags[0]][j]))

        return mod_list


    def get_SVO_ind(self, tag_list):
        """ create a dictionary storing indices of subject, verb, 
            object. """
        
        indices = {}

        for tag in tag_list:
            for subtag in tag.split('.'):
                if subtag == 's':
                    indices['subj'] = tag_list.index(tag)
                elif subtag == 'o':
                    indices['obj'] = tag_list.index(tag)
                elif tag.split('.')[0] == 'VB':
                    indices['verb'] = tag_list.index(tag)
        
        return indices


    def get_word(self, tag):
        """ Word-getter function. Calls functions to retrieve words by 
            word class. Each of those functions create a new word 
            object, either by retrieving a word from database, from 
            statics (pronouns, conjunctions), or sometimes raw words 
            from sentence model. """

        get_func_dict = {
            NOUN: self.get_noun,
            PROPER_NOUN: self.get_proper_noun,
            PRONOUN: self.get_pronoun,
            ADJECTIVE: self.get_adj,
            VERB: self.get_verb,
            ADVERB: self.get_adv,
            PREPOSITION: self.get_prep_conj_md,
            CONJUNCTION: self.get_prep_conj_md,
            MOD_AUX: self.get_prep_conj_md,
            CARDINAL: self.get_card,
            ORDINAL: self.get_ord,
            DEF_ARTICLE: self.get_def_article,
            SPECIAL: self.get_spec
        }

        word = get_func_dict[tag.split('.')[0]](tag)

        return word
        

    def get_verb(self, tag):
        """ Get a verb from database, conjugate it properly and 
            return it.
                
            Verb sentence model rules:
            0: Always 'VB' 
            1: 'I', 'Z', 'D', 'G', 'N', 'C', 'F'
            2: optional any verb
            """            

        tags = tag.split('.')
        # Check if a particular verb has been specified by a third
        # verb subtag (at tags[2]), else get a word from database
        try:
            verb = WordList(tag=tags[0], word=tags[2], mult_syll=0)
            if verb.word in list(IRREGULAR_VERBS):
                verb.irregular = 1
            else:
                verb.irregular = 0
        except:
            verb = (WordList.query
                .filter_by(tag=tags[0])
                .order_by(func.random()).first())

        # If not infinitive form, conjugate
        if tags[1] != INFINITIVE:
            verb.word = self.conjugate(verb.word, verb.mult_syll, tags[1], 
                verb.irregular)

        return verb

    
    def conjugate(self, verb, mult_syll, tag, irregular):
        """ Conjugate and return correct form of verb. """

        subj_tags = self.mod_list[self.SVO_ind['subj']]

        # Special handling of forms of 'be', e.g. 'is', 'are', 'was'
        if verb == 'be':
            return self.conj_be(tag, subj_tags)

        # Future tense
        if tag == FUTURE:
            return 'will ' + verb

        # Present tense
        elif tag == PRESENT_TENSE:
            return self.present_tensify(verb)
            
        # Else either past tense, past continuous, present participle 
        # or past participle
        else:
            # Store base verb
            self.base_verb = verb
            # If last char is consonant and preceded by vowel, 
            # double consonant
            if verb[-1] not in VOWELS and verb[-2] in VOWELS:
                # WARNING NOT REALLY GOOD, ALSO HAS TO DO WITH SYLLABLE 
                # STRESS SO BEWARE WHEN ADDING WORDS
                if verb[-3] not in VOWELS and mult_syll == 0:
                    if verb.endswith('c'):
                        verb += 'k'
                    elif verb[-1] not in ['h', 'w', 'x', 'y']:
                        verb += verb[-1]

            # Remove last letter if it is 'e'
            elif verb[-1] == 'e' and verb[-2] not in VOWELS:
                verb = verb[:-1]
            
            # Past tense
            if tag == PAST_TENSE:
                return self.make_past_tense(verb)
            
            # Else it will be present participle, past participle or 
            # past continuous
            elif tag == PRESENT_PART:
                # Present participle is present tense of 'be' and the 
                # verb in ing-form. 
                return (self.conj_be(PRESENT_TENSE, subj_tags) + ' ' + 
                    verb + 'ing')
            
            elif tag == PAST_CONT:
                return (self.conj_be(PAST_TENSE, subj_tags) + ' ' + 
                    verb + 'ing')
            
            # else it will be past participle
            else:
                return self.make_past_part(verb)


    def conj_be(self, form, subj_tag):
        """ Conjugate 'be'. checks sentence subject's word class and 
            count (singular/plural). Also checks desired form (tempus) 
            of verb (be) and returns appropriate form. """

        subj_tags = subj_tag.split('.')

        # Sentence subject's possible word classes
        w_classes = {PROPER_NOUN: BE[PROPER_NOUN][form]}

        # Try to check if noun is plural or singular. 
        # Will throw error if subj is not a noun
        try:
            w_classes[NOUN] = BE[subj_tags[0]][form][subj_tags[2]]
        except:
            pass

        # If subj is a pronoun, get pronoun word and use that as key
        if subj_tags[0] == PRONOUN:
            pronoun_word = self.sentence[self.SVO_ind['subj']].word
            w_classes[subj_tags[0]] = BE[subj_tags[0]][pronoun_word][form]

        return w_classes[subj_tags[0]]


    def make_past_part(self, verb):
        """ Transform verb into past participle. Nouns, proper nouns and
            pronouns in third person singular use 'has' instead' of
            'have'. """

        if self.base_verb in list(IRREGULAR_VERBS):
            verb = IRREGULAR_VERBS[self.base_verb][PAST_PART]
        else: 
            verb = self.make_past_tense(verb)

        return self.check_have() + ' ' + verb
            

    def make_past_tense(self, verb):
        """ Transform verb into simple past tense. """

        if self.base_verb in list(IRREGULAR_VERBS):
            return IRREGULAR_VERBS[self.base_verb][PAST_TENSE]
        else:
            if self.end_cons_y(verb):
                # if last char is 'y' and preceded by a consonant, 
                # replace with 'i'
                verb = verb[:-1] + 'i' 

        return verb + 'ed'

    
    def present_tensify(self, verb):
        """ Transform verb into present tense. """

        if verb == 'do':
            return self.check_do()
        elif verb == 'have':
            return self.check_have()
        else:
            # Add 'es' or 's' if word is noun, proper noun or
            # pronoun in third person singular
            if self.check_subj():
                if self.end_cons_y(verb):
                    verb = verb[:-1] + 'i'
                    return verb + 'es'
                else:
                    return verb + 's'
            else:
                return verb


    def check_subj(self):
        """ Check if subject is a singular noun, proper noun or a 
            pronoun in third person singular. """

        subj_tags = self.mod_list[self.SVO_ind['subj']].split('.')
        third_pers = False

        try:
            if subj_tags[3] == '3':
                third_pers = True
        except:
            pass
       
        if (subj_tags[0] == NOUN and subj_tags[2] == SINGULAR) or \
            subj_tags[0] == PROPER_NOUN or third_pers:
            return True
        else:
            return False


    def check_do(self):
        """ Transform 'do' to 'does' if subject is a singular noun, 
            proper noun or a pronoun in third person singular. """
        
        if self.check_subj():
            return 'does'
        else:
            return 'do'

    
    def check_have(self):
        """ Transform 'have' to 'has' if subject is a singular noun, 
            proper noun or a pronoun in third person singular. """

        if self.check_subj():
            return 'has'
        else:
            return 'have'
            

    def get_noun(self, tag):
        """ Get a noun word object from database, check if it needs to 
            be pluralized or transformed for possession and then return
            it.
            
            Noun sentence model rules:
            0: Always 'NN'
            1: 's', 'o', '$', 'n'   
            2: 'S', 'P' """

        tags = tag.split('.')
        noun = (WordList.query.filter_by(tag=tags[0])
                              .order_by(func.random()).first())

        # Pluralize
        if tags[2] == PLURAL:
            noun.word = self.pluralize(noun.word)

        # Handle possessive case
        if tags[1] == '$':
             noun.word += "'" if noun.word[-1] == 's' else "'s"

        return noun


    def pluralize(self, noun):
        """ Find and return proper plural form for noun """

        # Some nouns don't change in plural form
        if noun in SAME_IN_PLURAL:
            return noun
        
        # If noun ends in 's', 'sh', 'ch', 'x', or 'z', 
        # add 'es' instead of 's'
        elif (noun.endswith('s') or noun.endswith('sh') or 
            noun.endswith('ch') or noun.endswith('x') or 
            noun.endswith('z')):
            return noun + 'es'
        
        # If noun ends in 'f' or 'fe', usually 'f' is changed
        # to 've' before adding 's'
        elif noun.endswith('f'):
            if noun not in NOUN_EXCEPTIONS:
                noun = noun[:-1]
                return noun + 'ves'
        elif noun.endswith('fe'):
            if noun not in NOUN_EXCEPTIONS:
                return noun[:-2] + 'ves'
        
        # If last letter is 'y' and preceding letter is a 
        # consonant, replace 'y' with 'i', pluralize with 'es'
        elif self.end_cons_y(noun):
            noun = noun[:-1]
            return noun + 'ies'

        # If noun ends in 'o', usually pluralize with 'es'
        elif noun.endswith('o') and noun not in NOUN_EXCEPTIONS:
            return noun + 'es'

        # If noun ends in 'on' or 'um', remove and pluralize with 'a',
        # e.g. 'phenomenon' - 'phenomena'
        elif noun.endswith('on') or noun.endswith('um'):
            if noun not in NOUN_EXCEPTIONS:
                noun = noun[:-2]
                return noun + 'a'
            else:
                return noun + 's'

        # If nothing funky is going on, pluralize by just adding 's'
        else:
            return noun + 's'


    def end_cons_y(self, word):
        """ Check if last character is 'y' and is preceded by a 
            consonant. """

        if word[-1] == 'y' and word[-2] not in VOWELS:
            return True
        else:
            return False


    def get_proper_noun(self, tag):
        """ Create proper noun object. 
            Get a word, transform for possession if needed and return.
            
            proper noun sentence model rules:
            0: Always 'NP'
            1: 's', 'o', '$', 'n' """

        proper_noun = (WordList.query.filter_by(tag=tag.split('.')[0])
                                     .order_by(func.random()).first())

        proper_noun.word = proper_noun.word.capitalize()

        # handle possessive case
        if tag.split('.')[1] == '$':
             proper_noun.word += "'" if proper_noun.word[-1] == 's' else "'s"

        return proper_noun

                
    def get_pronoun(self, tag):
        """ Pronouns aren't stored in database. Instead they're 
            statically stored in static assets, in nested dictionary 
            form.

            First get base pronoun, then figure out the correct form.
        
            Pronoun sentence model rules:
            0: Always 'PN'                          
            1: 's', 'o', 'ref_s', 'ref_o', 'reflex' 
                # subject, object or referencing them (actually called 
                # possessive adjective and possessive pronouns) and 
                # reflexive.
            2: 'S', 'P', 'IN'
            3: '1', '2', '3', 'IN'
            4: 'MM', 'FF', 'NN', 'IN' """

        tags = tag.split('.')

        # Establish base pronoun
        pronoun = self.get_base_pronoun(tag)

        # Get correct form
        if tags[1] == 'o':
            pronoun.word = PRONOUNS[pronoun.word]['obj']
        elif tags[1] == 'ref_s':
            pronoun.word = PRONOUNS[pronoun.word]['poss_adj']
        elif tags[1] == 'ref_o':
            pronoun.word = PRONOUNS[pronoun.word]['poss_pronoun']
        elif tags[1] == 'reflex':
            pronoun.word = PRONOUNS[pronoun.word]['reflex']

        return pronoun


    def get_base_pronoun(self, tag):
        """ Create pronoun word object and figure out correct base
            pronoun. """

        tags = tag.split('.')

        pronoun = WordList(word='', gender=NEUTRAL, tag=tags[0])

        # Check inheritance
        if tags[2] == INHERIT:
            # if referencing a word, inherit from that word object
            if tags[1] == 'ref_s':
                pronoun = self.inherit_pronoun(tags, 
                    self.sentence[self.SVO_ind['subj']], pronoun)
            elif tags[1] == 'ref_o':
                pronoun = self.inherit_pronoun(tags, 
                self.sentence[self.SVO_ind['obj']], pronoun)

        # Singular, i.e. I, you, he, she, it
        elif tags[2] == SINGULAR:
            # First person
            if tags[3] == '1':
                pronoun.word = 'I'
            # Second person
            elif tags[3] == '2':
                pronoun.word = 'you'
            # Third person
            elif tags[3] == '3':
                # Male
                if tags[4] == MALE:
                    pronoun.word = 'he'
                    pronoun.gender = MALE
                # Female
                elif tags[4] == FEMALE:
                    pronoun.word = 'she'
                    pronoun.gender = FEMALE
                # Default to neutral
                else:
                    pronoun.word = 'it'
                    pronoun.gender = NEUTRAL

        # Plural, i.e. either we, you, they
        elif tags[2] == PLURAL:
            # First person
            if tags[3] == '1':
                pronoun.word = 'we'
            # Second person
            elif tags[3] == '2':
                pronoun.word = 'you'
            # Default to third person
            else:
                pronoun.word = 'they'

        # default to random
        else:
            pronoun.word = random.choice(list(PRONOUNS.keys()))

            if pronoun.word == 'he':
                pronoun.gender = MALE
            elif pronoun.word == 'she':
                pronoun.gender = FEMALE

        return pronoun


    def inherit_pronoun(self, tags, ref, pronoun):
        """ First checks if referenced word is a pronoun. If it is, 
            return it. If it isn't a pronoun, it will be either a 
            proper noun or a noun, so a gender check will suffice to 
            select correct pronoun. If not male or female, function 
            defaults to neutral, i.e. 'it'. """

        if ref.word in list(PRONOUNS):
            pronoun.word = ref.word
            pronoun.gender = ref.gender
        elif ref.gender == MALE:
            pronoun.word = 'he'
            pronoun.gender = MALE
        elif ref.gender == FEMALE:
            pronoun.word = 'she'
            pronoun.gender = FEMALE
        else:
            pronoun.word = 'it'
            pronoun.gender = NEUTRAL

        return pronoun


    def get_adj(self, tag):
        """ Create adjective object.
        
            Sentence model rules:
            0: 'JJ'
            1: 'P', 'C', 'S'  
            2: 'ref_s', 'ref_o', 'ref_n' """

        tags = tag.split('.')
        adj = (WordList.query.filter_by(tag=tags[0])
                       .order_by(func.random()).first())

        # handle comparative, superlative forms
        if tags[1] != POSITIVE:
            adj.word = self.transform_adj(adj, tags[1]) 

        return adj

    
    def transform_adj(self, adj, form):
        """ Transform adjective to comparative or superlative form. """

        transform = {
            'C':{'pref':'more ','suff':'er'},
            'S':{'pref':'most ','suff':'est'}
        }
        
        word = adj.word
        mult_syllables = adj.mult_syll

        if adj.irregular == 0:
            # One syllable adjectives
            if mult_syllables == 0:
                # If word ends in 'e', remove 'e'
                if word[-1] == 'e':
                    word = word[:-1]
                # If word ends in vowel and consonant, double consonant
                elif word[-1] not in VOWELS and word[-2] in VOWELS:
                    if not word[-1] == 'n':
                        word += word[-1]
                # Add suffix and return
                return word + transform[form]['suff']

            # Two or more syllable adjectives
            elif mult_syllables == 1:
                # If word ends in 'y' replace with 'i'
                if word.endswith('y'):
                    word = word[:-1] + 'i'
                    # Add suffix and return
                    return word + transform[form]['suff']
                # Else add prefix ('more ' or 'most ') and return
                else:
                    return transform[form]['pref'] + word            
        # else HANDLE IRREGULAR ADJECTIVES!!
        else:
            return word

    
    def get_adv(self, tag):
        """ Create adverb object.
        
            Sentence model rules:
            0: 'RB'
            1: 'P', 'C', 'S'
            2: 'N', 'T', 'F', 'P' """

        tags = tag.split('.')

        # Get "normal" adverb, i.e. adjective-based
        if tags[2] == 'N':
            adv = (WordList.query.filter_by(tag=ADJECTIVE)
                                 .order_by(func.random()).first())
            # Set tag to adverb
            adv.tag = ADVERB

            # Adverbify
            if adv.irregular == 0:
                adv.word = self.adverbify(adv.word) 

            # Handle comparative, superlative forms
            if tags[1] != POSITIVE and adv.irregular == 0:
                adv.word = self.transform_adv(adv.word, tags[1])
        else:
            subtypes = {'T':'time',
                        'F':'frequency',
                        'P':'place'}

            adv = (WordList.query.filter_by(tag=tags[0], 
                subtype=subtypes[tags[2]]).order_by(func.random()).first())

        return adv


    def adverbify(self, adv):
        """ Turn adjective into adverb. Checks some grammatical rules
            and transforms adjective. """

        if self.end_cons_y(adv):
            adv = adv[:-1] + 'ily'
        elif adv.endswith('le') and adv[-3] not in VOWELS:
            adv = adv[:-1] + 'y'
        elif adv.endswith('ic'):
            if adv == 'public':
                adv += 'ly'
            else:
                adv += 'ally'
        else:
            if not adv.endswith('ly') and adv not in SAME_AS_ADJ:
                adv += 'ly'
        
        return adv


    def transform_adv(self, adv, form):
        """ Transform adverb into its comparative or superlative 
            form. """

        transform = {'C':{'pref':'more ','suff':'er'}, \
                     'S':{'pref':'most ','suff':'est'}}

        # Either add prefix or suffix
        if adv in SAME_AS_ADJ:
            if adv[-1] == 'y':
                adv = adv[:-1] + 'i'
            return adv + transform[form]['suff']
        else:
            return transform[form]['pref'] + adv


    def get_def_article(self, tag):
        """ Create word object for definite article, i.e. 'the'. """

        article = WordList(tag=tag, word='the')

        return article


    def get_prep_conj_md(self, tag):
        """ Create preposition, conjunction or modal
            auxiliary object.
        
        Sentence model rules:
        0: 'IN', 'CN', 'MD'
        1: desired word or '??' for random """

        tags = tag.split('.')
        word = WordList(tag=tags[0], word=tags[1])

        if tags[0] == MOD_AUX:
            if word.word == self.sentence[self.SVO_ind['verb']].word:
                word.word = random.choice(MOD_AUXS)

        return word

    
    def get_card(self, tag):
        """ Create cardinal number object. 
            Can generate numbers ranging from 2 to 9999.
        
            Sentence model rules:
            0: 'CD'
            1: '1', '2', '3', '4', '??'     # length or random """

        tags = tag.split('.')
        num_len = int(tags[1])
        text_num = self.textify(random.randint(2, int('9' * num_len) + 1))
        cardinal = WordList(tag=tags[0], word=text_num)

        return cardinal

    
    def textify(self, num):
        """ Translates a number into text. """

        text_num = ''

        if num < 21:
            text_num = CARDINALS[num]
        else:
            num = str(num)
            if 0 < int(num[-2:]) < 21:
                text_num = CARDINALS[int(num[-2:])]
            else:
                # Get second-from-right number (tens)
                if num[-2] != '0':
                    text_num = CARDINALS[int(num[-2]) * 10]
                # Get last digit, append to string
                if num[-1] != '0':
                    text_num += '-' + CARDINALS[int(num[-1])]
            # Get hundreds number
            if len(num) > 2 and int(num[-3]) != 0:
                hundreds_num = CARDINALS[int(num[-3])] + ' hundred'
                if int(num[-2:]) > 0:
                    hundreds_num += ' and '
                text_num = hundreds_num + text_num
            # Get thousands number
            if len(num) > 3:
                thousands_num = CARDINALS[int(num[0])] + ' thousand'
                if int(num[-3:]) > 0:
                    thousands_num += ', '
                text_num = thousands_num + text_num

        return text_num


    def get_ord(self, tag):
        """ Create ordinal number object. 
            Simply retrieve a random ordinal number from a static list.
            
            Model rules:
            0: 'OD' """

        ordinal = WordList(tag=tag.split('.')[0], word=random.choice(ORDINALS))

        return ordinal


    def get_indef_article(self, i):
        """ Create indefinite article object and choose the right 
            one. """

        article = WordList(tag=INDEF_ARTICLE)

        # If next word is noun, get its article
        if self.sentence[i+1].tag == NOUN:
            article.word = self.sentence[i+1].article
        # else check if next word starts with a vowel 
        # (not great solution but oh well)
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
    """ Gets random sentence model from database, creates a new
        Sentence instance object. The actual sentence (obj.sentence)
        is a list of word objects. """

    sentence_model = random_sentence_model()
    new_sentence = Sentence(sentence_model.sentence)

    sentence = ''
    for item in new_sentence.sentence:
        sentence += item.word + ' '

    return sentence.capitalize().rstrip() + '.'


def random_sentence_model():
    """ Get random sentence model from database. """

    sentence_model = SentenceModel.query.order_by(func.random()).first()

    return sentence_model