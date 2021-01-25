import datetime
from private import userparam
from src import LinePushMessage
from src import ErrorLog


def __DisplayUserName(line_bot_api, user_status):

	user_ids = list(user_status.keys())

	if len(user_ids) > 0:
		result_list = []
		for (index, user_id) in enumerate(user_ids):
			profile = line_bot_api.get_profile(user_id)
			result_list.append('{} : {}'.format(index + 1, profile.display_name))
		result_msg = '\n'.join(result_list)
	else:
		result_msg = 'アプリ使用者はいません'
	
	return result_msg


def ForcedSwitchApp(line_bot_api, event, curr_enable_app):

	if curr_enable_app:
		if event.message.text == 'appstop':
			LinePushMessage.line_msg_obj.PushMessage('app Disable')
			app_mode = 'stop'
		else:
			app_mode = 'hold'
	else:
		if event.message.text == 'appstart':
			LinePushMessage.line_msg_obj.PushMessage('app Enable')
			app_mode = 'start'
		else:
			app_mode = 'hold'
	
	return app_mode


def MasterCheck(line_bot_api, event, user_status):

	# チェック機能:使用ユーザの確認
	if event.message.text == 'usrchk':
		LinePushMessage.line_msg_obj.PushMessage('usrchk PROCESS BEGIN')
		result_msg = __DisplayUserName(line_bot_api, user_status)
		LinePushMessage.line_msg_obj.PushMessage(result_msg)
		LinePushMessage.line_msg_obj.PushMessage('usrchk PROCESS END')
		return True
	
	# 時間取得
	if event.message.text == 'time':
		LinePushMessage.line_msg_obj.PushMessage(str(datetime.datetime.now()))
		return True
	
	return False
