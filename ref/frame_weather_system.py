import os
import sys
import json

import requests
import json
from datetime import date, datetime, timedelta, time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram_bot import TelegramBot

from da_concept_extractor import DA_Concept
from ReadPresetData import ReadPresetData

class FrameWeatherSystem:

    # 地方リスト
    prefs = ['三重', '京都', '佐賀', '兵庫', '北海道', '千葉', '和歌山', '埼玉', '大分',
             '大阪', '奈良', '宮城', '宮崎', '富山', '山口', '山形', '山梨', '岐阜', '岡山',
             '岩手', '島根', '広島', '徳島', '愛媛', '愛知', '新潟', '東京',
             '栃木', '沖縄', '滋賀', '熊本', '石川', '神奈川', '福井', '福岡', '福島', '秋田',
             '群馬', '茨城', '長崎', '長野', '青森', '静岡', '香川', '高知', '鳥取', '鹿児島']

    # 情報種別のリスト
    ## 料理種別のリスト
    with open('./src/genre.txt', 'r') as f:
        data = f.readlines()
    genre = [i.split()[0] for i in data]
    ## 地域(県)種別のリスト
    with open('src/pref_code.json', 'r', encoding='utf-8') as f:
        pref_code_list = json.load(f)

    # 状態遷移リスト
    frame_phase = []
    frame_type = []
    with open('./src/frame.txt', 'r') as f:
        a = f.readlines()
        for i in a:
            txt = i.split('\t')
            frame_phase.append(txt[0])
            frame_type.append(txt[1].split()[0])

    # システムの対話行為とシステム発話を紐づけた辞書
    uttdic = {"open-prompt": "ご用件をどうぞ",
            "ask-place": "地名を言ってください",
            "ask-genre": "何が食べたいですか?"}

    urls = 'https://api.gnavi.co.jp/RestSearchAPI/v3/'
    telegram_key =  os.environ['TELEGRAM_API']# 自身のAPPIDを入れてください    
    gurunavi_key =  os.environ['GURUNAVI_API_KEY']
    def __init__(self):
        # 対話セッションを管理するための辞書
        self.sessiondic = {}
        # 対話行為タイプとコンセプトを抽出するためのモジュールの読み込み
        self.da_concept = DA_Concept()
    
    def get_restrant(self, genre, pref_code):
        r = requests.get(self.urls, params = {'keyid': self.gurunavi_key, 'freeword': genre, 'pref': pref_code})
        total_hit_count = r.json()['total_hit_count']
        rest_info = {}
        for i in range(len(r.json()['rest'])):
            rest_info[f"rest{i}"] = {}
            rest_info[f"rest{i}"]['name'] = r.json()['rest'][i]['name']
            rest_info[f"rest{i}"]['latitude'] = r.json()['rest'][i]['latitude']
            rest_info[f"rest{i}"]['longitude'] = r.json()['rest'][i]['longitude']
            rest_info[f"rest{i}"]['url'] = r.json()['rest'][i]['url']
            rest_info[f"rest{i}"]['url_mobile'] = r.json()['rest'][i]['url_mobile']
            rest_info[f"rest{i}"]['address'] = r.json()['rest'][i]['address']
            rest_info[f"rest{i}"]['tel'] = r.json()['rest'][i]['tel']
            rest_info[f"rest{i}"]['opentime'] = r.json()['rest'][i]['opentime']
            rest_info[f"rest{i}"]['holiday'] = r.json()['rest'][i]['holiday']
        
        rest_data = {}
        rest_data['total_hit_count'] = total_hit_count
        rest_data['rest_info'] = rest_info
        return rest_data

    def get_pref_code(self, pref):
        for i in self.pref_code_list:
            if pref in i['name']:
                return i['pref']
        return None

    def genre2ID(self, genre):
        genres = ReadPresetData().ReadTxt('./src/genre.txt')
        for item in genres:
            if genre in item[1]:
                return {'id': item[0]}
        
        return {'id': None}

    # 発話から得られた情報をもとにフレームを更新
    def update_frame(self, frame, da, conceptdic):
        # 値の整合性を確認し，整合しないものは空文字にする
        for k,v in conceptdic.items():
            if k == "place" and v not in self.prefs:
                conceptdic[k] = ""
            elif k == "genre" and v not in self.genre:
                conceptdic[k] = ""
        if da == "request-restrante":
            for k,v in conceptdic.items():
                # コンセプトの情報でスロットを埋める
                frame[k] = v
        elif da == "initialize":
            frame = {"place": "", "genre": ""}
        elif da == "correct-info":
            for k,v in conceptdic.items():
                if frame[k] == v:
                    frame[k] = ""
        return frame

    # フレームの状態から次のシステム対話行為を決定
    def next_system_da(self, frame):
        bit = ''
        for i in frame.values():
            if i == '':
                bit += '0'
            else:
                bit += '1'
        return self.frame_type[int(bit,2)]
        # # すべてのスロットが空であればオープンな質問を行う
        # if frame["place"] == "" and frame["genre"] == "":
        #     return "open-prompt"
        # # 空のスロットがあればその要素を質問する
        # elif frame["place"] == "":
        #     return "ask-place"
        # elif frame["genre"] == "":
        #     return "ask-genre"
        # else:
        #     return "tell-info"

    def initial_message(self, input):
        text = input["utt"]
        sessionId = input["sessionId"]

        # セッションIDとセッションに関連する情報を格納した辞書
        self.sessiondic[sessionId] = {"frame": {"place": "", "genre": ""}}

        return {"utt":"こちらはぐるなび案内システムです。ご用件をどうぞ。", "end":False}

    def reply(self, input):
        text = input["utt"]
        sessionId = input["sessionId"]

        # 現在のセッションのフレームを取得
        frame = self.sessiondic[sessionId]["frame"]
        print("frame=", frame)

        # 発話から対話行為タイプとコンセプトを取得
        da, conceptdic = self.da_concept.process(text)
        print(da, conceptdic)

        # 対話行為タイプとコンセプトを用いてフレームを更新
        frame = self.update_frame(frame, da, conceptdic)
        print("updated frame=", frame)

        # 更新後のフレームを保存
        self.sessiondic[sessionId] = {"frame": frame}

        # フレームからシステム対話行為を得る
        sys_da = self.next_system_da(frame)

        # 遷移先がtell-infoの場合は情報を伝えて終了
        if sys_da == "tell-info":
            utts = []
            utts.append("お伝えします")
            place = frame["place"]
            genre = frame["genre"]

            pref_code = self.get_pref_code(place)
            # print(pref_code)
            cw = self.get_restrant(genre, pref_code)
            utts.append(cw['rest_info']['rest0']['name'])
            utts.append("ご利用ありがとうございました")
            del self.sessiondic[sessionId]
            return {"utt":"。".join(utts), "end": True}

        else:
            # その他の遷移先の場合は状態に紐づいたシステム発話を生成
            sysutt = self.uttdic[sys_da]            
            return {"utt":sysutt, "end": False}

if __name__ == '__main__':
    system = FrameWeatherSystem()
    bot = TelegramBot(system)
    bot.run()    

# end of file
