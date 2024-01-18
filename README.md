# IDP Project Repository

## Project Description

Analyze the personality of a person from scraping result of their social media account.


## Order of the code:

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
- It needs selenium to be installed, pip install selenium 
- run linkedin.py main.
- filepath is hardcoded as csv_file_path, if column names differ modify csv_file_content inputs.
- if you like to iterate more than 3576 rows (it was our sample size) modify for loop interval.
- The scrapper requires internet connection.
- LinkedIn frequently changes its site structure for preventing scraping, check the structure of the profiles page. 

### Processing the text prior to usage of Receptiviti API:
- process_text.py contains necessary fucntions to remove urls, symbols etc processing which must be done before feeding the texts to receptiviti API.
- It takes the given txt files from defined directory and controls if the txt files contains required number of words or less
- If the file contains more than 500 words it will take only first 500, if less then it will take all 

### Reciptiviti API: 
- Define input and output directories as; data_directory, json_directory respectively.
- Define starting and ending index numbers, it's dependent on alphabetical order.
- receptiviti_send() method contains api_key and api_secret, these must be changed if it will be used with a different account
- Returned Json files will be saved in the defined directory.

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

