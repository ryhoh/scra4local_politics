import sys
import time
from urllib.parse import urlparse, urljoin
import re
from typing import List, Dict, Union, Iterable

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import bs4

from src import utils


def load_council_page_urls(entry_url: str) -> List[Dict[str, str]]:
    r"""
    「会議録の閲覧」ページからスタートして，全ての会議日程について，そのページへのリンクを見つけ，URLを取得する．
    （高槻市なら http://www.kensakusystem.jp/takatsuki/cgi-bin3/See.exe?Code=izm2vke6bjde8ygf0p からスタート）

    会議録の閲覧ページは，以下の構造を想定している．

    - 会議録の閲覧ページ
        - 年度のかたまり："平成28年～令和2年", "平成22年～平成27年" ...
            - 年度："令和2年", "令和元年", ...
                - 定例会・臨時会："令和 2年 第1回定例会", ...
                    - 日程："（第1日 2月27日）", ...

    これを木構造に例えるなら，この関数は深さ優先探索のようにして，1つずつ末端の URL を取得していく

    :param entry_url: 「会議録の閲覧」ページの URL
    :return: リスト[辞書(会議・日程の名前とリンク)]
    """

    def open_year_sets():
        target_alts = []
        body = browser.find_element_by_xpath('/html/body')
        a_tags = body.find_elements(By.XPATH, '//a')
        for tag in a_tags:
            children = tag.find_elements(By.XPATH, '*')
            for child in children:  # a タグの中身を走査
                if child.tag_name == 'img':
                    alt = child.get_attribute('alt').replace(' ', '').replace('　', '')
                    if re.fullmatch(re_year_set_pat, alt):  # "平成22年～平成27年", "平成28年～" を狙う
                        target_alts.append(alt)

        for target_alt in target_alts:
            body = browser.find_element_by_xpath('/html/body')
            a_tags = body.find_elements(By.XPATH, '//a')
            for tag in a_tags:
                children = tag.find_elements(By.XPATH, '*')
                for child in children:  # a タグの中身を走査
                    if child.tag_name == 'img':
                        alt = child.get_attribute('alt').replace(' ', '').replace('　', '')
                        if alt == target_alt:
                            tag.click()  # これで，"令和 2年" などの，年度のリストが現れる
                            open_years()  # この状態で，定例会・臨時会の一覧を開ける
                            browser.back()
                            break
                else:
                    continue
                break

    def open_years():
        target_alts = []
        body = browser.find_element_by_xpath('/html/body')
        a_tags = body.find_elements(By.XPATH, '//a')
        for tag in a_tags:
            children = tag.find_elements(By.XPATH, '*')
            for child in children:  # a タグの中身を走査
                if child.tag_name == 'img':
                    alt = child.get_attribute('alt').replace(' ', '').replace('　', '')
                    if '～' not in alt and alt.endswith('年'):  # "令和 2年", "平成31年" ... を狙う
                        target_alts.append(alt)

        for target_alt in target_alts:
            body = browser.find_element_by_xpath('/html/body')
            a_tags = body.find_elements(By.XPATH, '//a')
            for tag in a_tags:
                children = tag.find_elements(By.XPATH, '*')
                for child in children:  # a タグの中身を走査
                    if child.tag_name == 'img':
                        alt = child.get_attribute('alt').replace(' ', '').replace('　', '')
                        if alt == target_alt:
                            tag.click()  # これで "令和 2年 第1回定例会" などのリストが現れる
                            open_councils()  # この状態で，定例会・臨時会の日程一覧を開ける
                            browser.back()
                            break
                else:
                    continue
                break

    def open_councils():
        target_names = []
        body = browser.find_element_by_xpath('/html/body')
        a_tags = body.find_elements(By.XPATH, '//a')
        for tag in a_tags:
            if re.fullmatch(re_council_pat, tag.text):
                target_names.append(tag.text)

        for target_name in target_names:
            body = browser.find_element_by_xpath('/html/body')
            a_tags = body.find_elements(By.XPATH, '//a')
            for tag in a_tags:
                if tag.text == target_name:
                    tag.click()  # これで，（第1日 2月27日）" などのリストが現れる
                    open_date(target_name)  # この状態で，各日程ページの HTML を取りに行く
                    browser.back()
                    break

    def open_date(council_name: str):
        body = browser.find_element_by_xpath('/html/body')
        a_tags = body.find_elements(By.XPATH, '//a')
        for tag in a_tags:
            if re.fullmatch(re_date_pat, tag.text):
                date_name = tag.text.replace(' ', '').replace('　', '')
                results.append({
                    '会の名称': '%s%s' % (council_name, date_name),
                    'HTML': tag.get_attribute('href')
                })
                print('\"%s%s\" を取得' % (council_name, date_name))

    re_date_pat = re.compile(r'.*月.*日.*')
    re_council_pat = re.compile(r'.*(定例|臨時)会')
    re_year_set_pat = re.compile(r'.*年～?')

    results: List[Dict[str, str]] = []
    browser = utils.new_selenium()
    browser.get(entry_url)
    try:
        open_year_sets()
    finally:  # 失敗しても，それまでに取った分を返す
        return results


