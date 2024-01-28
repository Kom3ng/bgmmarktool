import time

import requests as req

TOKEN = input('access token:')
API_URL = 'https://api.bgm.tv'
USER_ID = input('user id:')
LIMIT = 30
headers = {'Authorization': 'Bearer ' + TOKEN,
           'user-agent': 'kom3ng/mirai-bangumi (https://github.com/kom3ng/mirai-bangumi)',
           'Content-Type': 'application/json'}
total = \
    req.get(API_URL + '/v0/users/' + USER_ID + '/collections', {'subject_type': 2, 'type': 2, 'limit': 1},
            headers=headers).json()[
        'total']

for i in range(total // LIMIT + 1):
    p = req.get(API_URL + '/v0/users/' + USER_ID + '/collections',
                {'subject_type': 2, 'type': 2, 'limit': LIMIT, 'offset': i * LIMIT}, headers=headers).json()

    for subject in p['data']:
        print('查找 ' + subject['subject']['name'])
        subjectId = subject['subject_id']
        relates = req.get(API_URL + '/v0/subjects/' + str(subjectId) + '/subjects', headers=headers).json()

        for relate in relates:
            if relate['type'] != 3:
                continue
            relation = relate['relation']
            if relation != '原声集' and relation != '片头曲' and relation != '片尾曲':
                continue
            print('收藏 ' + relate['name'])
            req.post(API_URL + '/v0/users/-/collections/' + str(relate['id']), data="{\"type\": 2}",
                     headers=headers)
            time.sleep(0.5)
