import os
from typing import List
import random

import numpy as np
import pandas as pd


def choose_name_list() -> List[str]:
    '''choose a random name list from file'''
    filepath = '/Users/k/Desktop/Courses/idp/founders_dataset_IDP.csv'
    csv_file = pd.read_csv(filepath)
    company_groups = csv_file.groupby('legal_name')
    # names = list(company_groups.groups.keys())
    company_groups = {name: group for name, group in sorted(
        company_groups.groups.items(),
        key=lambda item: len(item[1]), reverse=True)}
    quota = 200
    person_names = []
    for name, group in company_groups.items():
        person_names.extend(
            csv_file.loc[csv_file['legal_name'] == name].person_name.tolist())
        quota -= len(group)
        if quota <= 0:
            break
    random.shuffle(person_names)
    print('Fatih:', person_names[0:len(person_names) // 3])
    print('Guowen:', person_names[len(person_names) //
          3:len(person_names) // 3 * 2])
    print('Sefat:', person_names[len(person_names) // 3 * 2:])


if __name__ == '__main__':
    choose_name_list()
