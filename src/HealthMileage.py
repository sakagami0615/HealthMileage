from src.ParseInputMessage import ParseInputMessage
from src.WebDriver import WebDriver
from src.HealthLogin import HealthLogin
from src.HealthAutofill import HealthAutofill
from src import LinePushMessage
from src import ErrorLog



class HealthMileage:
	"""
	わくわくマイレージ自動入力のメインクラス

	Attributes
	----------
	parse_message : class
		Lineのチャットで送信されたメッセージをParseするクラスオブジェクト
	"""

	def __init__(self):

		self.__parse_message = ParseInputMessage()
		ErrorLog.error_log_object = ErrorLog.ErrorLog()
	

	def Run(self, event_msg, is_hidden=True):
		"""
		わくわくマイレージ自動入力を実施する

		Parameters
		----------
		event_msg : string
			Lineのチャットで送信されたメッセージ
		is_hidden : boolean
			ブラウザの表示/非表示フラグ(True：非表示、False：表示)

		Returns
		----------
		result_flg : boolean
			自動入力成功フラグ(True：成功、False：失敗)
		result_msg : string
			自動入力実施の結果ログ
			※エラーが生じた際は、エラーログが返却される
		"""
		# 入力のParse処理
		user_param, flg_param, value_param = self.__parse_message.Parse(event_msg)
		if ErrorLog.error_log_object.error_flg:
			return False, ErrorLog.error_log_object.CreateErrorMessage()
		
		# ドライバと自動入力処理クラスのを用意
		web_driver = WebDriver(is_hidden=is_hidden)
		autofill = HealthAutofill(web_driver)
		health_login = HealthLogin(web_driver)

		# ログイン処理
		LinePushMessage.line_msg_obj.PushMessage('PepupLogin Process Now')
		health_login.Login(user_param)
		if ErrorLog.error_log_object.error_flg:
			return False, ErrorLog.error_log_object.CreateErrorMessage()
		
		# 自動入力処理
		result_msg = autofill.Record(flg_param, value_param)
		if ErrorLog.error_log_object.error_flg:
			return False, ErrorLog.error_log_object.CreateErrorMessage()

		return True, result_msg
