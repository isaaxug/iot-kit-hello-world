#!/usr/bin/env python3
# coding: utf-8

"""
    mqtt_controllerを始動させるサンプル
    別途環境変数の指定が必要です。
    
    必要な環境変数は以下のとおりです。

    MQTT_NAME (任意） 表示制御を行う Touch pHAT で指定した名前
    MQTT_HOST MQTTホスト名
    MQTT_USER MQTTユーザー名
    MQTT_PASSWORD MQTTパスワード
    MQTT_PORT MQTTポート
    OPENWEATHER_API_KEY
 """

from logging import getLogger
logger = getLogger('unicorn_mqtt_display')

from logging import Formatter, StreamHandler, INFO
import sys
import os

# ロガーのレベル
logger.setLevel(INFO)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(
    Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
)
logger.addHandler(handler)

# ここから始動処理

from lib.mqtt import start, end

if __name__ == '__main__':
    try:
        start()

    except KeyboardInterrupt:
        pass

    except Exception as e:
        logger.exception(e)
        raise e

    finally:
        logger.info('stopping...')
        end()
        sys.stdout.write("bye.\n")
