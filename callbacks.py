import os
import json

import pandas as pd
import plotly.express as px
from dash import dcc, callback
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go


def get_personality_score(name: str, cate: str) -> float:
    '''get the personality score of the person'''
    json_directory = os.environ.get('JSON_DIRECTORY')
    json_file = os.path.join(json_directory, f'{name}.json')
    if not os.path.exists(json_file):
        return None
    category = {'openness': ['artistic', 'adventurous', 'intellectual',
                             'liberal', 'imaginative', 'emotionally_aware'],
                'extraversion': ['sociable', 'friendly', 'assertive',
                                 'active', 'energetic', 'cheerful'],
                'agreeableness': ['generous', 'trusting', 'cooperative',
                                  'empathetic', 'genuine', 'humble'],
                'conscientiousness': ['self_assured', 'organized', 'dutiful',
                                      'disciplined', 'cautious', 'ambitious'],
                'neuroticism': ['anxiety_prone', 'stress_prone', 'melancholy',
                                'self_conscious', 'aggressive', 'impulsive']}
    if cate not in category.keys():
        scores = []
        with open(json_file, 'r', encoding='utf-8') as file:
            content = json.load(file)
            if 'error' in content['results'][0].keys():
                return None
            scores.append(content['results'][0]['personality'][cate])
        return round(sum(scores) / len(scores), 2)
    scores = []
    with open(json_file, 'r', encoding='utf-8') as file:
        content = json.load(file)
        if 'error' in content['results'][0].keys():
            return None
        for item in category[cate]:
            scores.append(content['results'][0]['personality'][item])
    return round(sum(scores) / len(scores), 2)


@ callback(
    Output('personality-score-founding-graph', 'figure'),
    Input('personality-score-category-dropdown', 'value'),
    Input('founding-item-dropdown', 'value'))
def update_personality_score_founding_graph(score_category: str,
                                            founding_item: str) -> go.Figure:
    '''Update the personality score founding graph.'''
    founders_csv_file = os.environ.get('FOUNDERS_CSV')
    content = pd.read_csv(founders_csv_file)
    filter_columns = ['person_name', founding_item]
    content = content[filter_columns]
    content = content.dropna()
    if founding_item == 'num_funding_rounds':
        content[founding_item] = content[founding_item].astype(int)
    elif founding_item == 'total_funding_usd':
        content[founding_item] = content[founding_item].astype(float)
        content[founding_item] = content[founding_item] // 50000000 + 1
        content[founding_item] = content[founding_item].astype(int)
    groups = content.groupby(founding_item)
    x_axis = []
    y_axis = []
    for item, group in groups:
        x_axis.append(item)
        scores = []
        for _, row in group.iterrows():
            person_name = row['person_name'].split('.')[0]
            person_name = ''.join(person_name.split())
            scores.append(get_personality_score(person_name,
                                                score_category))
        scores = [item for item in scores if item is not None]
        score = round(sum(scores) / len(scores), 2) if scores else 0
        y_axis.append(score)
    if founding_item == 'total_funding_usd':
        x_axis = [f'{item * 50}M' for item in x_axis]
    figure = go.Figure(data=go.Bar(x=x_axis, y=y_axis))
    figure.update_layout(title=f'Personality score vs {founding_item}',
                         xaxis_title=f'{founding_item}',
                         yaxis_title='Personality score',
                         font_family='Lucida Sans, sans-serif',
                         font_size=14,
                         title_font_size=16,
                         legend_title_font_size=14,
                         plot_bgcolor='rgb(255,255,255)')
    figure.update_traces(marker_color='#52BE80',
                         marker_line_color='rgb(8,48,107)',
                         marker_line_width=1.5, opacity=0.5,
                         textposition='outside',
                         texttemplate='%{y:.2f}',
                         textfont=dict(family='Lucida Sans, sans-serif',
                                       size=16,
                                       color='rgb(8,48,107)'))
    return figure
