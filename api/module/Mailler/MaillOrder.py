# ----------------------------------------------------------------------------------------------------
# モジュールフォルダのパスを追加
# ----------------------------------------------------------------------------------------------------
import os, sys
if sys.path.count('api/module') == 0:
	if os.path.basename(os.getcwd()) == 'HealthMileage':
		sys.path.append('api/module')
	elif os.path.basename(os.getcwd()) == 'api':
		os.chdir('../')
		sys.path.append('api/module')
	else:
		exit()


# ----------------------------------------------------------------------------------------------------
# モジュールimport
# ----------------------------------------------------------------------------------------------------
import os
import json
import email
import smtplib
import imaplib
import ssl
from email.utils import formatdate
from email.mime.text import MIMEText

from module.Mailler.MaillParam import Param as MAILPARAM


# ----------------------------------------------------------------------------------------------------
# MaillOrderクラス
# ----------------------------------------------------------------------------------------------------
class MaillOrder:

	def __init__(self):
		
		# ログイン情報ファイルの読み込み
		with open(MAILPARAM.PROFILE_PATH, 'r', encoding='utf-8') as f:
			self.__profile = json.load(f)

	
	# ----------------------------------------------------------------------------------------------------
	# 管理者メールアドレスを取得
	# ----------------------------------------------------------------------------------------------------
	def GetLoginAdress(self):

		return self.__profile['Adress']		


	# ----------------------------------------------------------------------------------------------------
	# メール受信
	# ----------------------------------------------------------------------------------------------------
	def RecvMail(self):

		# ----------------------------------------
		# ログイン処理
		# ----------------------------------------
		# https://qiita.com/takey/items/1498af9e1113eeb7bb21
		imapobj = imaplib.IMAP4_SSL('imap.gmail.com', 993)
		imapobj.login(self.__profile['Adress'], self.__profile['Password'])

		imapobj.select() # メールボックスの選択
		data = imapobj.search(None, 'ALL')[1]
		datas = data[0].split()

		# 取得メッセージ数
		fetch_num = MAILPARAM.MAX_RECV_NUM if len(datas) >= MAILPARAM.MAX_RECV_NUM else len(datas)

		# ----------------------------------------
		# 受信メール取得
		# ----------------------------------------
		mime_msg_list = []  # 取得したMIMEメッセージを格納するリスト
		for data_iter in datas[len(datas) - fetch_num:]:
			data = imapobj.fetch(data_iter, '(RFC822)')[1]
			mime_msg = email.message_from_bytes(data[0][1])
			mime_msg_list.append(mime_msg)

		imapobj.close()
		imapobj.logout()

		return mime_msg_list
	
	# ----------------------------------------------------------------------------------------------------
	# メール送信
	# ----------------------------------------------------------------------------------------------------
	def SendMail(self, to, subject, body):

		# ----------------------------------------
		# メッセージ作成
		# ----------------------------------------
		msg = MIMEText(body)
		msg['Subject'] = subject
		msg['From'] = self.__profile['Adress']
		msg['To'] = to
		msg['Date'] = formatdate()

		# ----------------------------------------
		# メッセージ送信
		# ----------------------------------------
		smtpobj = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
		smtpobj.login(self.__profile['Adress'], self.__profile['Password'])
		smtpobj.sendmail(self.__profile['Adress'], msg['To'], msg.as_string())
		smtpobj.close()