try:
	from linebot.models import TextSendMessage
except:
	pass


class LinePushMessage:
	"""
	LineのPushメッセージを出力する処理用のクラス
	※line_msg_objのグローバル変数を使用して
	　PushMessageを実施する

	Attributes
	----------
	bot_api : LineBotApi
		エラーログの有無フラグ(True：有り、False：無し)
	send_id : string
		LineのユーザID
	"""

	def __init__(self, bot_api=None, send_id=None):
		self.__bot_api = bot_api
		self.__send_id = send_id
	

	def PushMessage(self, message):
		"""
		プッシュメッセージを通知
		bot_apiとsend_idのいずれかがNoneの場合は通知をしない

		Parameters
		----------
		message : string
			メッセージ文字列
		"""
		if (self.__bot_api != None) and (self.__send_id != None):
			self.__bot_api.push_message(
				self.__send_id,
				TextSendMessage(text=message))


global line_msg_obj