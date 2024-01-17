# IDP Project Repository

## Project Description

Analyze the personality of a person from scraping result of their social media account.

## File Structure

- `linkedin.py`: Scraping LinkedIn profile
- `twitter.py`: Scraping Twitter profile
- `facebook.py`: Scraping Facebook profile
- `merge_csv.py`: Merging all csv files into one. Each scaper stores the scraped file inside a single csv file. This script will merge all csv files into one.
- `process_text.py`: After merging all csv files, the script process text into txt file format and remove useless words that is not helpful in receptiviti analysis to save expense.
- `receptiviti.py`: Analyzing the personality of a person from their social media account. This script will read the merged csv file and analyze the personality of the person.
- `visualize.py`: Visualizing the result of the analysis.

## How to Run:

- Run twitter.py to scrape twitter. Adjust line 102 to set the directory of the initail founders dataset.
