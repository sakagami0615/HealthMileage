import os, sys
if os.path.basename(os.getcwd()) == 'test':
	os.chdir('../../../')
	sys.path.append('HealthMileageBot')
elif os.path.basename(os.getcwd()) == 'HealthMileageBot':
	os.chdir('../')
	sys.path.append('HealthMileageBot')
else:
	exit()


from app.private import userparam
from app.src.HealthMileage import HealthMileage
from app.src import LinePushMessage
from app.src import ErrorLog


def TEST_HealthMileage(event_msg):

	# PushMessage通知用クラス生成
	LinePushMessage.line_msg_obj = LinePushMessage.LinePushMessage()
	# エラーメッセージ格納用クラス生成
	ErrorLog.error_log_object = ErrorLog.ErrorLog()
	
	health_mileage = HealthMileage()
	result_flg, result_msg = health_mileage.Run(event_msg, is_hidden=True)

	return result_msg


if __name__ == '__main__':

	print()
	print('-'*50)
	print('TEST_HealthMileage BEGIN')
	print('-'*50)

	event_msg = "【Format】\nメールアドレス:" + userparam.ADDRESS + "\nパスワード:" + userparam.PASSWORD + "\n歩数:8000-10000\n睡眠時間:6-7.5\nチェック:あり"

	result_msg = TEST_HealthMileage(event_msg)

	print(result_msg)

	print('-'*50)
	print('TEST_HealthMileage END')
	print('-'*50)
	print()
