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
import datetime

from module.Mailler.MaillParam import Param as MAILPARAM


# ----------------------------------------------------------------------------------------------------
# 通常のタイトルから形式化したタイトルに変換する
# ----------------------------------------------------------------------------------------------------
def ConvertFormattedSubject(subject):
	
	formatted_subject = MAILPARAM.MAIL_SUBJECT_FORMAT.format(subject)
	return formatted_subject


# ----------------------------------------------------------------------------------------------------
# メール通知用情報の整理
# ----------------------------------------------------------------------------------------------------
def OrganizeAckinfo(order_type, is_success, ack_msg):
	
	if not is_success:
		subject = ConvertFormattedSubject('{} : failuer'.format(order_type))
		error_msg = '■完了日時:{}\n\n■内容\n{}'.format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'), ack_msg)
		return {'Result': is_success, 'Subject': subject, 'Msg': error_msg}

	subject = ConvertFormattedSubject('{} : success'.format(order_type))
	msg = '■完了日時:{}\n\n■内容\n{}'.format(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'), ack_msg)
	return {'Result': is_success, 'Subject': subject, 'Msg': msg}