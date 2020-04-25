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
import re
import json
import traceback
import datetime
import dateutil.parser
from email.header import decode_header
from email.header import make_header

from module.Request.RequestParam import Param as REQPARAM


# ----------------------------------------------------------------------------------------------------
# MaillExtractorクラス
# ----------------------------------------------------------------------------------------------------
class MaillExtractor:

	def __init__(self, maill_order):
		
		self.__maill_order = maill_order
	

	# ----------------------------------------------------------------------------------------------------
	# Fromの内容からメールアドレスのみ抽出する
	# ※ XXXX <xxxx@gmail.com>　の文字から「xxxx@gmail.com」のみを抽出する
	# ----------------------------------------------------------------------------------------------------
	def __ExtractFrom2Adress(self, from_str):

		tokens = from_str.split(' <')
		
		if len(tokens) > 1:
			pre_adress_str = tokens[len(tokens) - 1]
			adress_str = pre_adress_str[:len(pre_adress_str) - 1]
		else:
			 adress_str = from_str

		return adress_str

	# ----------------------------------------------------------------------------------------------------
	# 指定された命令のメールであるかを判別
	# ----------------------------------------------------------------------------------------------------
	def __JudgeRequestMail(self, subject):
		
		if REQPARAM.ORDER_TYPES.count(subject):
			return True
		return False
	

	# ----------------------------------------------------------------------------------------------------
	# 未出の命令であるかを判別
	# ----------------------------------------------------------------------------------------------------
	def __JudgeUnpublishMail(self, head_date, date):
		
		if (head_date != None) and (head_date >= date):
			return False
		return True

	
	# ----------------------------------------------------------------------------------------------------
	# 受信メールの情報を本システムの命令形式に変更する
	# ----------------------------------------------------------------------------------------------------
	def __ConvertRequestInfoList(self, mime_msg_list, unpublish_head_date):
		
		req_list = []
		for mime_msg in mime_msg_list:
			# 日付、差出アドレス、件名を取得
			date_origin = make_header(decode_header(mime_msg['Date']))
			from_addr_origin = make_header(decode_header(mime_msg['From']))
			subject_origin = make_header(decode_header(mime_msg['Subject']))

			# 型変換
			date = dateutil.parser.parse(str(date_origin))
			from_addr = self.__ExtractFrom2Adress(str(from_addr_origin))
			subject = str(subject_origin)

			if self.__JudgeRequestMail(subject) and self.__JudgeUnpublishMail(unpublish_head_date, date):				
				req_list.append({
					'Date'   : date,
					'From'   : from_addr,
					'Subject': subject
				})
		
		# 日時が古い順で並び替え
		req_list = sorted(req_list, key=lambda s: s['Date'])
		
		return req_list

	
	# ----------------------------------------------------------------------------------------------------
	# MaillerManagerのエントリー関数
	# ----------------------------------------------------------------------------------------------------
	def ExtractRequestInfoList(self, unpublish_head_date):

		mime_msg_list = self.__maill_order.RecvMail()
		req_info_list = self.__ConvertRequestInfoList(mime_msg_list, unpublish_head_date)
		
		return req_info_list