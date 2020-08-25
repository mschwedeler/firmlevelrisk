# firmlevelrisk

This repository hosts a basic Python code that calculates the firm level scores of earnings call transcripts as developed in:
 * Hassan, Tarek, Stephan Hollander, Laurence van Lent, and Ahmed Tahoun, "Firm-Level Political Risk: Measurement and Effects," *Quarterly Journal of Economics*, 134(2020), pp. 2135-2202.
 * Hassan, Tarek, Stephan Hollander, Laurence van Lent, and Ahmed Tahoun, "Firm-level Exposure to Epidemic Diseases: Covid-19, SARS, and H1N1," *Working Paper*.
 * Hassan, Tarek, Stephan Hollander, Laurence van Lent, and Ahmed Tahoun, "The Global Impact of Brexit Uncertainty ," *Working Paper*.

Please see https://www.firmlevelrisk.com/ for the papers and most recent update of their firm level scores.


## Overview
To create the scores, please run `~./code/run_score.py`. The code creates the following scores:
* Risk (*Risk* in the QJE paper)
* Sentiment (*Sentiment* in the QJE paper)
* Covid (as in the recent working paper on firm exposure to diseases)
* Political (*Pol* in the QJE paper)
* Political Risk (*PRisk* in the QJE paper)
* Political Sentiment (*PSentiment* in the QJE paper)

For more details on the scores, please see the paper itself.

To run this code, you need to install Python 3 and the following modules: BeautifulSoup, Pandas.

Please direct any questions about the code to mschwed at bu dot edu.

## Inputs (see "~./input/")
* **Earnings call transcripts** I use two example earnings call transcripts that I downloaded from https://www.fool.com/earnings-call-transcripts/ but more can be added.
* **Synonyms of risk** Manually transcribed from Oxford Dictionary.
* **Sentiment words** Downloaded from https://sraf.nd.edu/textual-analysis/resources/#Master%20Dictionary.
* **Political bigrams and associated tf\*idf weights** Taken from the latest update of the PRisk scores. Note that the political bigrams are not published on https://www.firmlevelrisk.com/. But we include them in this repository for convenience. For more details on how they are created, please see the readme.md in its input folder here or the paper.

## Output (see "~./output/")

A tab-separated file that contains the above scores for each of the earnings call transcripts.
