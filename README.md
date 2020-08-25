# firmlevelrisk

This repository hosts a basic Python code that calculates the firm level scores of earnings call transcripts as developed in Hassan et al. (2020).

Please see https://www.firmlevelrisk.com/ for the most recent update of the scores.

To run this code, you need to install Python 3 and the following modules: BeautifulSoup, Pandas.

## Overview
This code creates the following scores:
* Risk (*Risk* in the paper)
* Sentiment (*Sentiment* in the paper)
* Covid (as in the recent working paper on firm exposure to diseases; see https://www.firmlevelrisk.com/)
* Political (*Pol* in the paper)
* Political Risk (*PRisk* in the paper)
* Political Sentiment (*PSentiment* in the paper)

For more details on the scores, please see the paper itself.

## Inputs (see "~./input/")
* **Earnings call transcripts** I use two example earnings call transcripts that I downloaded from https://www.fool.com/earnings-call-transcripts/ but more can be added.
* **Synonyms of risk** Manually transcribed from Oxford Dictionary.
* **Sentiment words** Downloaded from https://sraf.nd.edu/textual-analysis/resources/#Master%20Dictionary.
* **Political bigrams and associated tf\*idf weights** Taken from the latest update of the PRisk scores. Note that the political bigrams are not published on https://www.firmlevelrisk.com/. But we include them in this repository for convenience. For more details on how they are created, please see the readme.md in its input folder here or the paper.

## Output (see "~./output/")

A tab-separated file that contains the above scores for each of the earnings call transcripts.
