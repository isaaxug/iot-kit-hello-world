#! /usr/bin/env python3
# coding: utf-8

"""
    Enviro pHAT部分の制御を行う。
"""

import os
import time
import envirophat
from threading import Thread, Event

# 別途ファイルで定義したMQTTクライアントをインポートする
from lib.mqtt import client, start

# 変更要求をパブリッシュするトピックを作成する
TARGET_NAME = os.environ.get('MQTT_TARGET_NAME')
TOPIC = 'cmnd/' + TARGET_NAME + '/display/change'

# eventオブジェクトを作成する
# https://docs.python.jp/3/library/threading.html#event-objects
event = Event()
driver = None

def main():
    """
        メイン関数
        ここで動かしているstartは上でインポートしたMQTTの接続開始関数
    """

    # イベントオブジェクトをセットして現在動作している表示処理を終了させる。
    # これがセットされると表示関数中ループを抜け出すことにより関数が終了し、デーモンも消滅する。
    # 各表示関数はwhileループ毎でこれを確認しているので終了には時間がかかる。
    # なのである程度待つ必要がある。
    # 動作モードによって終了に必要な時間にばらつきがある場合は、Lockオブジェクトを使用するのもアリ
    event.set()
    time.sleep(1)
    # イベントオブジェクトをリセットして再利用可能にする
    event.clear()

    #　Threadオブジェクトに動作関数を渡し、並列動作を開始させる（デーモンの作成）
    # ここでeventオブジェクトを渡して終了イベントを渡せるようにする
    # https://docs.python.jp/3/library/threading.html#thread-objects
    driver = Thread(target=start_envirophat, args=(event))
    driver.daemon = True
    driver.start()

    # MQTTサブスクライブ
    start()

def start_envirophat(s=60):
    """
        Enviro pHATから環境データを取得し定期的にクラウドに送信
        インターバルはデフォルト60秒
    """
    while True:
        # 後で加工しやすいようにデータはJSON形式にする
        data = {
            'name': 'Enviro pHAT',
            'temperature': 26.5, # ToDo: 実際の気温データに変更
            'pressure': 1026.11, # ToDo: 実際の気圧データに変更
            'light': 2630, # ToDo: 実際の照度データに変更
        }
        pub_data(data)
        time.sleep(s)

def pub_data(data):
    """
        定期的にデータをパブリッシュする
    """
    client.publish(
            topic=TOPIC,
            payload=data
        )
