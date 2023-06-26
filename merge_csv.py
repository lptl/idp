import sys
import os
import pandas as pd


def get_words_number(data_frame: pd.DataFrame) -> int:
    '''get the number of words in a data frame'''
    words_number = 0
    data_frame.rename(columns={'0': 'text'}, inplace=True)
    for _, row in data_frame.iterrows():
        words_number += len(row['text'].split(' '))
    print(f'words number: {words_number}')
    return words_number


def read_csv_file(csv_path):
    '''read a csv file and return a data frame'''
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        print(f'File not valid: {csv_path}')
        sys.exit(1)
    try:
        data = pd.read_csv(csv_path)
    except Exception as exception:
        print(f'Exception: {csv_path} is not valid: {exception}')
        data = pd.DataFrame(columns=['0'])
    return data


def process_linkedin(linkedin_frame):
    '''process linkedin data frame'''
    return linkedin_frame.iloc[::2]


def main():
    '''main function'''
    csv_file_name = '/Users/k/Desktop/Courses/idp/founders_dataset_IDP.csv'
    filter_columns = ['person_name']
    names = pd.read_csv(csv_file_name, usecols=filter_columns)

    twitter_csv_dir = '/Users/k/Desktop/Courses/idp/4000/twitter/'
    linkedin_csv_dir = '/Users/k/Desktop/Courses/idp/4000/linkedin/'
    result_csv_dir = '/Users/k/Desktop/Courses/idp/4000/result-350/'

    # set the minimum wnumber of ords one csv file should contain
    minimum_words_number = 350
    if minimum_words_number is None:
        print('A minimum words number is required. If no restriction exists, set it to 0.')
        sys.exit(1)

    for index, row in names.iterrows():
        name = ''.join(row['person_name'].split(' '))
        twitter_csv_file = twitter_csv_dir + name + '.csv'
        linkedin_csv_file = linkedin_csv_dir + name + '.csv'
        result_csv_file = result_csv_dir + name + '.csv'
        print(f'processing {name} for {index}')
        if os.path.exists(twitter_csv_file) and \
                os.path.exists(linkedin_csv_file):
            twitter_data = read_csv_file(twitter_csv_file)
            linkedin_data = read_csv_file(linkedin_csv_file)
            linkedin_data = process_linkedin(linkedin_data)
            result_data = pd.concat([twitter_data, linkedin_data], axis=0)
            if get_words_number(result_data) >= minimum_words_number:
                result_data.to_csv(result_csv_file, index=False)
        elif os.path.exists(twitter_csv_file):
            twitter_data = read_csv_file(twitter_csv_file)
            if get_words_number(twitter_data) >= minimum_words_number:
                twitter_data.to_csv(result_csv_file, index=False)
        elif os.path.exists(linkedin_csv_file):
            linkedin_data = read_csv_file(linkedin_csv_file)
            linkedin_data = process_linkedin(linkedin_data)
            if get_words_number(linkedin_data) >= minimum_words_number:
                linkedin_data.to_csv(result_csv_file, index=False)
        else:
            continue


if __name__ == '__main__':
    main()