def frame_unpack_by_url(entry_url: str) -> str:
    r"""
    与えられた URL から，フレームを展開してコンテンツのページの HTML を返す
    :param entry_url: 開くページの URL
    :return: コンテンツページの HTML (str)
    """
    parsed_url = urlparse(entry_url)
    result = parsed_url.geturl()

    while True:
        current_url = result
        html = get_by_url(current_url)
        soup = bs4.BeautifulSoup(html, 'html.parser')
        time.sleep(5)  # DoS 攻撃にならないよう，待つ

        # フレームページだった場合
        frames = soup.find_all('frame')
        if len(frames) == 0:
            result = html
            break
        else:
            result = urljoin(current_url, frames[1]['src'])  # frame を使うなら，普通は要素2つ以上，IndexError はないはず

    return result


def find_frame_src(html: str) -> Union[str, None]:
    r"""
    与えられた HTML にフレームがあるかチェックして，あれば展開してコンテンツのページの URL を返す．
    なければ None を返す．
    :param html: 開くページの HTML
    :return: コンテンツページの URL または None （フレームがなかった場合）
    """
    soup = bs4.BeautifulSoup(html, 'lxml')
    frames = soup.find_all('frame')
    if len(frames) == 0:
        return None
    else:
        return frames[1]['src']  # frame を使うなら，普通は要素2つ以上，IndexError はないはず


def get_by_url(url: str, do_wait: bool = True, do_frame_unpack: bool = True) -> str:
    r"""
    :param url: HTTP GETメソッドを発行したいURL
    :param do_wait: サーバに負荷をかけないために，待ち時間を設けるか
    :param do_frame_unpack: 取得したページが Frameset で構成されていた時，それを展開してさらに GET を行うか
    :return: 受け取った HTML を適切な文字コードで読み込んだ文字列
    """
    if do_wait:
        time.sleep(10)  # 負荷をかけないため

    response = requests.get(url)
    sys.stderr.write('[GET {}] {}\n'.format(response.status_code, url))
    if response.status_code % 100 in (4, 5):
        raise ValueError('got status code {} at {}'.format(response.status_code, url))

    html = utils.safe_decode(response.content)
    if do_frame_unpack:
        frame_src = find_frame_src(html)
        if frame_src is not None:
            next_url = urljoin(url, frame_src)
            html = get_by_url(next_url, do_wait=False)  # 人間がブラウジングする時は待ち時間なしで取得するので，それに倣う

    return html


if __name__ == '__main__':
    # print(frame_unpack('http://www.kensakusystem.jp/takatsuki/cgi-bin3/ResultFrame.exe?Code=izm2vke6bjde8ygf0p&fileName=R020227A&startPos=0'))
    takatsuki_url = 'http://www.kensakusystem.jp/takatsuki/cgi-bin3/See.exe?Code=izm2vke6bjde8ygf0p'
    res = load_council_page_urls(takatsuki_url)
    print(repr(res))
    with open('res.txt', 'w') as f:
        f.write(repr(res))
