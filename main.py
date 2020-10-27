import sys
import re
from typing import List

from chardet.universaldetector import UniversalDetector
import mojimoji


def replace_empty_line(lines: str) -> str:
    r"""
    :param lines: 文字列
    :return: lines 内の空行を取り除いた文字列
    """
    # 改行文字が LF か CR+LF かはデータによるが，ここで LF に統一する
    lines = lines.replace('\r\n', '\n')

    # 空行 = "\n\n" or "\r\n\r\n"
    while '\n\n' in lines:  # 効率が悪い可能性があるが，改良は後回し
        lines = lines.replace('\n\n', '\n')
    return lines


def parse(html_string: str) -> List[dict]:
    r"""
    :param html_string: htmlのソース
    :return: list(dict(number: 議員番号, name: 氏名), …)

    作戦：和歌山市のようなフォーマットに一度揃える
        要件1: 空行を含まないこと
        要件2: <br>タグではなく，改行コードで行の終わりを明示
    """
    # フォーマット変更ここから
    br_line_pattern = re.compile('( |　)*<(br|BR|br /|BR /)>( |　)*')  # 改行タグと空白のみ
    html_string = re.sub(br_line_pattern, '', html_string)  # からなる行を取り除く
    html_string = replace_empty_line(html_string)
    # フォーマット変更終わり

    re_res = re.search(r'出席.*', html_string)
    html_string = html_string[re_res.start():]  # 「出席」が含まれる行を開始地点とする

    member_list = []
    for row in html_string.split('\n')[1:]:  # 最初の行はいらない
        if '番' not in row or re.fullmatch(r'　*(―|－)+', row):
            break  # '番'が含まれない行，全角または半角のハイフン用いた水平線が終わりを表すと仮定
        ban_count = row.count('番')

        if ban_count == 2:
            pivot = row.rfind('番') - 2  # 2番目の「番」より2文字前まであたりを境界に，前後に名前がある
            member_list.append(row[:pivot])
            member_list.append(row[pivot:])
        elif ban_count == 1:
            member_list.append(row)
        else:  # 1行に3個以上の氏名がある場合は，ひとまず考えない
            sys.stderr.write('「番」の数が %d 個あり，対処できない\n' % ban_num)
            assert True

    member_list = list(map(lambda x: x.replace('　', '').replace(' ', ''), member_list))

    # 番号を取り除く
    member_list_without_nb = []
    for member in member_list:
        re_res = re.search(r'[0-9|０-９]+番', member)
        number = mojimoji.zen_to_han(member[re_res.start(): re_res.end() - 1])  # '番'を落とす -1
        name = member[re_res.end():]

        if name.endswith('議員'):
            name = name[:-2]
        elif name.endswith('君'):
            name = name[:-1]
        elif name.endswith('さん'):
            name = name[:-2]

        member_list_without_nb.append({
            'number': number,
            'name':   name,
        })

    return member_list_without_nb

def det_encoding(file_path: str) -> str:
    detector = UniversalDetector()

    with open(file_path, mode='rb') as f:
        for binary in f:
            detector.feed(binary)
            if detector.done:
                break
    detector.close()

    return detector.result['encoding']


def det_encoding_by_bytes(html_bytes: bytes) -> str:
    detector = UniversalDetector()
    for binary in html_bytes:
        detector.feed(binary)
        if detector.done:
            break
    detector.close()

    return detector.result['encoding']


if __name__ == '__main__':
    # path = 'res/ibaraki.html'
    # path = 'res/takatsuki.html'
    # path = 'res/wakayama.html'
    # path = 'res/otsu.html'
    path = 'res/hikone.html'
    enc = det_encoding(path)
    with open(path, 'r', encoding=enc) as f:
        print(parse(f.read()))
