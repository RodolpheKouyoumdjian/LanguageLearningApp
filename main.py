'''
from googletrans import Translator

translator = Translator()
translation = translator.translate("Der Himmel ist blau und ich mag Bananen", dest='en')
print(translation.pronunciation)
'''

import pickle
from functions import Leitner

# Get words from file
file = open('data.pkl', 'rb')
output = pickle.load(file)
original_words = output['Original']
translated_words = output['Translations']


language = input('Enter the language you wish to learn: ').lower()

while language not in original_words.keys():
    input('We do not offer this language, please enter one we offer: ').lower()

print('Would you like to type or say your answer?')
answer_format = int(input('Enter 0 to type, 1 to say it: '))

while answer_format != 0 and answer_format != 1:
    answer_format = int(input('Please enter 0 or 1: '))

words = original_words[language]
translation = translated_words[language]

Leitner(words, translation, 1, answer_format)