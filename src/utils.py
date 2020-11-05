import sys
from urllib3.exceptions import MaxRetryError
import traceback
from typing import Union, List, Dict

from selenium import webdriver
from chardet import UniversalDetector
import nkf


def det_encoding(file: Union[str, bytes]) -> str:
    r"""
    :param file: 文字コードを判定したいファイルのパス(str)，またはそれを読み込んだバイナリ(bytes)
    :return: 判定結果の文字コード
    """
    # バイナリに揃えて処理
    if isinstance(file, str):
        with open(file, mode='rb') as f:
            binary = f.read()
    elif isinstance(file, bytes):
        binary = bytes(file)
    else:
        raise TypeError('func det_encoding receives str or bytes, but given {}.'.format(file.__class__))

    # 2つの方法で文字コード判定
    # 1. chardet.UniversalDetector
    detector = UniversalDetector()
    detector.feed(binary)
    detector.close()
    chardet_res = detector.result['encoding'].lower()

    # 2. nkf
    nkf_res = nkf.guess(binary).lower()

    # 時々，2つの結果が食い違っていたりするが，どうにかして片方を選ぶ
    if chardet_res != nkf_res:
        sys.stderr.write('[warning] conflict char_codes: %s vs %s ' % (chardet_res,  nkf_res))
        if 'cp932' in {chardet_res, nkf_res}:
            sys.stderr.write('-> choosing CP932...\n')
            return 'CP932'  # 暫定的に，CP932の可能性がある時はCP932にしておく
        elif 'shift_jis' in {chardet_res, nkf_res}:
            sys.stderr.write('-> choosing Shift_JIS...\n')
            return 'Shift_JIS'  # 次に，Shift_JISの可能性がある時はShift_JISにしておく
        else:
            raise ValueError("現在扱えない文字コードで書かれたファイル：", file)
    return chardet_res


def safe_decode(file: Union[str, bytes]) -> str:
    r"""
    ファイルまたはバイナリに対して，文字コードがわからない状態から，判定-読込までする関数
    :param file: 開きたいファイルのパス(str)，またはそれを読み込んだバイナリ(bytes)
    :return: 読み込まれた（デコードされた）状態の文字列
    """
    enc = det_encoding(file)
    if isinstance(file, str):
        with open(file, mode='rb') as f:
            binary = f.read()
    elif isinstance(file, bytes):
        binary = bytes(file)
    else:
        raise TypeError('func safe_encode receives str or bytes, but given {}.'.format(file.__class__))

    return binary.decode(encoding=enc)


def new_selenium() -> webdriver.Remote:
    r"""
    新しい selenium driver を作って返す
    :return: selenium driver
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    try:
        driver = webdriver.Remote(
            command_executor='http://localhost:65000/wd/hub',
            desired_capabilities=options.to_capabilities(),
            options=options,
        )
    except MaxRetryError:
        sys.stderr.write(traceback.format_exc() + '\n')
        raise RuntimeError('The docker container might be dead!')

    driver.implicitly_wait(10)

    return driver


def sorted_result(res_list: list) -> List[Dict]:
    r"""
    :param res_list: 出席議員を表す dict(議員番号, 氏名) のリスト
    :return: 与えられたリストを議員番号順にソートしたもの
    """
    return sorted(res_list, key=lambda x: int(x['number']))
