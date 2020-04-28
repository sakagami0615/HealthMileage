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
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

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
	# ※img_path：list
	# ----------------------------------------------------------------------------------------------------
	def SendMail(self, to, subject, body, img_paths=None):

		# Create the root message and fill in the from, to, and subject headers
		msg_root = MIMEMultipart('related')
		msg_root['Subject'] = subject
		msg_root['From'] = self.__profile['Adress']
		msg_root['To'] = to
		msg_root.preamble = 'This is a multi-part message in MIME format.'

		# Encapsulate the plain and HTML versions of the message body in an
		# 'alternative' part, so message agents can decide which they want to display.
		msg_alternative = MIMEMultipart('alternative')
		msg_root.attach(msg_alternative)

		#msg_text = MIMEText(body)
		#msg_alternative.attach(msg_text)
		
		if img_paths == None:
			body_html = body.replace('\n', '<br>')
			img_src = '<p>{}</p>'.format(body_html)
			msg_text = MIMEText(img_src, 'html')
			msg_alternative.attach(msg_text)

		else:
			# We reference the image in the IMG SRC attribute by the ID we give it below		
			body_html = body.replace('\n', '<br>')
			img_src = '<p>{}</p>'.format(body_html)
			for idx in range(len(img_paths)):
				img_src += '<img src="cid:image{}"><br>'.format(idx)
			msg_text = MIMEText(img_src, 'html')
			msg_alternative.attach(msg_text)

			for (idx, img_path) in enumerate(img_paths):
				# This example assumes the image is in the current directory
				fp = open(img_path, 'rb')
				msg_image = MIMEImage(fp.read())
				fp.close()
				# Define the image's ID as referenced above
				msg_image.add_header('Content-ID', '<image{}>'.format(idx))
				msg_root.attach(msg_image)
	
		# ----------------------------------------
		# メッセージ送信
		# ----------------------------------------
		smtpobj = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
		smtpobj.login(self.__profile['Adress'], self.__profile['Password'])
		smtpobj.sendmail(self.__profile['Adress'], msg_root['To'], msg_root.as_string())
		smtpobj.close()