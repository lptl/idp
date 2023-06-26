import os
import re
import pandas as pd


def remove_urls(line: str) -> str:
    '''remove urls from line'''
    url_regex_pattern = '(?:(?:(?:https?|ftp):)?\/\/)(?:\S+(?::\S*)?@)?(?:(?!(?:10|127)(?:\.\d{1,3}){3})(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))|(?:(?:[a-z0-9\u00a1-\uffff][a-z0-9\u00a1-\uffff_-]{0,62})?[a-z0-9\u00a1-\uffff]\.)+(?:[a-z\u00a1-\uffff]{2,}\.?))(?::\d{2,5})?(?:[/?#]\S*)?'
    return re.sub(url_regex_pattern, '', line)


def remove_mentions(text: str) -> str:
    '''scrub text of @mentions'''
    scrubbed_text = re.sub("@\w+", "", text).strip()
    return scrubbed_text


def process_text(text: str) -> str:
    '''process text'''
    text = text.replace('\n', '')
    text = text.replace('\r', '')
    text = text.replace('\t', '')
    text = remove_urls(text)
    text = remove_mentions(text)
    return text


def main():
    '''main function'''
    data_directory = '/Users/k/Desktop/Courses/idp/4000/result-350/'
    txt_directory = '/Users/k/Desktop/Courses/idp/4000/txt/'
    for csv_file_name in os.listdir(data_directory):
        person_name = csv_file_name.split('.')[0]
        csv_path = data_directory + csv_file_name
        data = pd.read_csv(csv_path)
        txt_file_name = txt_directory + person_name + '.txt'
        txt_file = open(txt_file_name, 'w', encoding='utf-8')
        for _, row in data.iterrows():
            txt_file.write(process_text(row['text']))
            txt_file.write('\n')
        txt_file.close()


if __name__ == '__main__':
    main()
