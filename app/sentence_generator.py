import random # maybe not required?
from app import app, db
from sqlalchemy.sql.expression import func, select
from app.models import SentenceModel, WordList


'''
Part-of-speech tags used:

special words
BEZ     is
BER     are
HV      have

word classes
IN      preposition
JJ      adjective
NN      singular noun
NNS     plural noun
RB      adverb


# own tweaks (not in Brown Corpus) - KANSKE
AI      article indefinite (a/an), determine programmatically
AD      article definite (the)



'''





# Main function
def generate_sentence():


#     # get random sentence model from database
#     sentence_model = random_sentence_model()
    
#     # split model string into array
#     model_arr = sentence_model.sentence.split('/')

#     sentence = ''

#     # loop through model array
#     for tag in model_arr:

#         # get word
#         word = random_word(tag)

#         # KONTROLLERA OM TAG == verb ELLER adjektiv SOM BEHÖVER EXEMPELVIS BÖJAS ELLER ADVERBIFIERAS
#         # do it here


#         # append word to sentence
#         sentence += word + ' '  # hantera sista ordet, dvs mellanslag efter sista ordet kanske inte ska va med

# # format (capitalize, full stop etc?)
#     return sentence

    
    



    nouns = ['adam', 'Kvarjo', 'testman', 'kas']
    verbs = ['eats', 'pats', 'kills']

    sentence = random.choice(nouns).capitalize() + ' ' + random.choice(verbs) + ' ' + random.choice(nouns) + '.'

    return sentence


# Get random sentence model from database
def random_sentence_model():

    sentence_model = SentenceModel.query.order_by(func.random()).first()

    return sentence_model


# Get random word from database matching part-of-speech tag
def random_word(tag):

    word = WordList.query.filter_by(tag=tag).order_by(func.random()).first()

    return word


# # Transform adjective into adverb
# def adverbify(adj):
#     return adj + 'ly'


# # Conjugate verb
# def conjugate(verb, tag):
#     '''
#         Gets tempus from tag argument, transforms verb accordingly
#     '''

#      return conjugated_verb


# # Transform noun into plural form, perhaps add article?
# def pluralize(noun):
#     return noun + 's'