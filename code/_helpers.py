#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 21:18:19 2020

@author: markusschwedeler
"""

from bs4 import BeautifulSoup, FeatureNotFound
import os
import re
import pandas as pd

# Note: need to install html5lib parser



def import_sentimentwords(file):
    df = pd.read_csv(file, sep=',')
    tokeep = ['Word','Positive']
    positive = set([x['Word'].lower() for idx, x in df[tokeep].iterrows()
                    if x['Positive'] > 0])
    tokeep = ['Word','Negative']
    negative = set([x['Word'].lower() for idx, x in df[tokeep].iterrows()
                    if x['Negative'] > 0])
    return {'positive':positive, 'negative':negative}



def import_riskwords(file):
    synonyms = set()
    with open(file, 'r') as inp:
        for line in inp:
            split = line.split(' ')
            for syn in split:
                synonyms.add(re.sub('\n', '', syn))
    return synonyms



def import_politicalbigrams(file):
    df = pd.read_csv(file, sep=',', encoding='utf-8')
    df = df.assign(bigram=df['bigram'].str.replace('_', ' '))
    df.rename(columns={'politicaltbb':'tfidf'}, inplace=True)
    df.set_index('bigram', inplace=True)
    return df.to_dict(orient='index')



def load_transcripts(folder):
    
    # ATTENTION: Assumes html file was downloaded from The Motley Fool
    
    # Collect files in list
    files = [x for x in os.listdir(folder) if '.html' in x]
    
    # Collect results here
    results = {}
    
    # Loop through all files
    for file in files:

        print('Working on', file)
        
        # Load HTML
        with open(folder + file, 'r', encoding='utf-8') as infile:
            webpage = infile.read()
            
        # Parse
        try:
            soup = BeautifulSoup(webpage, 'html5lib')
        except FeatureNotFound:
            soup = BeautifulSoup(webpage, 'html.parser')

        # Narrow down to relevant content
        try:
            content = soup.select('[class~=article-content]')[0]
        except IndexError:
            # To support current version of the Motley Fool website
            content = soup.select('[class~=tailwind-article-body]')[0]
        title = clean_title(soup.title.get_text())
        
        # Extract text
        text = []
        for part in content.find_all('p'):

            # Metadata
            exists = [x.get('id') for x in part.find_all(True)]
            if 'date' in exists:
                date = part.find(id='date').get_text()
                time = part.find(id='time').get_text()
                try:
                    ticker = part.find(class_='ticker').get_text()
                except AttributeError:
                    # To support current version of the Motley Fool website
                    ticker = part.find(class_='ticker-symbol').get_text()
                continue
            
            # Skip links
            links = part.find_all(href=True)
            if links:
                continue
            
            # Skip Motley Fool
            if re.search(r'The Motley Fool.$', part.get_text()):
                continue
            
            # Text
            text.append(part.get_text())
        
        # Collect
        results[title] = {'text':' '.join(text),
                          'date':date,
                          'time':time,
                          'ticker':ticker}
                
    return results



def clean_title(string):
    
    # Remove leading and trailing white space
    string = re.sub(r'^\s+','', string)
    string = re.sub(r'\s+$', '', string)
    
    # Remove The Motley Fool
    string = re.sub(r' \| [\s\S]+$', '', string)
    
    return string



def preprocess(nested_dict, window_size=20):
    
    # Make copy into which window of 22 words is pasted
    result = nested_dict.copy()

    # Loop
    for title, content in nested_dict.items():
        
        # Access raw text
        text_str = content['text']
        
        # Preprocess
        text_str = re.sub(r'[^a-zA-Z ]', '', text_str.lower())
        words = text_str.split()
        
        # TODO: Remove name of analysts
        
        # Bigrams
        bigrams = [' '.join(x) for x in zip(words[0:], words[1:])]
        
        # Window of +/- 10 consecutive bigrams
        window = list(zip(*[bigrams[i:] for i in range(window_size+1)]))
        
        result[title]['bigram_windows'] = window
        result[title]['cleaned'] = words
        
    return result


