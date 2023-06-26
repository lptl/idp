import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from wordcloud import WordCloud


# print(matplotlib.get_cachedir())
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Lucida Sans']
rcParams['font.size'] = 10


def get_words_number(data_frame: pd.DataFrame) -> int:
    '''Get the number of words in a pandas dataframe'''
    words_number = 0
    data_frame.rename(columns={'0': 'text'}, inplace=True)
    for _, row in data_frame.iterrows():
        words_number += len(row['text'].split(' '))
    return words_number


def read_csv(csv_path) -> pd.DataFrame:
    '''Read csv file and return a pandas dataframe'''
    data = pd.read_csv(csv_path)
    return data


def words_number_scatter() -> None:
    '''Plot the distribution of words number in the csv files'''
    folder_path = '/Users/k/Desktop/Courses/idp/4000/result-350/'
    words_number_list = []
    for csv_file in os.listdir(folder_path):
        csv_file_path = folder_path + csv_file
        data = read_csv(csv_file_path)
        words_number_list.append(get_words_number(data))
    x = range(len(words_number_list))
    fig, ax = plt.subplots()
    ax.scatter(x, words_number_list, alpha=0.5)
    ax.grid()
    ax.set(xlabel='index', ylabel='words number',
           title='Words number scatter plot')
    fig.savefig("figures/words_number_scatter.png")
    # plt.show()


def words_number_bar() -> None:
    '''Plot the distribution of words number in the csv files'''
    folder_path = '/Users/k/Desktop/Courses/idp/4000/result-350/'
    words_number_list = [0 for _ in range(8)]
    for csv_file in os.listdir(folder_path):
        csv_file_path = folder_path + csv_file
        data = read_csv(csv_file_path)
        words_number = get_words_number(data)
        index = (words_number - 350) // 400
        index = index if index < 8 else 7
        words_number_list[index] += 1
    print(words_number_list)
    bar_names = ['350-750', '750-1150', '1150-1550',
                 '1550-2000', '2000-2400', '2400-2800',
                 '2800-3200', '3200-']
    bar_colors = ['plum', 'DarkSeaGreen', 'indianred',
                  'dodgerblue', 'green', 'tan', 'palegreen', 'cadetblue']
    fig, ax = plt.subplots()
    ax.bar(bar_names, words_number_list, color=bar_colors, alpha=1.0)
    ax.grid()
    ax.set(xlabel='words number range', ylabel='frequency',
           title='Words number bar plot')
    fig.savefig("figures/words_number_bar.png", dpi=600)
    plt.show()


def validate_word(word: str) -> bool:
    '''Validate the word'''
    if len(word) < 3:
        return False
    if 'https' in word or 'http' in word or 'www' in word:
        return False
    if word == 'one' or word == '&amp;' or word == 'Thank':
        return False
    return True


def word_cloud() -> None:
    '''Plot the word cloud of the csv files'''
    folder_path = '/Users/k/Desktop/Courses/idp/4000/result-350/'
    words_file = '/Users/k/Desktop/Courses/idp/idp/words.txt'
    with open(words_file, 'w', encoding='utf-8') as f:
        f.write('')
    for csv_file in os.listdir(folder_path):
        words = []
        csv_file_path = folder_path + csv_file
        data = read_csv(csv_file_path)
        for _, row in data.iterrows():
            current_words = row['text'].split(' ')
            for word in current_words:
                if validate_word(word):
                    words.append(word)
        with open(words_file, 'a', encoding='utf-8') as f:
            f.write(' '.join(words))
    content = open(words_file, 'r', encoding='utf-8').read()
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          min_font_size=5).generate(content)
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig("figures/word_cloud.png", dpi=600)
    # plt.show()


if __name__ == '__main__':
    # words_number_scatter()
    words_number_bar()
    # word_cloud()
