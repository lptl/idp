import itertools
import json
import glob
import ntpath
import requests


def receptiviti_send(content: str, person_name: str) -> str:
    '''send content to receptiviti api and return the result'''
    url = 'https://api.receptiviti.com/v1/framework'
    api_key = 'c53719ecf6494a48a9d1ca37396130cc'
    api_secret = 'M0E3R0SBfT+yDfbtwvjhpEePYrKohPNyw8BSnAUNFOeLeAbrupKBhCTy'
    data = json.dumps({
        'request_id': person_name,
        'content': content
    })
    resp = requests.post(url, auth=(api_key, api_secret),
                         data=data, timeout=10)
    return json.dumps(resp.json(), indent=4, sort_keys=True)


def path_leaf(path):
    '''get the file name from path'''
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def main():
    '''main function'''
    data_directory = '/Users/k/Desktop/Courses/idp/4000/txt/'
    json_directory = '/Users/k/Desktop/Courses/idp/4000/json/'
    max_users_number = 1
    txt_file_directory = glob.glob(data_directory + '*.txt')
    for txt_file_name in itertools.islice(txt_file_directory, 0,
                                          max_users_number):
        txt_file = open(txt_file_name, 'r', encoding='utf-8')
        person_name = path_leaf(txt_file_name).split('.')[0]
        json_file_name = json_directory + person_name + '.json'
        content = txt_file.read()
        personality_score = receptiviti_send(content, person_name)
        json_file = open(json_file_name, 'w', encoding='utf-8')
        json_file.write(personality_score)
        txt_file.close()
        json_file.close()
        break  # Add break for testing


if __name__ == '__main__':
    main()
