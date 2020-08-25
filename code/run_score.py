#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 21:12:55 2020

@author: markusschwedeler
"""

# Change me
homedir = '/Users/markusschwedeler/Projects/firmlevelrisk/'

# Modules
import os
os.chdir(homedir)
import sys
if not 'code/' in sys.path:
    sys.path.append('code/')
import _helpers as h
import re
import pandas as pd

# Files
earningscall_dir = 'input/earningscall_transcripts/'
output_dir = 'output/'
sentimentwords_file = ('input/sentimentwords/'
                       + 'LoughranMcDonald_MasterDictionary_2018.csv')
riskwords_file = 'input/riskwords/synonyms.txt'
polbigrams_file = 'input/political_bigrams/political_bigrams.csv'


#-----------------------------#
# 1) Load auxiliary data sets #
#-----------------------------#
# Import positive and negative sentiment words, risk words, and collect all
sentiment_words = h.import_sentimentwords(sentimentwords_file)
risk_words = h.import_riskwords(riskwords_file)
allwords = dict(sentiment_words, **{'risk':risk_words})

# Import political bigrams
political_bigrams = h.import_politicalbigrams(polbigrams_file)

# SarsCov2-related words
sarscov2 = ['Coronavirus', 'Corona virus', 'coronavirus',
            'Covid-19', 'COVID-19', 'Covid19', 'COVID19',
            'SARS-CoV-2', '2019-nCoV']
sarscov2_words = set([re.sub('[^a-z ]', '', x.lower()) for x in sarscov2])


#---------------------------------------------#
# 2) Load and clean earnings call transcripts #
#---------------------------------------------#
# Parse text and metadata from HTML
transcripts_raw = h.load_transcripts(earningscall_dir)

# Preprocess text and return window of 22 consecutive bigrams
preprocessed = h.preprocess(transcripts_raw)


#----------#
# 3) Score #
#----------#
# Note: For illustrative purposes, I don't call any custom function

# Loop through transcripts
scores = {}
for title, content in preprocessed.items():
    
    print('Working on:', title)
    scores[title] = {}
    
    # Access preprocessed windows of consecutive bigrams
    windows = content['bigram_windows']
    words = content['cleaned']
    
    # Total number of words (to normalize scores)
    totalwords = len(words)
    
    ### A) Score unconditional scores
    risk = len([word for word in words if word in allwords['risk']])
    sentpos = len([word for word in words if word in allwords['positive']])
    sentneg = len([word for word in words if word in allwords['negative']])
    covid = len([word for word in words if word in sarscov2_words])
    
    # Collect and prepare for conditional scores
    scores[title] = {
        'Risk':risk,
        'Sentiment':sentpos-sentneg,
        'Covid':covid,
        'Pol':0,
        'PRisk':0,
        'PSentiment':0,
        'Total words':totalwords
        }
    
    ### B) Score conditional scores
    # Loop through each windows
    for window in windows:
    
        # Find middle ngram and check whether a "political" bigram
        middle_bigram = window[10]
        if middle_bigram not in political_bigrams:
            continue
        tfidf = political_bigrams[middle_bigram]['tfidf']
        
        # Create word list for easy and quick access
        window_words = set([y for x in window for y in x.split()])
        
        # If yes, check whether risk synonym in window
        conditional_risk = (len([word for word in window_words
                            if word in allwords['risk']]) > 0)
        
        # If yes, check whether positive or negative sentiment
        conditional_sentpos = len([word for word in window_words
                                   if word in allwords['positive']])
        conditional_sentneg = len([word for word in window_words
                                   if word in allwords['negative']])
        
        # Weigh by tfidf
        conditional_risk = conditional_risk * tfidf
        conditional_sentpos = conditional_sentpos * tfidf
        conditional_sentneg = conditional_sentneg * tfidf
        
        # Collect results
        scores[title]['Pol'] += tfidf
        scores[title]['PRisk'] += conditional_risk
        scores[title]['PSentiment'] += (conditional_sentpos-
                                                 conditional_sentneg)
        

# Collect in dataframe
scores_df = pd.DataFrame().from_dict(scores, orient='index')
scores_df.index.name = 'event name'

# Scale
toscale = [x for x in scores_df.columns if x not in {'Total words'}]
for column in toscale:
    scores_df[column] = scores_df[column]*100000*(1/scores_df['Total words'])

# Write
scores_df.to_csv(output_dir + 'earningscall_scores.tsv', sep='\t',
                 encoding='utf-8')