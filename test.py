from typing import List, Dict
import unittest

from main import parse, det_encoding


class TestParse(unittest.TestCase):
    @staticmethod
    def load(path: str) -> str:
        enc = det_encoding(path)
        with open(path, 'r', encoding=enc) as f:
            return f.read()

    @staticmethod
    def sorted_result(res_list: list) -> List[Dict]:
        return sorted(res_list, key=lambda x: x['number'])

    def test_ibaraki(self):
        res = self.sorted_result(parse(self.load('res/ibaraki.html')))
        ideal = self.sorted_result([
            {'number': '1', 'name': '大野幾子'}, {'number': '14', 'name': '上田光夫'},
            {'number': '2', 'name': '塚理'}, {'number': '15', 'name': '大村卓司'},
            {'number': '3', 'name': '長谷川浩'}, {'number': '16', 'name': '青木順子'},
            {'number': '4', 'name': '朝田充'}, {'number': '17', 'name': '松本泰典'},
            {'number': '5', 'name': '大嶺さやか'}, {'number': '18', 'name': '安孫子浩子'},
            {'number': '6', 'name': '畑中剛'}, {'number': '19', 'name': '稲葉通宣'},
            {'number': '7', 'name': '桂睦子'}, {'number': '20', 'name': '友次通憲'},
            {'number': '8', 'name': '小林美智子'}, {'number': '23', 'name': '河本光宏'},
            {'number': '9', 'name': '米川勝利'}, {'number': '24', 'name': '篠原一代'},
            {'number': '10', 'name': '福丸孝之'}, {'number': '25', 'name': '坂口康博'},
            {'number': '11', 'name': '萩原佳'}, {'number': '26', 'name': '上田嘉夫'},
            {'number': '12', 'name': '岩本守'}, {'number': '28', 'name': '辰見登'},
            {'number': '13', 'name': '下野巖'}
        ])
        self.assertListEqual(ideal, res)

    def test_takatsuki(self):
        res = self.sorted_result(parse(self.load('res/takatsuki.html')))
        ideal = self.sorted_result([
            {'number': '1', 'name': '髙島佐浪枝'}, {'number': '2', 'name': '鴻野潔'}, {'number': '3', 'name': '中村明子'},
            {'number': '4', 'name': '市來隼'}, {'number': '5', 'name': '江澤由'}, {'number': '6', 'name': '岡田安弘'},
            {'number': '7', 'name': '甲斐隆志'}, {'number': '8', 'name': '遠矢家永子'}, {'number': '9', 'name': '五十嵐秀城'},
            {'number': '10', 'name': '三井泰之'}, {'number': '11', 'name': '笹内和志'}, {'number': '12', 'name': '竹中健'},
            {'number': '13', 'name': '真鍋宗一郎'}, {'number': '14', 'name': '木本祐'}, {'number': '15', 'name': '森本信之'},
            {'number': '16', 'name': '岡井寿美代'}, {'number': '17', 'name': '出町ゆかり'}, {'number': '18', 'name': '髙木隆太'},
            {'number': '19', 'name': '宮田俊治'}, {'number': '20', 'name': '吉田忠則'}, {'number': '21', 'name': '吉田章浩'},
            {'number': '22', 'name': '平田裕也'}, {'number': '23', 'name': '山口重雄'}, {'number': '24', 'name': '吉田稔弘'},
            {'number': '25', 'name': '強田純子'}, {'number': '26', 'name': '宮本雄一郎'}, {'number': '27', 'name': '川口洋一'},
            {'number': '28', 'name': '北岡隆浩'}, {'number': '29', 'name': '灰垣和美'}, {'number': '30', 'name': '福井浩二'},
            {'number': '31', 'name': '岩為俊'}, {'number': '32', 'name': '久保隆'}, {'number': '33', 'name': '中浜実'},
            {'number': '34', 'name': '中村玲子'}
        ])
        self.assertListEqual(ideal, res)

    def test_wakayama(self):
        res = self.sorted_result(parse(self.load('res/wakayama.html')))
        ideal = self.sorted_result([
            {'number': '1', 'name': '井本有一'}, {'number': '2', 'name': '中村朝人'}, {'number': '3', 'name': '赤松良寛'},
            {'number': '4', 'name': '浜田真輔'}, {'number': '5', 'name': '堀良子'}, {'number': '6', 'name': '西風章世'},
            {'number': '7', 'name': '山中敏生'}, {'number': '8', 'name': '川端康史'}, {'number': '9', 'name': '永野裕久'},
            {'number': '10', 'name': '中庄谷孝次郎'}, {'number': '11', 'name': '山野麻衣子'}, {'number': '12', 'name': '中村元彦'},
            {'number': '13', 'name': '中谷謙二'}, {'number': '14', 'name': '丹羽直子'}, {'number': '15', 'name': '森下佐知子'},
            {'number': '16', 'name': '坂口多美子'}, {'number': '17', 'name': '吉本昌純'}, {'number': '18', 'name': '園内浩樹'},
            {'number': '19', 'name': '中塚隆'}, {'number': '20', 'name': '薮浩昭'}, {'number': '21', 'name': '山本忠相'},
            {'number': '22', 'name': '芝本和己'}, {'number': '23', 'name': '戸田正人'}, {'number': '24', 'name': '松井紀博'},
            {'number': '25', 'name': '井上直樹'}, {'number': '26', 'name': '古川祐典'}, {'number': '27', 'name': '姫田高宏'},
            {'number': '28', 'name': '南畑幸代'}, {'number': '29', 'name': '尾崎方哉'}, {'number': '30', 'name': '奥山昭博'},
            {'number': '31', 'name': '中尾友紀'}, {'number': '32', 'name': '松本哲郎'}, {'number': '33', 'name': '寒川篤'},
            {'number': '34', 'name': '北野均'}, {'number': '35', 'name': '佐伯誠章'}, {'number': '36', 'name': '山本宏一'},
            {'number': '37', 'name': '宇治田清治'}, {'number': '38', 'name': '遠藤富士雄'}
        ])
        self.assertListEqual(ideal, res)

    def test_otsu(self):
        res = self.sorted_result(parse(self.load('res/otsu.html')))
        ideal = self.sorted_result([
            {'number': '1', 'name': '鳥井義徳'}, {'number': '2', 'name': '細川俊行'}, {'number': '3', 'name': '神田健次'},
            {'number': '4', 'name': '出町明美'}, {'number': '5', 'name': '柏木敬友子'}, {'number': '6', 'name': '小島義雄'},
            {'number': '7', 'name': '寺田英幸'}, {'number': '8', 'name': '河村浩史'}, {'number': '9', 'name': '幸光正嗣'},
            {'number': '10', 'name': '西村和典'}, {'number': '11', 'name': '井内律子'}, {'number': '12', 'name': '笠谷洋佑'},
            {'number': '13', 'name': '中田一子'}, {'number': '14', 'name': '谷祐治'}, {'number': '15', 'name': '立道秀彦'},
            {'number': '16', 'name': '林まり'}, {'number': '17', 'name': '草野聖地'}, {'number': '18', 'name': '川口正徳'},
            {'number': '19', 'name': '近藤眞弘'}, {'number': '20', 'name': '八田憲児'}, {'number': '21', 'name': '桐田真人'},
            {'number': '22', 'name': '佐藤弘'}, {'number': '23', 'name': '改田勝彦'}, {'number': '24', 'name': '田中知久'},
            {'number': '25', 'name': '岸本典子'}, {'number': '26', 'name': '杉浦智子'}, {'number': '27', 'name': '仲野弘子'},
            {'number': '28', 'name': '津田新三'}, {'number': '29', 'name': '竹内基二'}, {'number': '30', 'name': '竹内照夫'},
            {'number': '31', 'name': '青山三四郎'}, {'number': '32', 'name': '伴孝昭'}, {'number': '33', 'name': '高橋健二'},
            {'number': '34', 'name': '濱奥修利'}, {'number': '35', 'name': '嘉田修平'}, {'number': '36', 'name': '船本力'},
            {'number': '37', 'name': '奥村功'}, {'number': '38', 'name': '草川肇'}
        ])
        self.assertListEqual(ideal, res)

    def test_hikone(self):
        res = self.sorted_result(parse(self.load('res/hikone.html')))
        ideal = self.sorted_result([
            {'number': '1', 'name': '辻真理子'}, {'number': '13', 'name': '森野克彦'}, {'number': '2', 'name': '中川睦子'},
            {'number': '14', 'name': '林利幸'}, {'number': '3', 'name': '角井英明'}, {'number': '15', 'name': '森田充'},
            {'number': '4', 'name': '獅山向洋'}, {'number': '16', 'name': '小川吉則'}, {'number': '5', 'name': '堀口達也'},
            {'number': '17', 'name': '矢吹安子'}, {'number': '6', 'name': '北川元気'}, {'number': '18', 'name': '赤井康彦'},
            {'number': '7', 'name': '上杉正敏'}, {'number': '19', 'name': '小川隆史'}, {'number': '8', 'name': '中野正剛'},
            {'number': '20', 'name': '黒澤茂樹'}, {'number': '9', 'name': '杉原祥浩'}, {'number': '21', 'name': '伊藤容子'},
            {'number': '10', 'name': '谷口典隆'}, {'number': '22', 'name': '馬場和子'}, {'number': '11', 'name': '和田一繁'},
            {'number': '23', 'name': '長崎任男'}, {'number': '12', 'name': '野村博雄'}, {'number': '24', 'name': '安澤勝'}
        ])
        self.assertListEqual(ideal, res)

    def test_higashiomi(self):
        res = self.sorted_result(parse(self.load('res/higashiomi.html')))
        ideal = self.sorted_result([
            {'number': '1', 'name': '山本直彦'}, {'number': '2', 'name': '青山孝司'}, {'number': '3', 'name': '櫻直美'},
            {'number': '4', 'name': '鈴木則彦'}, {'number': '5', 'name': '辻英幸'}, {'number': '6', 'name': '西村和恭'},
            {'number': '7', 'name': '田井中丈三'}, {'number': '8', 'name': '井上均'}, {'number': '9', 'name': '吉坂豊'},
            {'number': '10', 'name': '森田德治'}, {'number': '11', 'name': '廣田耕康'}, {'number': '12', 'name': '戸嶋幸司'},
            {'number': '13', 'name': '西﨑彰'}, {'number': '14', 'name': '安田高玄'}, {'number': '15', 'name': '西澤由男'},
            {'number': '16', 'name': '西村純次'}, {'number': '17', 'name': '和田喜藏'}, {'number': '18', 'name': '市木徹'},
            {'number': '19', 'name': '山中一志'}, {'number': '20', 'name': '竹内典子'}, {'number': '21', 'name': '大橋保治'},
            {'number': '23', 'name': '田郷正'}, {'number': '24', 'name': '大洞共一'}, {'number': '25', 'name': '西澤善三'}
        ])
        self.assertListEqual(ideal, res)


if __name__ == '__main__':
    unittest.main()
