import math
import numpy as np
import random
import speech_recognition as sr

def Leitner(words, translation, threshold, answer_format):

    # Number of words
    n_words = len(words)

    # Number of 'boxes' with 10 words per box
    n_boxes = math.ceil(n_words / 10) + 1

    # Dictionary containing the box number of each word
    words_box = dict(zip(words, np.ones(n_words)))

    # Dictionary containing the translation of each word
    words_translation = dict(zip(words, translation))

    box = 1
    cycle = 0
    over_threshold = False

    while not over_threshold: # If too many words are not in the last box

        random.shuffle(words) # Randomize words order
        for word in words:

            if words_box[word] <= box:

                # User answer, correct translation, box of word
                if answer_format == 0: # If user wants to type the answer
                    answer = input(f'What is the translation of {word}? ').lower()

                elif answer_format == 1: # If user wants to say the answer

                    print(f'What is the translation of {word}? ')
                    # Record answer
                    try:
                        r = sr.Recognizer()
                        mic = sr.Microphone()
                        print('Recording...')

                        with mic as source:
                            r.adjust_for_ambient_noise(source)
                            audio = r.listen(source)
                        answer = r.recognize_google(audio, language='en').lower()
                        print(answer)

                    # Ask user to type answer in case of error
                    except:
                        print("I didn't understand your answer! Please type it...")
                        answer = input(f'What is the translation of {word}? ').lower()

                word_translated = words_translation[word].lower()
                word_box = words_box[word]

                # Correct answer, move word into next box
                if answer == word_translated: # Correct answer?
                    if word_box < n_boxes: # Not last box?
                        words_box[word] += 1

                # Wrong answer, move word into previous box
                else: # Wrong answer
                    if word_box > 1: # Not in first box?
                        words_box[word] -= 1

        box += 1
        box = box % (n_boxes + 1)

        if box == 0:
            box += 1

        if box == 1:
            cycle += 1

        # Amount in last box greater than threshold ?
        words_in_last_box = 0
        for word in words:
            if words_box[word] == n_boxes:
                words_in_last_box += 1

        pct_mastered = words_in_last_box / n_words
        if pct_mastered >= threshold:
            over_threshold = True

        print()
    print("You're a master!")