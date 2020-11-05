import pickle

import pandas as pd

from src.crawler import frame_unpack_by_url, load_council_page_urls
from src.parser import parse


if __name__ == '__main__':
    url = 'http://www.kensakusystem.jp/takatsuki/cgi-bin3/See.exe?Code=izm2vke6bjde8ygf0p'
    res = load_council_page_urls(url)
    with open('res.txt', 'w') as f:
        f.write(repr(res))
    with open('res.pkl', 'wb') as f:
        pickle.dump(res, f)

    for d in res:
        print('\"%s\" の出席議員を取得中...' % d['会の名称'])
        d['attend'] = parse(frame_unpack_by_url(d['HTML']))

    attendance = pd.DataFrame({'council_name': [], 'number': [], 'person_name': []})
    for d in res:
        for person in d['attend']:
            attendance = attendance.append({
                'council_name': d['会の名称'],
                'number': person['number'],
                'person_name': person['name']
            }, ignore_index=True)

    attendance.to_csv('高槻市_20201104収集.csv')
