import argparse
import subprocess
from logging import getLogger
logger = getLogger(__name__)

import unicornhathd
import time

'''
発話させたい内容を受け取って音声ファイルを作成する関数
- text : 喋らせたいテキスト
- path : 音声ファイルの作成先
'''
def create_wave(text, path):
    # テキストをUTF-8に変換
    if isinstance(text, bytes):
        text = text.decode('utf-8')

    text = text.strip()
    text = text.replace('\r\n', ' ')
    text = text.replace('\n', ' ')
    text = text.encode('utf-8')

    # コマンドを作成する部分。必要なコマンドとその引数やオプションを繋げているだけです。
    open_jtalk = ['open_jtalk']
    mech = ['-x', '/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice = ['-m', '/usr/share/hts-voice/mei/mei_normal.htsvoice']
    outwav = ['-ow', path]
    cmd = open_jtalk + mech + htsvoice + outwav

    # 作成したコマンドを子プロセスとして実行
    c = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    c.stdin.write(text)
    c.stdin.close()
    c.wait()

    return path

def play(path):
    # aplayコマンドを実行する
    cmd = ['aplay', path]
    subprocess.call(cmd)

def jtalk(text, path='/tmp/jtalk.wav'):
    path = create_wave(text, path)
    play(path)

def change(mode):
    """
       画面の変更要求を受け付ける関数。
       使用時はこれをインポートして、随時関数を始動してこれを操作する。
    """

    # 渡されたモードの確認。
    # 知らないモードが渡された場合はここで受付を棄却する
    if mode not in ('Washington', 'NewDelhi','London','Brasilia'):
        logger.warn('invalid mode (%s)', mode)
        return False

    logger.debug('get change call to "%s"', mode)


if __name__ == '__main__':
    # コマンドの引数を受け取る
    ap = argparse.ArgumentParser()
    ap.add_argument('-p', '--path', default='/tmp/jtalk.wav',
            help='作成する音声ファイルへのパス')
    args = vars(ap.parse_args())
    if mode == 'Washington'
        jtalk("アメリカの首都は、ニューヨークと思われがちですが、ただしくはワシントンDCです。 アメリカの人口は、約3億2500万人、大統領は、ドナルドトランプです。 日本との時差は13時間なので、ワシントンDCの現在の時刻は[]です。天気は晴れ、気温は[]です。 ", args['path'])
    if mode == 'London'
        jtalk("イギリスの首都は、ロンドンです。 イギリスの人口は約6600万人、首相はボリスジョンソンです。 日本との時差は8時間なので、ロンドンの現在の時刻は[]です。天気は[]、気温は[]です。")
    if mode == 'New Delhi'
        jtalk("インドの首都は、ニューデリーです。 インドの人口は約、13億4000万人、大統領は、ジラーム・ナート・コーヴィンド、です。 インドの言語は、ヒンディー語を筆頭に、ベンガル語など、方言も含めると、800以上の言語があります。 日本との時差は3時間30分なので、ニューデリーの現在の時刻は、[]です。天気は[]、気温は[]です。 ", args['path'])
    if mode == 'Brasilia'
        jtalk("ブラジルの首都はリオデジャネイロと思われがちですが、ただしくはブラジリアです。 ブラジルの人口は約2億1400万人、大統領はジャイール・ボルソナーロです。 日本との時差は12時間なので、ブラジリアの現在の時刻は[]です。天気は[]、気温は[]です。", args['path'])
        return False