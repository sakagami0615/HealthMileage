from datetime import datetime
from selenium.webdriver.support.ui import Select
from src import ErrorLog
from src import Parameter as PARAM
from src.Parameter import XPATH


class HealthAutofillValue:
	"""
	数値入力項目の自動入力を実施するクラス

	Attributes
	----------
	web_driver : WebDriver
		ChromeのWebドライバ用のクラス
	"""

	def __init__(self, web_driver):
		
		self.web_driver = web_driver
	

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
	

	def RecordValue(self, date_list, millage_name, millage_id, generator):
		"""
		値入力項目の自動入力を実施する

		Parameters
		----------
		date_list : dict
			マイレージ内の日付ボタン押下用のDate情報
		millage_name : string
			マイレージ名
		millage_id : int
			マイレージID
		generator : class
			乱数生成器
		
		Returns
		----------
		result_log_list : list of string
			出力結果格納リスト
		"""
		header = '● Item : {}'.format(millage_name)
		prev_date = None
		milage_enable_flg = False
		result_log_list = []
		result_logs = None


		# 日付情報に基づいてデータを入力
		for date in date_list:
			
			# 入力月の移動
			is_move_month = self.__PulldownMonth(date['Pulldown'])
			# 月の移動をしたタイミングで項目が存在するかを確認
			if is_move_month:

				# 先月のデータの格納処理
				if result_logs != None:
					# 既にチェック入力されているかを判定
					if len(result_logs) == 0:
						date_tmp = datetime.strptime(prev_date['Date'], '%Y/%m/%d').strftime('%Y/%m/ALL')
						result_logs.append('{} : <Already Input>'.format(date_tmp))
					
					# 配列にスタック
					result_log_list.extend(result_logs)
				
				# 指定月に入力項目があるかを確認
				if self.__CheckMilageEnable(millage_id, date['Week']['Id'] + 1, date['Day']['Id'] + 1):
					# ログ格納リストを初期化
					result_logs = []
					milage_enable_flg = True
				else:
					# 入力項目が無いというメッセージをログに格納
					date_tmp = datetime.strptime(date['Date'], '%Y/%m/%d').strftime('%Y/%m/ALL')
					result_log_list.append('{} : <Empty>'.format(date_tmp))
					result_logs = None
					milage_enable_flg = False
			

			# 入力項目が存在する場合は、自動入力を実施する
			if milage_enable_flg:
				# 現在よりも後の日は除外
				if not date['Exist']: continue

				# 日付ボタンをクリック
				self.__ClickDayButton(millage_id, date['Week']['Id'] + 1, date['Day']['Id'] + 1)

				# テキストボックスのelement取得
				textbox_elem = self.web_driver.driver.find_element_by_xpath(XPATH.INPUT_TEXTBOX)
				self.web_driver.Sleep()

				# 現在の入力値を取得
				value_text = textbox_elem.get_attribute('value')

				# 現在の入力がない場合
				if value_text == '':
					# 入力値を生成して入力する
					input_text = str(generator.Generate())
					textbox_elem.send_keys(input_text)
					self.web_driver.Sleep()
					
					# 記録ボタンをクリック
					self.web_driver.driver.find_element_by_xpath(XPATH.INPUT_DONE_BUTTON).click()
					self.web_driver.driver.find_element_by_xpath(XPATH.INPUT_CANCEL_BUTTON).click()
					self.web_driver.Sleep()

					# メッセージを格納
					result_logs.append('{} - Input [{}]'.format(date['Date'], input_text))

				# 現在の入力がある場合
				else:
					# キャンセルボタンをクリック
					self.web_driver.driver.find_element_by_xpath(XPATH.INPUT_CANCEL_BUTTON).click()
					self.web_driver.Sleep()
					
				# 過去値を保存
				prev_date = date
		

		# ログが残っていれば、ログ配列にスタックする
		if result_logs != None:
			# 既にチェック入力されているかを判定
			if len(result_logs) == 0:
				date_tmp = datetime.strptime(prev_date['Date'], '%Y/%m/%d').strftime('%Y/%m/ALL')
				result_logs.append('{} : <Already Input>'.format(date_tmp))
			
			# 配列にスタック
			result_log_list.extend(result_logs)

		# ヘッダを格納
		result_log_list.insert(0, header)

		return result_log_list
