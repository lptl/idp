'''the layout of the dashboard'''
from dash import dcc, html
from style import TABS_STYLE, TAB_SELECTED_STYLE, TAB_STYLE


def get_basic_visualization_tab() -> dcc.Tab:
    '''get the basic visualization tab, has no personality score'''
    return dcc.Tab(label='Basic', children=[], style=TAB_STYLE,
                   selected_style=TAB_SELECTED_STYLE)


def get_personality_score_visualization_tab() -> dcc.Tab:
    '''get the personality score visualization tab'''
    return dcc.Tab(label='Personality', children=[
        get_personality_score_founding_part(),
        get_personality_city_status_category_part()
    ], style=TAB_STYLE, selected_style=TAB_SELECTED_STYLE)


def get_personality_score_founding_part() -> html.Div:
    '''get the founding part of the personality score visualization tab'''
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
    items = []
    for cate in category.keys():
        items.extend(category[cate])
    # items = list(category.keys())
    return html.Div([
        html.H3('Personality score and founding relevance', style={
            'text-align': 'center', 'margin-bottom': '20px',
            'font-size': '18px'}),
        html.Div([
            dcc.Dropdown(id='personality-score-category-dropdown',
                         placeholder='Personality category',
                         options=items,
                         clearable=False,
                         value=items[0],
                         style={'width': '50%', 'display': 'inline-block'}),
            dcc.Dropdown(id='founding-item-dropdown',
                         placeholder='Founding category',
                         options=['num_funding_rounds', 'total_funding_usd'],
                         clearable=False,
                         value='num_funding_rounds',
                         style={'width': '50%', 'display': 'inline-block'})],
                 style={'width': '100%', 'display': 'inline-block'}),
        dcc.Graph(id='personality-score-founding-graph')],
        style={'width': '80%', 'padding': '0 20',
               'margin': '0 auto', 'text-align': 'center',
               'margin-top': '20px', 'margin-bottom': '40px'})


def get_personality_city_status_category_part() -> html.Div:
    '''get the city status category part'''
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
    items = []
    # for cate in category.keys():
    #     items.extend(category[cate])
    items = list(category.keys())
    return html.Div([
        html.H3('Personality score and city/status/category/employee', style={
            'text-align': 'center', 'margin-bottom': '20px',
            'font-size': '18px'}),
        html.Div([
            dcc.Dropdown(id='personality-score-category-dropdown-2',
                         placeholder='Personality category',
                         options=items,
                         clearable=False,
                         value=items[0],
                         style={'width': '50%', 'display': 'inline-block'}),
            dcc.Dropdown(id='city-status-category-dropdown',
                         placeholder='Founding category',
                         options=['city', 'status', 'category_groups_list',
                                  'employee_count'],
                         clearable=False,
                         value='status',
                         style={'width': '50%', 'display': 'inline-block'})],
                 style={'width': '100%', 'display': 'inline-block'}),
        dcc.Graph(id='personality-score-city-status-category-graph',
                  style={'height': '500px'})],
        style={'width': '80%', 'padding': '0 20',
               'margin': '0 auto', 'text-align': 'center',
               'margin-top': '20px', 'margin-bottom': '40px'})


def get_layout() -> html.Div:
    '''Get the layout of the dashboard.'''
    return html.Div([
        dcc.Tabs([
            get_basic_visualization_tab(),
            get_personality_score_visualization_tab(),
        ], style=TABS_STYLE)
    ], style={'font-family': 'Libertinus Sans, sans-serif'})
