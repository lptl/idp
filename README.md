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

### Initial Data Exploration:
- Open the python notebook file Data_exploration.ipynb on Jupyter Notebook, Google Colab or VS Code.
- Adjust the path of the input file in cell 4.
- Run.
- Since it's a Jupyter Notebook, the outputs from the latest execution of the file is visible on github upon opening it.

### Twitter Scraping:
- install snscrape using the following command: pip3 install --upgrade git+https://github.com/JustAnotherArchivist/snscrape.git
- Run twitter.py to scrape twitter. Adjust line 102 to set the directory of the initail founders dataset.
- The scrapper requires internet connection.
- The scrapping sometimes randomly shuts down due to network issues. As a result please keep track of until which index twitter data has been scrapped.
- Then rerun the twitter.py by adjusting the value of starting index at line 105.

### LinkedIn Scraping:

### Reciptiviti API:


### Combine generated personality scores with founders data:
- Open Combine_dataset.ipynb on Jupyter Notebook, Google Colab or VS Code.
- Adjust the path to the initial dataset on cell 3.
- Adjust the path to the directory containing all JSON files in which personality scores of the founders are stored.
- Run
- Since it's a Jupyter Notebook, the outputs from the latest execution of the file is visible on github upon opening it.

### Generate boxplots of personality score distribution:
- Open boxplot.ipynb on Jupyter Notebook, Google Colab or VS Code.
- Set the path conraining all JSON files containing personality of founders in cell 3.
- Run
- Since it's a Jupyter Notebook, the outputs from the latest execution of the file is visible on github upon opening it.
  
### Correlation Analysis Numerical:
- Run Correlation2.ipynb with the merged_dataset.csv in the same directory as the python notebook.
- Since it's a Jupyter Notebook, the outputs from the latest execution of the file is visible on github upon opening it.

### Company level Statistical Analysis:
- Run company_analysis.ipynb with the merged_dataset.csv in the same directory as the python notebook.
- Since it's a Jupyter Notebook, the outputs from the latest execution of the file is visible on github upon opening it.

