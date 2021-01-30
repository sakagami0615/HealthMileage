from app.src import ErrorLog


class ParseInputMessage:
	"""
	入力メッセージのParseを担当するクラス

	Attributes
	----------
	user_param : dict
		ユーザの情報
		※アドレス、パスワード等
	flg_param : dict
		各種入力項目を実施するかどうかのフラグ
	value_param : dict
		歩数、睡眠時間の数値
	item_list : list of dict
		各種入力項目チェックのメンバ関数を格納した辞書リスト
	"""

	def __init__(self):

		# 初期化
		self.__user_param = dict()
		self.__user_param['Address'] = None
		self.__user_param['Password'] = None
		
		self.__flg_param = dict()
		self.__flg_param['StepInputFlg'] = False
		self.__flg_param['SleepInputFlg'] = False
		self.__flg_param['CheckFlg'] = False

		self.__value_param = dict()
		self.__value_param['StepValueMin'] = None
		self.__value_param['StepValueMax'] = None
		self.__value_param['SleepValueMin'] = None
		self.__value_param['SleepValueMax'] = None


		# 各種入力項目確認用データ格納配列
		self.__item_list = [
			{'Label' : 'メールアドレス', 'Event': self.__ResistAddress},
			{'Label' : 'パスワード', 'Event': self.__ResistPassword},
			{'Label' : '歩数', 'Event': self.__ResistStepValue},
			{'Label' : '睡眠時間', 'Event': self.__ResistSleepValue},
			{'Label' : 'チェック', 'Event': self.__ResistCheck}
		]
	

	def __CheckAndConvNumeric(self, str, type):
		"""
		数値文字列の確認および変換後の数値を取得する

		Parameters
		----------
		str : string
			対象の対象の文字列
		type : class
			変換する数値の方(int、floatなど)

		Returns
		----------
		num_flg : boolean
			変換成功フラグ(True：成功、False：失敗)
		num_value : type
			変換後の数値(変換失敗時は、Noneとなる)
		"""
		try:
			num_value = type(float(str))
			num_flg = True
		except ValueError:
			num_value = None
			num_flg = False
		
		return num_flg, num_value
	

	def __ResistAddress(self, address, message):
		"""
		アドレスをパラメータに格納する

		Parameters
		----------
		address : string
			アドレス
		message : string
			アドレスを抽出した入力メッセージ
		"""
		# エラーチェック無し
		# (ログイン時のエラーは別クラスでチェックする)
		self.__user_param['Address'] = address


	def __ResistPassword(self, password, message):
		"""
		パスワードをパラメータに格納する

		Parameters
		----------
		password : string
			パスワード
		message : string
			パスワードを抽出した入力メッセージ
		"""
		# エラーチェック無し
		# (ログイン時のエラーは別クラスでチェックする)
		self.__user_param['Password'] = password
	

	def __ResistStepValue(self, value, message):
		"""
		歩数値をパラメータに格納する

		Parameters
		----------
		value : string
			歩数
		message : string
			歩数を抽出した入力メッセージ
		"""
		value_item = value.split('-')

		# スカラ指定のエラーチェック
		if len(value_item) == 1:
			num_flg, num_value = self.__CheckAndConvNumeric(value_item[0], int)
			if num_flg:
				self.__flg_param['StepInputFlg'] = True
				self.__value_param['StepValueMin'] = num_value
				self.__value_param['StepValueMax'] = num_value
			else:
				ErrorLog.error_log_object.Resist('')
				ErrorLog.error_log_object.Resist('■数値エラー｜{}'.format(message))
				ErrorLog.error_log_object.Resist('　[{}]が数値になっていません'.format(value))
		
		# 範囲指定のエラーチェック
		elif len(value_item) == 2:
			num_1_flg, num_1_value = self.__CheckAndConvNumeric(value_item[0], int)
			num_2_flg, num_2_value = self.__CheckAndConvNumeric(value_item[1], int)

			if num_1_flg and num_2_flg:
				min_num_value = num_1_value if num_1_value <= num_2_value else num_2_value
				max_num_value = num_1_value if num_1_value >  num_2_value else num_2_value
				
				self.__flg_param['StepInputFlg'] = True
				self.__value_param['StepValueMin'] = min_num_value
				self.__value_param['StepValueMax'] = max_num_value

			else:
				if not num_1_flg:
					ErrorLog.error_log_object.Resist('')
					ErrorLog.error_log_object.Resist('■数値エラー｜{}'.format(message))
					ErrorLog.error_log_object.Resist('　[{}]が数値になっていません'.format(value_item[0]))
				
				if not num_2_flg:
					ErrorLog.error_log_object.Resist('')
					ErrorLog.error_log_object.Resist('■数値エラー｜{}'.format(message))
					ErrorLog.error_log_object.Resist('　[{}]が数値になっていません'.format(value_item[1]))
		
		else:
			ErrorLog.error_log_object.Resist('')
			ErrorLog.error_log_object.Resist('■構文エラー｜{}'.format(message))
			ErrorLog.error_log_object.Resist('　[-]による範囲指定の記載法に不備があります')
	

	def __ResistSleepValue(self, value, message):
		"""
		睡眠時間値をパラメータに格納する

		Parameters
		----------
		value : string
			睡眠時間
		message : string
			睡眠時間を抽出した入力メッセージ
		"""
		value_item = value.split('-')

		# スカラ指定のエラーチェック
		if len(value_item) == 1:
			num_flg, num_value = self.__CheckAndConvNumeric(value_item[0], float)
			if num_flg:
				self.__flg_param['SleepInputFlg'] = True
				self.__value_param['SleepValueMin'] = num_value
				self.__value_param['SleepValueMax'] = num_value
			else:
				ErrorLog.error_log_object.Resist('')
				ErrorLog.error_log_object.Resist('■数値エラー｜{}'.format(message))
				ErrorLog.error_log_object.Resist('　[{}]が数値になっていません'.format(value))
		
		# 範囲指定のエラーチェック
		elif len(value_item) == 2:
			num_1_flg, num_1_value = self.__CheckAndConvNumeric(value_item[0], float)
			num_2_flg, num_2_value = self.__CheckAndConvNumeric(value_item[1], float)

			if num_1_flg and num_2_flg:
				min_num_value = num_1_value if num_1_value <= num_2_value else num_2_value
				max_num_value = num_1_value if num_1_value >  num_2_value else num_2_value
				
				self.__flg_param['SleepInputFlg'] = True
				self.__value_param['SleepValueMin'] = min_num_value
				self.__value_param['SleepValueMax'] = max_num_value

			else:
				if not num_1_flg:
					ErrorLog.error_log_object.Resist('')
					ErrorLog.error_log_object.Resist('■数値エラー｜{}'.format(message))
					ErrorLog.error_log_object.Resist('　[{}]が数値になっていません'.format(value_item[0]))
				
				if not num_2_flg:
					ErrorLog.error_log_object.Resist('')
					ErrorLog.error_log_object.Resist('■数値エラー｜{}'.format(message))
					ErrorLog.error_log_object.Resist('　[{}]が数値になっていません'.format(value_item[1]))
		
		else:
			ErrorLog.error_log_object.Resist('')
			ErrorLog.error_log_object.Resist('■構文エラー｜{}'.format(message))
			ErrorLog.error_log_object.Resist('　[-]による範囲指定の記載法に不備があります')
	

	def __ResistCheck(self, res, message):
		"""
		チェック入力の有無をパラメータに格納する

		Parameters
		----------
		res : string
			チェック入力の有無(あり or なし)
		message : string
			チェック入力の有無を抽出した入力メッセージ
		"""
		if res == 'あり':
			self.__flg_param['CheckFlg'] = True
		elif res == 'なし':
			self.__flg_param['CheckFlg'] = False
		else:
			ErrorLog.error_log_object.Resist('')
			ErrorLog.error_log_object.Resist('■記載ミス｜{}'.format(message))
			ErrorLog.error_log_object.Resist('　[あり/なし]のどちらにして下さい')
	

	def Parse(self, message):
		"""
		入力メッセージをParseしてパラメータ辞書に変換する

		Parameters
		----------
		message : string
			Lineのチャットで入力されたメッセージ

		Returns
		----------
		num_flg : boolean
			変換成功フラグ(True：成功、False：失敗)
		num_value : type

		user_param : dict
			ユーザの情報
		flg_param : dict
			各種入力項目を実施するかどうかのフラグ
		value_param : dict
			歩数、睡眠時間の数値
		"""

		labels = [item['Label'] for item in self.__item_list]

		lines = message.split('\n')
		for line in lines:
			# 入力項目の判定用フラグとカウント計算
			item_flgs = [label in line for label in labels]
			item_count = item_flgs.count(True)

			# 入力項目の判定
			if item_count == 1:
				tokens = line.split(':', 1)
				if len(tokens) <= 1:
					# 構文エラー
					ErrorLog.error_log_object.Resist('')
					ErrorLog.error_log_object.Resist('■構文エラー｜{}'.format(line))
					ErrorLog.error_log_object.Resist('　[:]の記載法に不備があります')
				else:
					# パラメータ抽出
					item = self.__item_list[item_flgs.index(True)]
					item['Event'](tokens[1], line)
		
		# 入力フラグ確認
		if [self.__flg_param[key] for key in self.__flg_param.keys()].count(True) == 0:
			ErrorLog.error_log_object.Resist('')
			ErrorLog.error_log_object.Resist('■構文エラー｜入力チャット全体')
			ErrorLog.error_log_object.Resist('　自動入力する項目が指定されていません')
		
		return self.__user_param, self.__flg_param, self.__value_param
