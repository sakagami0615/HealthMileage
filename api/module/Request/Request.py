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
import traceback
import datetime
import dateutil.parser

from module.Health.HealthRunRecord import HealthRunRecord
from module.Health.HealthRunConfirm import HealthRunConfirm
from module.Health.HealthRunParam import HealthRunParam
from module.Mailler import MailUtility

from module.Request.RequestParam import Param as REQPARAM
from module.Mailler.MaillParam import Param as MAILPARAM
from module.Main.MainParam import Param as MAINPARAM


# ----------------------------------------------------------------------------------------------------
# Requestクラス
# ----------------------------------------------------------------------------------------------------
class Request:

	def __init__(self, maill_order):
		
		self.__maill_order = maill_order
		self.__record = HealthRunRecord()
		self.__confirm = HealthRunConfirm()
		self.__param = HealthRunParam()

	# ----------------------------------------------------------------------------------------------------
	# 未出の命令開始地点日時を保存しているファイルの取得
	# ----------------------------------------------------------------------------------------------------
	def LoadUnpublishMailHeadDate(self):
		
		if os.path.isfile(REQPARAM.NEXT_HEAD_DATE_PATH):
			with open(REQPARAM.NEXT_HEAD_DATE_PATH, 'r', encoding='utf-8') as f:
				unpublish_head_date_dict = json.load(f)
				unpublish_head_date = dateutil.parser.parse(unpublish_head_date_dict['Date'])
		else:
			unpublish_head_date = None
		
		return unpublish_head_date


	# ----------------------------------------------------------------------------------------------------
	# 未出の命令開始地点日時をファイルに保存
	# ----------------------------------------------------------------------------------------------------
	def SaveUnpublishMailHeadDate(self, req_info_list):
		
		if len(req_info_list) > 0:
			tale_date = req_info_list[len(req_info_list) - 1]['Date']
			with open(REQPARAM.NEXT_HEAD_DATE_PATH, 'w', encoding='utf-8') as f:
				json.dump({'Date': str(tale_date)}, f)


	# ----------------------------------------------------------------------------------------------------
	# リクエストに応じて処理を実行
	# ----------------------------------------------------------------------------------------------------
	def RunRequest(self, req_info_list):
		
		for req_info in req_info_list:
			# 予期せぬエラーをキャッチするためにtryを記載
			try:
				# 記録処理
				if req_info['Subject'] == REQPARAM.ODER_TYPE_RECORD:
					print(' - Process [{}]'.format(REQPARAM.ODER_TYPE_RECORD))
					(is_success, ack_msg) = self.__record.RunRecord()
					ack = MailUtility.OrganizeAckinfo(req_info['Subject'], is_success, ack_msg)
					img_paths = None
				
				# 通知処理
				elif req_info['Subject'] == REQPARAM.ODER_TYPE_CONFIRM:
					print(' - Process [{}]'.format(REQPARAM.ODER_TYPE_CONFIRM))
					(is_success, ack_msg) = self.__confirm.RunConfirm()
					ack = MailUtility.OrganizeAckinfo(req_info['Subject'], is_success, ack_msg)
					img_paths = None
				
				# パラメータ確認処理
				elif req_info['Subject'] == REQPARAM.ODER_TYPE_PARAM:
					print(' - Process [{}]'.format(REQPARAM.ODER_TYPE_PARAM))
					(is_success, ack_msg) = self.__param.RunParam()
					ack = MailUtility.OrganizeAckinfo(req_info['Subject'], is_success, ack_msg)
					img_paths = MAINPARAM.PARAM_IMG_PATHS
				
				# 命令以外の場合、無視
				else:
					continue

				self.__maill_order.SendMail(req_info['From'], ack['Subject'], ack['Msg'], img_paths)

			# 予期せぬエラー等を通知する処理
			except Exception:
				mail_to = self.__maill_order.GetLoginAdress(),

				mail_subject = MailUtility.ConvertFormattedSubject('SYSTEM ERROR')
				mail_body = '■Date:{}\n\n■Contents\n{}'.format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'), traceback.format_exc())
				self.__maill_order.SendMail(mail_to, mail_subject, mail_body)