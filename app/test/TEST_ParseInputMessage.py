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
from app.src.ParseInputMessage import ParseInputMessage
from app.src import ErrorLog


def TEST_ParseInputMessage(event_msg):

	ErrorLog.error_log_object = ErrorLog.ErrorLog()

	parse_message = ParseInputMessage()
	user_param, flg_param, value_param = parse_message.Parse(event_msg)

	error_flg = ErrorLog.error_log_object.error_flg
	result_msg = ErrorLog.error_log_object.CreateErrorMessage()

	return error_flg, result_msg, user_param, flg_param, value_param
	

if __name__ == '__main__':

	TEST_DATA_LIST = [
		{
			'TestID': 1,
			'Message': "メールアドレス:" + userparam.ADDRESS + "\nパスワード:" + userparam.PASSWORD + "\n歩数:8000-10000\n睡眠時間:6-7.5\nチェック:あり",
			'Correct': False,
			'Description': "正常"
		},
		{
			'TestID': 2,
			'Message': "メールアドレス:" + userparam.ADDRESS + "\nパスワード:" + userparam.PASSWORD + "\n歩数:8000-10000\n睡眠時間:6-7.5\nチェック:なし",
			'Correct': False,
			'Description': "正常"
		},
		{
			'TestID': 3,
			'Message': "メールアドレス:" + userparam.ADDRESS + "\nパスワード:" + userparam.PASSWORD + "\n歩数:8000\n睡眠時間:6-7.5\nチェック:あり",
			'Correct': False,
			'Description': "正常"
		},
		{
			'TestID': 4,
			'Message': "メールアドレス:" + userparam.ADDRESS + "\nパスワード:" + userparam.PASSWORD + "\n歩数:8000-10000\n睡眠時間:7.5\nチェック:あり",
			'Correct': False,
			'Description': "正常"
		},
		{
			'TestID': 5,
			'Message': "メールアドレス" + userparam.ADDRESS + "\nパスワード" + userparam.PASSWORD + "\n歩数:8000-10000\n睡眠時間:6-7.5\nチェック:あり",
			'Correct': True,
			'Description': "パスワードの入力不正"
		},
		{
			'TestID': 6,
			'Message': "メールアドレス:" + userparam.ADDRESS + "\nパスワード:" + userparam.PASSWORD + "\n歩数8000-10000\n睡眠時間:6-7.5\nチェック:あり",
			'Correct': True,
			'Description': "歩数の入力不正"
		},
		{
			'TestID': 7,
			'Message': "メールアドレス:" + userparam.ADDRESS + "\nパスワード:" + userparam.PASSWORD + "\n歩数:STR-10000\n睡眠時間:6-7.5\nチェック:あり",
			'Correct': True,
			'Description': "歩数入力不正"
		},
		{
			'TestID': 8,
			'Message': "メールアドレス:" + userparam.ADDRESS + "\nパスワード:" + userparam.PASSWORD + "\n歩数:8000-STR\n睡眠時間:6-7.5\nチェック:あり",
			'Correct': True,
			'Description': "歩数の入力不正"
		},
		{
			'TestID': 9,
			'Message': "メールアドレス:" + userparam.ADDRESS + "\nパスワード:" + userparam.PASSWORD + "\n歩数:8000-10000\n睡眠時間6-7.5\nチェック:あり",
			'Correct': True,
			'Description': "睡眠時間の入力不正"
		},
		{
			'TestID': 10,
			'Message': "メールアドレス:" + userparam.ADDRESS + "\nパスワード:" + userparam.PASSWORD + "\n歩数:8000-10000\n睡眠時間:STR-7.5\nチェック:あり",
			'Correct': True,
			'Description': "睡眠時間の入力不正"
		},
		{
			'TestID': 11,
			'Message': "メールアドレス:" + userparam.ADDRESS + "\nパスワード:" + userparam.PASSWORD + "\n歩数:8000-10000\n睡眠時間:6-STR\nチェック:あり",
			'Correct': True,
			'Description': "睡眠時間の入力不正"
		},
		{
			'TestID': 12,
			'Message': "メールアドレス:" + userparam.ADDRESS + "\nパスワード:" + userparam.PASSWORD + "\n歩数:8000-10000\n睡眠時間:6-7.5\nチェック:STR",
			'Correct': True,
			'Description': "チェックの入力不正"
		}
	]
	

	print()
	print('-'*50)
	print('TEST_ParseInputMessage BEGIN')
	print('-'*50)

	normally_count = 0
	for TEST_DATA in TEST_DATA_LIST:
		testID = TEST_DATA['TestID']
		message = TEST_DATA['Message']
		correct = TEST_DATA['Correct']
		description = TEST_DATA['Description']
		error_flg, error_msg, user_param, flg_param, value_param = TEST_ParseInputMessage(message)

		if correct == error_flg: normally_count = normally_count + 1

		print('[TEST ID - {}]'.format(testID))
		print('-> Flg Check(Result:Correct) - {}:{}'.format(error_flg, correct))

		print('-> description - {}'.format(description))
		print('-> error_msg\n{}'.format(error_msg))
		print('-'*10)

	
	print('normally_count : {}/{}'.format(normally_count, len(TEST_DATA_LIST)))


	
	print('-'*50)
	print('TEST_ParseInputMessage END')
	print('-'*50)
	print()
