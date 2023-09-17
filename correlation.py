import os
import json
import re

import numpy as np
import pandas as pd


def merge_dataframe(orinal_csv_path, json_folder_path) -> pd.DataFrame:
    '''merge all csv files in json_folder into one dataframe'''
    personality_information = [
        'openness', 'conscientiousness', 'extraversion',
        'agreeableness', 'neuroticism']
    df = pd.read_csv(orinal_csv_path)
    valid_json_file_count = 0
    for file in os.listdir(json_folder_path):
        person_name = file.split('.')[0]
        person_name = ' '.join(re.findall('[A-Z][^A-Z]*', person_name))
        test_result = json.load(
            open(os.path.join(json_folder_path, file), 'r', encoding='utf-8'))
        if 'personality' in test_result['results'][0]:
            valid_json_file_count += 1
            personality = test_result['results'][0]['personality']
            for _, name in enumerate(personality_information):
                df.loc[df['person_name'] == person_name,
                       name] = personality[name]
    print(
        f'valid json file count: {valid_json_file_count} total length of df: {len(os.listdir(json_folder_path))}')
    return df


if __name__ == '__main__':
    original_csv_path = '/Users/k/Desktop/Courses/idp/founders_dataset_IDP.csv'
    json_folder_path = '/Users/k/Desktop/Courses/idp/4000/json'
    merged_dataframe = merge_dataframe(original_csv_path, json_folder_path)
    merged_dataframe.to_csv('merged_dataframe.csv', index=False)
    print(len(merged_dataframe.dropna()))
