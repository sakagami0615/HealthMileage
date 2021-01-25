import traceback


class ErrorLog:
	"""
	エラーログ管理用のクラス
	※error_log_objectのグローバル変数を使用して
	　エラーを格納していく

	Attributes
	----------
	error_flg : boolean
		エラーログの有無フラグ(True：有り、False：無し)
	error_logs : list of string
		エラーログ格納配列
	"""
	def __init__(self):
		self.error_flg = False
		self.__error_log_list = []
	

	def Resist(self, log_msg):
		"""
		エラーログを格納する

		Returns
		----------
		log_msg : string
			格納するエラーログ
		"""
		if not self.error_flg:
			# 初回時のみ、エラーログのタイトルを格納する
			self.__error_log_list.append('下記入力で不備があります')
		
		self.__error_log_list.append(log_msg)
		self.error_flg = True


	def Traceback(self):
		"""
		Tracebackのエラー内容を格納する

		Returns
		----------
		log_msg : string
			格納するエラーログ
		"""
		self.__error_log_list.append(traceback.format_exc())
		self.error_flg = True

	
	def CreateErrorMessage(self):
		"""
		エラーログを格納リストからエラーメッセージを作成する

		Returns
		----------
		error_msg : string
			エラーメッセージ
		"""
		error_msg = '\n'.join(self.__error_log_list)
		return error_msg



global error_log_object
