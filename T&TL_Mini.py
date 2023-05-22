#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import messagebox
from PyDictionary import PyDictionary
from nltk.corpus import wordnet
from nltk.corpus import cmudict
import pronouncing
import pyttsx3


# In[2]:


d = cmudict.dict()
def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())
    return list(set(synonyms))

def get_antonyms(word):
    antonyms = []
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            if lemma.antonyms():
                antonyms.append(lemma.antonyms()[0].name())
    return list(set(antonyms))

def get_definition(word):
    dictionary=PyDictionary()
    return dictionary.meaning(word)

def get_rhyming_words(word):
    phones = pronouncing.phones_for_word(word.lower())
    if not phones:
        return []
    rhyme_part = pronouncing.rhyming_part(phones[0])
    rhyme_words = pronouncing.rhymes(word.lower())
    rhyme_words = [w for w in rhyme_words if w != word.lower()]
    return phones+rhyme_words

def get_example():
    word = word_entry.get().lower()
    for synset in wordnet.synsets(word):
        for example in synset.examples():
            if word in example:
                message = f"Example: {example}"
                messagebox.showinfo(title="Example Sentence", message=message)
                return
    messagebox.showwarning(title="Example Sentence", message="No example sentence found.")
    

def speak_word():
    word = word_entry.get()
    engine = pyttsx3.init()
    engine.say(word)
    engine.runAndWait()
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[1].id)


def search():
    word = word_entry.get().lower()
    synonyms = get_synonyms(word)
    antonyms = get_antonyms(word)
    definition = get_definition(word)
    rhyming_words = get_rhyming_words(word)
    if rhyming_words:
        message = f"Synonyms: {', '.join(synonyms)}\n\nAntonyms: {', '.join(antonyms)}\n\nDefinition: {definition}\n\nRhyming Words: {', '.join(rhyming_words)}"
    else:
        message = f"Synonyms: {', '.join(synonyms)}\n\nAntonyms: {', '.join(antonyms)}\n\nDefinition: {definition}\n\nNo rhyming words found."
    messagebox.showinfo(title="Search Results", message=message)


# In[3]:


window = tk.Tk()
window.title("Online Dictionary")
word_label = tk.Label(window, text="Enter a word:")
word_label.pack()
word_entry = tk.Entry(window)
word_entry.pack()
search_button = tk.Button(window, text="Search", command=search)
search_button.pack()
example_button = tk.Button(window, text="Example", command=get_example)
example_button.pack()
speak_button = tk.Button(window, text="Text-to-Speech", command=speak_word)
speak_button.pack()
window.mainloop()


# In[ ]:




