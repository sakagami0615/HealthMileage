from datetime import datetime
from selenium.webdriver.support.ui import Select
from app.src import ErrorLog
from app.src import Parameter as PARAM
from app.src.Parameter import XPATH


class HealthAutofillCheck:
	"""
	チェック項目の自動入力を実施するクラス

	Attributes
	----------
	web_driver : WebDriver
		ChromeのWebドライバ用のクラス
	"""

	def __init__(self, web_driver):
		
		self.web_driver = web_driver
		self.result_logs = []
	

	def __PulldownMonth(self, pulldown):
		"""
		プルダウンで月移動を実施する

		Parameters
		----------
		pulldown : string
			プルダウンの移動対象

		Returns
		----------
		is_run : boolean
			月の移動実施フラグ(True：実施、False：未実施)
		"""
		# 入力月の移動
		if pulldown != '':
			# 「過去の記録を見る」のエレメントを取得
			box_element = self.web_driver.driver.find_element_by_xpath(XPATH.MONTH_SELECT_BOX)
			select_element = Select(box_element)
			# 移動先の月を選択
			select_element.select_by_value(pulldown)
			self.web_driver.Sleep()
			is_run = True
		else:
			is_run = False
		
		return is_run
	

	def __CheckMilageEnable(self, millage_id, week_id, day_id):
		"""
		入力項目が存在するかを確認する

		Parameters
		----------
		millage_id : int
			入力項目のID
		week_id : int
			週のID(カレンダーの行インデックス)
		day_id : int
			日にちのID(カレンダーの列インデックス)

		Returns
		----------
		is_success : boolean
			入力項目存在フラグ(True：あり、False：なし)
		"""
		try:
			# 日付ボタンの有無から入力項目があるかを判定
			date_xpath = XPATH.MILLAGE_DAY_BUTTON.format(millage_id, week_id, day_id)
			self.web_driver.driver.find_element_by_xpath(date_xpath)
			self.web_driver.Sleep()
			is_enable = True
		except:
			is_enable = False
		
		return is_enable

	
	def __ClickDayButton(self, millage_id, week_id, day_id):
		"""
		日付ボタンのクリックを実施する

		Parameters
		----------
		millage_id : int
			入力項目のID
		week_id : int
			週のID(カレンダーの行インデックス)
		day_id : int
			日にちのID(カレンダーの列インデックス)
		"""
		# 日付ボタンのxpathを取得し、クリック
		date_xpath = XPATH.MILLAGE_DAY_BUTTON.format(millage_id, week_id, day_id)
		self.web_driver.driver.find_element_by_xpath(date_xpath).click()
		self.web_driver.Sleep()


	
	def __JudgeCheckType(self):
		"""
		チェックボックスかラジオボックスかの判定をする

		Returns
		----------
		check_type : string
			タイプ文字列(CheckBox：チェックボックス、RadioBox：ラジオボック、空文字：その他)
		"""
		checklist = self.web_driver.driver.find_elements_by_xpath(XPATH.CHECK_CHECKLIST)
		radiolist = self.web_driver.driver.find_elements_by_xpath(XPATH.RADIO_CHECKLIST)

		# 閉じるボタンを含めないため、-1している
		check_num = len(checklist) - 1
		radio_num = len(radiolist)

		if check_num > 0:
			check_type = 'CheckBox'
		elif radio_num > 0:
			check_type = 'RadioBox'
		else:
			check_type = ''
		
		return check_type

	

	def __RecordCheckBox(self, date):
		"""
		チェックボックスの自動入力を実施する

		Parameters
		----------
		date : string
			入力する日付

		Returns
		----------
		close_button_idx : int
			閉じるボタンのHTML要素のインデックス位置
		"""
		# 各チェックボックスにチェック処理を行う
		checklist = self.web_driver.driver.find_elements_by_xpath(XPATH.CHECK_CHECKLIST)
		check_num = len(checklist) - 1
		close_button_idx = len(checklist)

		# 初回入力時の判別フラグ
		is_init_check = True

		for idx in range(check_num):
			# チェックボックスのelement取得
			check_checkbox_elem = self.web_driver.driver.find_element_by_xpath(XPATH.CHECK_CHECKBOX.format(idx + 1))
			check_checktext_elem = self.web_driver.driver.find_element_by_xpath(XPATH.CHECK_CHECKTEXT.format(idx + 1))
			self.web_driver.Sleep()
			
			# 未チェックのチェックボックスにチェックを入れる
			if check_checkbox_elem.get_attribute(XPATH.CHECK_ATTRIBUTE) == None:
				check_checkbox_elem.click()
				self.web_driver.Sleep()
				
				# 初回入力時、メッセージに日付を格納
				if is_init_check:
					self.result_logs.append('{}'.format(date))
					is_init_check = False
				# メッセージを格納
				self.result_logs.append(' - Checked [{}]'.format(check_checktext_elem.text))
			
		return close_button_idx
	

	def __RecordRadioBox(self, date):
		"""
		ラジオボックスの自動入力を実施する

		Parameters
		----------
		date : string
			入力する日付
		"""
		radiolist = self.web_driver.driver.find_elements_by_xpath(XPATH.RADIO_CHECKLIST)
		radio_num = len(radiolist)

		# 入力済みであるかを確認
		is_enable_check = False
		for idx in range(radio_num):
			radio_checkbox_elem = self.web_driver.driver.find_element_by_xpath(XPATH.RADIO_CHECKBOX.format(idx + 1))
			self.web_driver.Sleep()

			if radio_checkbox_elem.get_attribute(XPATH.CHECK_ATTRIBUTE) != None:
				is_enable_check = True
		
		# 入力済みでない場合、入力を実施
		if not is_enable_check:
			# チェックボックスのelement取得
			radio_checkbox_elem = self.web_driver.driver.find_element_by_xpath(XPATH.RADIO_CHECKBOX.format(1))
			radio_checktext_elem = self.web_driver.driver.find_element_by_xpath(XPATH.RADIO_CHECKTEXT.format(1))
			self.web_driver.Sleep()

			# チェックボックスにチェックを入れる
			radio_checkbox_elem.click()
			self.web_driver.Sleep()

			# メッセージを格納
			self.result_logs.append('{} - Checked [{}]'.format(date, radio_checktext_elem.text))


	def RecordCheck(self, date_list, millage_name, millage_id):
		"""
		チェック項目の自動入力を実施する

		Returns
		----------
		date_list : dict
			マイレージ内の日付ボタン押下用のDate情報
		millage_name : string
			マイレージ名
		millage_id : int
			マイレージID
		
		Returns
		----------
		result_log_list : list of string
			出力結果格納リスト
		"""
		header = '● Item : {}'.format(millage_name)
		prev_date = None
		milage_enable_flg = False
		result_log_list = []
		self.result_logs = None


		# 日付情報に基づいてデータを入力
		for date in date_list:
			
			# 入力月の移動
			is_move_month = self.__PulldownMonth(date['Pulldown'])
			# 月の移動をしたタイミングで項目が存在するかを確認
			if is_move_month:

				# 先月のデータの格納処理
				if self.result_logs != None:
					# 既にチェック入力されているかを判定
					if len(self.result_logs) == 0:
						date_tmp = datetime.strptime(prev_date['Date'], '%Y/%m/%d').strftime('%Y/%m/ALL')
						self.result_logs.append('{} : <Already Input>'.format(date_tmp))
					
					# 配列にスタック
					result_log_list.extend(self.result_logs)
				
				# 指定月に入力項目があるかを確認
				if self.__CheckMilageEnable(millage_id, date['Week']['Id'] + 1, date['Day']['Id'] + 1):
					# ログ格納リストを初期化
					self.result_logs = []
					milage_enable_flg = True
				else:
					# 入力項目が無いというメッセージをログに格納
					date_tmp = datetime.strptime(date['Date'], '%Y/%m/%d').strftime('%Y/%m/ALL')
					result_log_list.append('{} : <Empty>'.format(date_tmp))
					self.result_logs = None
					milage_enable_flg = False
			

			# 入力項目が存在する場合は、自動入力を実施する
			if milage_enable_flg:
				# 現在よりも後の日は除外
				if not date['Exist']: continue

				# 日付ボタンをクリック
				self.__ClickDayButton(millage_id, date['Week']['Id'] + 1, date['Day']['Id'] + 1)

				# チェックボックスかラジオボックスかを判定
				check_type = self.__JudgeCheckType()

				# チェックボックスかラジオボックスの入力処理を実施
				if check_type == 'CheckBox':
					close_button_idx = self.__RecordCheckBox(date['Date'])
					self.web_driver.driver.find_element_by_xpath(XPATH.CHECK_CLOSE_BUTTON.format(close_button_idx)).click()
					self.web_driver.Sleep()
				elif check_type == 'RadioBox':
					self.__RecordRadioBox(date['Date'])
					self.web_driver.driver.find_element_by_xpath(XPATH.RADIO_RECORD_BUTTON).click()
					self.web_driver.Sleep()

				# 過去値を保存
				prev_date = date
		

		# ログが残っていれば、ログ配列にスタックする
		if self.result_logs != None:
			# 既にチェック入力されているかを判定
			if len(self.result_logs) == 0:
				date_tmp = datetime.strptime(prev_date['Date'], '%Y/%m/%d').strftime('%Y/%m/ALL')
				self.result_logs.append('{} : <Already Input>'.format(date_tmp))
			
			# 配列にスタック
			result_log_list.extend(self.result_logs)

		# ヘッダを格納
		result_log_list.insert(0, header)

		return result_log_list