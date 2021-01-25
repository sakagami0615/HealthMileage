from flask import Flask, request, abort

from linebot import (
	LineBotApi, WebhookHandler
)
from linebot.exceptions import (
	InvalidSignatureError
)
from linebot.models import (
	MessageEvent, TextMessage,
)

try:
	from private import channel
except:
	pass

try:
	from private import userparam
except:
	pass

try:
	from master import masterprocess
except:
	pass


import datetime
from version import version
from src.HealthMileage import HealthMileage
from src import LinePushMessage
from src import ErrorLog

app = Flask(__name__)

line_bot_api = LineBotApi(channel.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(channel.CHANNEL_SECRET)


@app.route("/")
def check():
	return "Hello World"


@app.route("/callback", methods=['POST'])
def callback():
	# get X-Line-Signature header value
	signature = request.headers['X-Line-Signature']

	# get request body as text
	body = request.get_data(as_text=True)
	app.logger.info("Request body: " + body)

	# handle webhook body
	try:
		handler.handle(body, signature)
	except InvalidSignatureError:
		print("Invalid signature. Please check your channel access token/channel secret.")
		abort(400)

	return 'OK'


enable_app = True
user_status = {}

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

	global enable_app
	global user_status

	# ユーザID取得
	user_id = event.source.user_id

	# 初回使用時のユーザ情報を保存
	if user_id not in user_status:
		profile = line_bot_api.get_profile(user_id)
		user_status[user_id] = {}
		user_status[user_id]['display_name'] = profile.display_name
		user_status[user_id]['user_id'] = profile.user_id
		user_status[user_id]['is_access'] = False
		# セキュリティの関係上、無効化
		#user_status[user_id]['last_message'] = '前回メッセージがありません'
		

	# PushMessage通知用クラス生成
	LinePushMessage.line_msg_obj = LinePushMessage.LinePushMessage(line_bot_api, user_id)
	# エラーメッセージ格納用クラス生成
	ErrorLog.error_log_object = ErrorLog.ErrorLog()
	
	# 管理者用処理
	try:
		if user_id == userparam.USERID:
			if not user_status[user_id]['is_access']:
				app_mode = masterprocess.ForcedSwitchApp(line_bot_api, event, enable_app)
				if app_mode == 'stop':
					enable_app = False
					return
				elif app_mode == 'start':
					enable_app = True
					return

				is_check = masterprocess.MasterCheck(line_bot_api, event, user_status)
				if is_check:
					return
			else:
				LinePushMessage.line_msg_obj.PushMessage('現在、自動入力処理中です')
				return
	except:
		pass
	
	# アプリ停止判定
	if not enable_app:
		LinePushMessage.line_msg_obj.PushMessage('現在、管理者によってアプリが停止しています')
		return
	
	# 処理開始
	if not user_status[user_id]['is_access']:
		try:
			# アプリのバージョン返却処理
			if event.message.text == 'version':
				LinePushMessage.line_msg_obj.PushMessage(version.VERSION)
				return
			# アプリ登録時メッセージ返却処理
			elif event.message.text == 'initmsg':
				LinePushMessage.line_msg_obj.PushMessage(version.HOW_TO_USE_MESSAGE)
				LinePushMessage.line_msg_obj.PushMessage(version.CHEAT_COMMAND_MESSAGE)
				LinePushMessage.line_msg_obj.PushMessage(version.FORMAT_MESSAGE)
				return
			# アプリ変更履歴返却処理
			elif event.message.text == 'history':
				LinePushMessage.line_msg_obj.PushMessage(version.HISTORY_LOG_MESSAGE)
				return
			
			# セキュリティの関係上、無効化
			# 前回コメント返却処理
			elif event.message.text == 'lastmsg':
				#LinePushMessage.line_msg_obj.PushMessage(user_status[user_id]['last_message'])
				#return
				pass
			# 自動入力処理
			else:
				LinePushMessage.line_msg_obj.PushMessage('自動入力が完了するまで少々お待ちください')
				user_status[user_id]['is_access'] = True
				health_mileage = HealthMileage()
				result_flg, result_msg = health_mileage.Run(event_msg=event.message.text, is_hidden=True)
				user_status[user_id]['is_access'] = False
				# セキュリティの関係上、無効化
				#if result_flg: user_status[user_id]['last_message'] = event.message.text

		except:
			# エラー内容を取得
			user_status[user_id]['is_access'] = False
			ErrorLog.error_log_object.Traceback()
			result_msg = ErrorLog.error_log_object.CreateErrorMessage()
	# 現在入力中のため、自動入力処理未実施
	else:
		result_msg = '現在、自動入力処理中です'

	# 結果ログを表示
	LinePushMessage.line_msg_obj.PushMessage(result_msg)


if __name__ == "__main__":
	app.run()