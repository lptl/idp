import os
import json
import re
from typing import List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plot
from scipy.stats import f_oneway, pointbiserialr, spearmanr, kruskal, alexandergovern
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split


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


def machine_learning_analysis(feature_columns: List[str], target_column: str, csv_file_path: str) -> None:
    '''use machine learning methods to analyze the correlation between feature and target'''
    csv_file = pd.read_csv(csv_file_path)
    csv_file = csv_file[csv_file[target_column].notna()]
    target_frame = csv_file[target_column].tolist()
    feature_frame = csv_file[feature_columns]
    for feature_column in feature_columns:
        feature_frame[feature_column] = feature_frame[feature_column].astype(
            'category').cat.codes
    feature_frame = feature_frame.astype('int64').to_numpy().tolist()
    feature_train, feature_test, target_train, target_test = train_test_split(
        feature_frame, target_frame, test_size=0.2, random_state=0)
    # Guowen: Decision Tree
    decision_tree_regressor = DecisionTreeRegressor()
    decision_tree_regressor.fit(feature_train, target_train)
    print(
        f'Decision Tree Accuracy: {decision_tree_regressor.score(feature_test, target_test)}')
    # Guowen: Neural Network
    neural_network_regressor = MLPRegressor(
        hidden_layer_sizes=(1000, 1000, 1000), max_iter=10000, verbose=True)
    neural_network_regressor.fit(feature_train, target_train)
    print(
        f'Neural Network Accuracy: {neural_network_regressor.score(feature_test, target_test)}')
    print(neural_network_regressor.loss_curve_)


def correlation_analysis_categorical_numeric(categorical_column_name: str, numeric_column_name: str, csv_file_path: str) -> None:
    '''use multiple methods to analyze the correlation between categorical and numeric data'''
    # Reference: http://www.sefidian.com/2020/08/02/measure-the-correlation-between-numerical-and-categorical-variables-and-the-correlation-between-two-categorical-variables-in-python-chi-square-and-anova/

    csv_file = pd.read_csv(csv_file_path)
    csv_file = csv_file[csv_file[numeric_column_name].notna()]
    # Remove non_binary and bigender rows, which only have 2 and 1 rows respectively
    if categorical_column_name == 'gender':
        csv_file = csv_file[(csv_file[categorical_column_name] !=
                            'non_binary') & (csv_file[categorical_column_name] != 'bigender')]
    categorical_column = csv_file[categorical_column_name]
    categories = categorical_column.unique()
    print(
        f'category_number/total_person: {len(categories)}/{len(categorical_column)} categories: {categories}')
    numeric_column = csv_file[numeric_column_name]

    category_numeric_frame = csv_file[[
        categorical_column_name, numeric_column_name]]

    # Guowen: ANOVA, analysis of variance
    print('\nANOVA: If the p-value < 0.05, we can reject the null hypothesis, which means that the two columns are correlated.')
    print('The smaller the p-value is, the stronger the correlation is.')
    category_numeric_list = category_numeric_frame.groupby(
        categorical_column_name)[numeric_column_name].apply(list)
    f, p = f_oneway(*category_numeric_list)
    print(f'groups: {len(category_numeric_list)} f-value: {f} p-value: {p}\n')

    # Guowen: Kruskal analysis if the ANOVA preassumptions are not met
    print('Kruskal-Wallis: How to analyze the values of the Kruskal-Wallis test?')
    h, p = kruskal(*category_numeric_list)
    print(f'groups: {len(category_numeric_list)} h-value: {h} p-value: {p}\n')

    # Guowen: Alexander Govern test
    print('Alexander Govern: How to analyze the values of the Alexander Govern test?')
    result = alexandergovern(*category_numeric_list)
    print(
        f'groups: {len(category_numeric_list)} a-value: {result.statistic} p-value: {result.pvalue}\n')

    # Guowen: box plot analysis
    print('Boxplot: If the data are weakly correlated, the boxes will be mostly overlapped with each other.')
    box_plot = category_numeric_frame.boxplot(
        numeric_column_name, by=categorical_column_name)
    box_plot.get_figure().savefig('box_plot_' + categorical_column_name +
                                  '_' + numeric_column_name + '.png')
    print('box plot saved\n')

    # Guowen: spearman correlation
    # Reference: https://machinelearningmastery.com/how-to-use-correlation-to-understand-the-relationship-between-variables/
    print('Spearman: If the correlation is close to 0, it means that the two columns are not correlated.')
    categorical_column = categorical_column.replace(
        {key: value for value, key in enumerate(categories)})  # takes encoding of the categories
    spearman_correlation = spearmanr(categorical_column, numeric_column)
    correlation, p_value = spearman_correlation.correlation, spearman_correlation.pvalue
    print(
        f'correlation: {correlation} p-value: {p_value}\n')

    # Guowen: if the categorical column is binary, we can use point biserial correlation
    if len(categories) == 2:
        print('Pointbiserial: If the coefficient is close to 0, it means that the two columns are not correlated.')
        categorical_column = categorical_column.replace(
            {categories[0]: 0, categories[1]: 1})
        point_biserial_correlation = pointbiserialr(
            categorical_column, numeric_column)
        print(
            f'coefficient {point_biserial_correlation.correlation} p-value {point_biserial_correlation.pvalue}\n')


if __name__ == '__main__':
    # Guowen: This part is to produce merged csv_file, combining the personality score and the original csv file
    # original_csv_path = '/Users/k/Desktop/Courses/idp/founders_dataset_IDP.csv'
    # json_folder_path = '/Users/k/Desktop/Courses/idp/4000/json'
    # merged_dataframe = merge_dataframe(original_csv_path, json_folder_path)
    # merged_dataframe.to_csv('merged_dataframe.csv', index=False)
    # print(len(merged_dataframe.dropna()))

    # Guowen: This part is to produce the correlation analysis between categorical and numeric data
    # The categorical columns include: status, city, employee_count, is_current, title, job_type, gender
    # The numberic columns include: openness, conscientiousness, extraversion, agreeableness, neuroticism
    # We don't consider other numeric columns because we only do personality analysis here
    # correlation_analysis_categorical_numeric(
    #     'job_type', 'agreeableness', 'merged_dataframe.csv')
    # The initial experiment shows that different personality scores have different correlation with
    # different categorial columns, for example, agreeableness and gender have a strong correlation

    # Guowen: This part is to produce the machine learning analysis between feature and target
    # The feature columns include: openness, conscientiousness, extraversion, agreeableness, neuroticism
    # The target columns include: status, city, employee_count, is_current, title, job_type, gender
    machine_learning_analysis(['gender'],
                              'openness', 'merged_dataframe.csv')
