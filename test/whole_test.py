import unittest

from src.crawler import frame_unpack_by_url
from src.parser import parse
from src.utils import sorted_result


class WholeTest(unittest.TestCase):
    def test_takatsuki(self):
        html_list = frame_unpack_by_url('http://www.kensakusystem.jp/takatsuki/cgi-bin3/ResultFrame.exe?Code=izm2vke6bjde8ygf0p&fileName=R020227A&startPos=0')
        actual = sorted_result(parse(html_list[0]))

        ideal = sorted_result([
            {'number': '1', 'name': '髙島佐浪枝'}, {'number': '2', 'name': '鴻野潔'}, {'number': '3', 'name': '中村明子'},
            {'number': '4', 'name': '市來隼'}, {'number': '5', 'name': '江澤由'}, {'number': '6', 'name': '岡田安弘'},
            {'number': '7', 'name': '甲斐隆志'}, {'number': '8', 'name': '遠矢家永子'}, {'number': '9', 'name': '五十嵐秀城'},
            {'number': '10', 'name': '三井泰之'}, {'number': '11', 'name': '笹内和志'}, {'number': '12', 'name': '竹中健'},
            {'number': '13', 'name': '真鍋宗一郎'}, {'number': '14', 'name': '木本祐'}, {'number': '15', 'name': '森本信之'},
            {'number': '16', 'name': '岡井寿美代'}, {'number': '17', 'name': '出町ゆかり'},
            {'number': '19', 'name': '宮田俊治'}, {'number': '20', 'name': '吉田忠則'}, {'number': '21', 'name': '吉田章浩'},
            {'number': '22', 'name': '平田裕也'}, {'number': '23', 'name': '山口重雄'}, {'number': '24', 'name': '吉田稔弘'},
            {'number': '25', 'name': '強田純子'}, {'number': '26', 'name': '宮本雄一郎'}, {'number': '27', 'name': '川口洋一'},
            {'number': '28', 'name': '北岡隆浩'}, {'number': '29', 'name': '灰垣和美'}, {'number': '30', 'name': '福井浩二'},
            {'number': '31', 'name': '岩為俊'}, {'number': '32', 'name': '久保隆'}, {'number': '33', 'name': '中浜実'},
            {'number': '34', 'name': '中村玲子'}
        ])

        self.assertEqual(ideal, actual)


if __name__ == '__main__':
    unittest.main()
