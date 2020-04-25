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
import json
from tqdm import tqdm
from selenium.webdriver.support.ui import Select

from module.Health import HealthUtility
from module.Health.HealthDriver import HealthDriver
from module.Health.HealthParam import Param as HEALTHPARAM
from module.Health.HealthXPath import XPath as XPATH


# ----------------------------------------------------------------------------------------------------
# Recordクラス
# ----------------------------------------------------------------------------------------------------
class HealthRunRecord(HealthDriver):
	
	def __init__(self):
		super().__init__()
		
		# ログイン情報ファイルの読み込み
		with open(HEALTHPARAM.PROFILE_PATH, 'r', encoding='utf-8') as f:
			self.__profile = json.load(f)

		# パラメータファイルの読み込み
		with open(HEALTHPARAM.INPUT_FLG_PATH) as f:
			input_flg = json.load(f)
		with open(HEALTHPARAM.STEP_VALUE_INFO_PATH) as f:
			step_value_info = json.load(f)
		with open(HEALTHPARAM.SLEEP_VALUE_INFO_PATH) as f:
			sleep_value_info = json.load(f)
		
		self.__param = self.__MediateParam(input_flg, step_value_info, sleep_value_info)


	# --------------------------------------------------------------------------------
	# パラメータファイルの調停
	# --------------------------------------------------------------------------------
	def __MediateParam(self, input_flg, step_value_info, sleep_value_info):

		# 初期化
		param = {}
		for mile_key in HEALTHPARAM.MILEAGE_KEY:
			param[mile_key] = {'Week': {}, 'IsRun': 0}
			for week_key in HEALTHPARAM.WEEKDAY_KEY:
				param[mile_key]['Week'][week_key] = {}
		
		# 実行必要フラグを格納
		for week_key in HEALTHPARAM.WEEKDAY_KEY:
			for mile_key in HEALTHPARAM.MILEAGE_KEY:
				param[mile_key]['IsRun'] = param[mile_key]['IsRun'] or input_flg[week_key][mile_key]

		# 各曜日のフラグを格納
		for week_key in HEALTHPARAM.WEEKDAY_KEY:
			for mile_key in HEALTHPARAM.MILEAGE_KEY:
				param[mile_key]['Week'][week_key]['Flag'] = input_flg[week_key][mile_key]

		# Stepのパラメータ格納
		for week_key in HEALTHPARAM.WEEKDAY_KEY:
			param['StepInput']['Week'][week_key]['Data'] = step_value_info[week_key]

		# Sleepのパラメータ格納
		for week_key in HEALTHPARAM.WEEKDAY_KEY:
			param['SleepInput']['Week'][week_key]['Data'] = sleep_value_info[week_key]
		
		return param


	# --------------------------------------------------------------------------------
	# パラメータリストに記載した条件から、値を入力するかどうかを確認する
	# --------------------------------------------------------------------------------
	def __CheckUpdateInput(self, value, condition):
	
		# 条件がある場合は、条件に合うかを調べる
		if condition:
			x = value
			is_input = eval(condition)
			del x
		# 条件がない場合は、そのままTrueを返す
		else:
			is_input = True
		
		return is_input
	

	# --------------------------------------------------------------------------------
	# 指定された範囲を利用して、生成する乱数のrangeを取得する
	# --------------------------------------------------------------------------------
	def __GetCreateRandRange(self, input_thresh):

		# 初期化
		thresh_min = HEALTHPARAM.DEFAULT_RAND_MIN
		thresh_max = HEALTHPARAM.DEFAULT_RAND_MAX
		

		split_thresh = []

		# 空文字を削除
		re_input_thresh = input_thresh.replace(' ', '')
		
		# 論理演算を分割する
		split_or = re_input_thresh.split('or')
		for split in split_or:
			split_or_and = split.split('and')
			split_thresh.extend(split_or_and)

		# 残ったかっこ文字の削除
		split_thresh = [split.replace(')', '') for split in split_thresh]
		split_thresh = [split.replace('(', '') for split in split_thresh]

		max_list = []
		min_list = []

		# 条件演算文字を削除し、閾値を取得
		for split in split_thresh:
			if split.find('x<=') != -1:
				thresh_num = eval(split.replace('x<=', ''))
				max_list.append(thresh_num)
				continue
			if split.find('x<') != -1:
				thresh_num = eval(split.replace('x<', ''))
				max_list.append(thresh_num)
				continue
		for split in split_thresh:
			if split.find('x>=') != -1:
				thresh_num = eval(split.replace('x>=', ''))
				min_list.append(thresh_num)
				continue
			if split.find('x>') != -1:
				thresh_num = eval(split.replace('x>', ''))
				min_list.append(thresh_num)
				continue
		
		# 閾値が取得できた場合、maxminをとり、返り値に渡す
		if max_list:
			thresh_max = max(max_list)
		if min_list:
			thresh_min = min(min_list)
		
		rand_range = [thresh_min, thresh_max]
		return rand_range


	# --------------------------------------------------------------------------------
	# テキスト入力箇所（歩数、睡眠時間）を自動で入力する
	# --------------------------------------------------------------------------------
	def __RecordInput(self, date_infos, millage_name, millage_id, param):

		header = '● Item : {}'.format(millage_name)
		results = []

		# 日付情報に基づいてデータを入力
		for date_info in tqdm(date_infos):
			
			curr_week = date_info['Day']['DayOfWeek']
			curr_param = param[curr_week]

			# 入力月の移動
			if date_info['Pulldown'] != '':
				# 「過去の記録を見る」のエレメントを取得
				box_element = self.driver.find_element_by_xpath(XPATH.MONTH_SELECT_BOX)
				select_element = Select(box_element)
				# 移動先の月を選択
				select_element.select_by_value(date_info['Pulldown'])

			# 現在よりも後の日は除外
			if date_info['Exist'] == False:
				continue

			# 入力が無効の場合は除外
			if not curr_param['Flag']:
				results.append('{} : Input Flag is <false>'.format(date_info['Date']))
				continue

			try:
				# 日付ボタンのxpathを取得し、クリック
				date_xpath = XPATH.MILLAGE_DAY_BUTTON.format(millage_id, date_info['Week']['Id'] + 1, date_info['Day']['Id'] + 1)
				self.driver.find_element_by_xpath(date_xpath).click()
				HealthUtility.Sleep()
			except:
				results.append('{} : <Empty>'.format(date_info['Date']))
				continue

			# テキストボックスのelement取得
			textbox_elem = self.driver.find_element_by_xpath(XPATH.INPUT_TEXTBOX)
			HealthUtility.Sleep('delta')

			# 現在の入力値を取得
			value_text = textbox_elem.get_attribute('value')
			
			# 入力データの確認し、必要があれば消去する
			if value_text != '':
				try:
					is_input = self.__CheckUpdateInput(float(value_text), curr_param['Data']['Switch'])

					# 入力条件に当てはまる場合は、消去する
					if is_input:
						textbox_elem.clear()
						HealthUtility.Sleep('delta')
						
					# 入力条件に当てはまらない場合は、Continueする
					else:
						self.driver.find_element_by_xpath(XPATH.INPUT_CANCEL_BUTTON).click()
						HealthUtility.Sleep()
				except:
					results.append('{} : <Can Not Update>'.format(date_info['Date']))
					self.driver.find_element_by_xpath(XPATH.INPUT_CLOSE_BUTTON).click()
					HealthUtility.Sleep()
					continue
			else:
				is_input = True
			
			# 入力フラグが立っている場合は、入力する
			if is_input:
				try:
					# データの入力
					rand_thresh = self.__GetCreateRandRange(curr_param['Data']['Range'])
					step_value = float(curr_param['Data']['Step'])
					range_condition = curr_param['Data']['Range']
					
					input_text = str(HealthUtility.GetRand(rand_thresh, step_value, range_condition))

					textbox_elem.send_keys(input_text)
					HealthUtility.Sleep('delta')

					if value_text != '':
						results.append('{} : Update Input  {} <- {}'.format(date_info['Date'], input_text, value_text))
					else:
						results.append('{} : New Input  {}'.format(date_info['Date'], input_text))
				except:
					results.append('{} : <Empty>'.format(date_info['Date']))

				try:
					# 更新をクリック
					self.driver.find_element_by_xpath(XPATH.INPUT_DONE_BUTTON).click()
					HealthUtility.Sleep()
				except:
					self.driver.find_element_by_xpath(XPATH.INPUT_CLOSE_BUTTON).click()
					HealthUtility.Sleep()

		# 入力がない場合のメッセージを格納
		if not results:
			results.append(' - Already Input All')

		# ヘッダ格納
		ack = [header]
		ack.extend(results)
		
		return ack


	# --------------------------------------------------------------------------------
	# チェック入力箇所（睡眠、アルコール、食生活）を自動で入力する
	# --------------------------------------------------------------------------------
	def __RecordCheck(self, date_infos, millage_name, millage_id, param):

		header = '● Item : {}'.format(millage_name)
		results = []
		
		# 日付情報に基づいてデータを入力
		for date_info in tqdm(date_infos):
			
			curr_week = date_info['Day']['DayOfWeek']
			curr_param = param[curr_week]

			# 入力月の移動
			if date_info['Pulldown'] != '':
				# 「過去の記録を見る」のエレメントを取得
				box_element = self.driver.find_element_by_xpath(XPATH.MONTH_SELECT_BOX)
				select_element = Select(box_element)
				# 移動先の月を選択
				select_element.select_by_value(date_info['Pulldown'])
			
			# 現在よりも後の日は除外
			if date_info['Exist'] == False:
				continue

			# 入力が無効の場合は除外
			if not curr_param['Flag']:
				results.append('{} : Check Flag is <false>'.format(date_info['Date']))
				continue
			
			try:
				# 日付ボタンのxpathを取得し、クリック
				date_xpath = XPATH.MILLAGE_DAY_BUTTON.format(millage_id, date_info['Week']['Id'] + 1, date_info['Day']['Id'] + 1)
				self.driver.find_element_by_xpath(date_xpath).click()
				HealthUtility.Sleep()
			except:
				results.append('{} : <Empty>'.format(date_info['Date']))
				continue

			# 各チェックボックスにチェック処理を行う
			check_list = self.driver.find_elements_by_xpath(XPATH.CHECK_CHECKLIST)
			HealthUtility.Sleep('delta')
			
			# 初回入力時の判別フラグ
			is_init_check = True

			try:
				for idx in range(len(check_list) - 1):
					# チェックボックスのelement取得
					checkbox_elem = self.driver.find_element_by_xpath(XPATH.CHECK_CHECKBOX.format(idx + 1))
					checktext_elem = self.driver.find_element_by_xpath(XPATH.CHECK_CHECKTEXT.format(idx + 1))
					HealthUtility.Sleep('delta')
					
					# 未チェックのチェックボックスにチェックを入れる
					if checkbox_elem.get_attribute(XPATH.CHECK_ATTRIBUTE) == None:
						checkbox_elem.click()
						HealthUtility.Sleep('delta')
						
						# 初回入力時、メッセージに日付を格納
						if is_init_check:
							results.append('{}'.format(date_info['Date']))
							is_init_check = False
						# メッセージを格納
						results.append(' - Checked [{}]'.format(checktext_elem.text))
				
				# 閉じるをクリック
				self.driver.find_element_by_xpath(XPATH.CHECK_CLOSE_BUTTON.format(len(check_list))).click()
				HealthUtility.Sleep()
			except:
				self.driver.find_element_by_xpath(XPATH.CHECK_CLOSE_BUTTON.format(len(check_list))).click()
				HealthUtility.Sleep()
		
		
		# 入力がない場合のメッセージを格納
		if not results:
			results.append(' - Already Check All')
		
		# ヘッダ格納
		ack = [header]
		ack.extend(results)

		return ack
	

	# ----------------------------------------------------------------------------------------------------
	# 自動入力処理
	# ----------------------------------------------------------------------------------------------------
	def RunRecord(self):
		
		# マイレージ内の日付ボタン押下用のDate情報を用意
		date_infos = HealthUtility.GetDateInfo()

		# ChromeDriver等の用意
		self.OpenDriver()
		
		# ack格納配列初期化
		ack_results = []
		ack_results.append('****************************************')

		# Pepupログイン処理
		is_login = self.Login(self.__profile['Adress'], self.__profile['Password'])
		
		# ログイン失敗時の処理
		if not is_login:
			self.CloseDriver()
			return (False, '')
	
		# わくわくマイレージにアクセス
		self.AccessMileage()
		
		# 入力データ確認処理
		for (idx, key) in enumerate(HEALTHPARAM.MILEAGE_KEY):

			if self.__param[key]['IsRun']:
				millage_name = key
				mileage_type = HEALTHPARAM.MILEAGE_TYPES[key]['Type']
				mileage_id = HEALTHPARAM.MILEAGE_TYPES[key]['Id']
				param = self.__param[key]['Week']
				
				if mileage_type == 'Input':
					print('■ {}'.format(millage_name))
					results = self.__RecordInput(date_infos, millage_name, mileage_id, param)
					ack_results.extend(results)
				
				elif mileage_type == 'Check':
					print('■ {}'.format(millage_name))
					results = self.__RecordCheck(date_infos, millage_name, mileage_id, param)
					ack_results.extend(results)
			
			if idx < (HEALTHPARAM.MILEAGE_TYPE_NUM - 1): ack_results.append('')
	
		ack_results.append('****************************************')

		# ChromeDriverのクローズ
		self.CloseDriver()

		# 戻り値用変数の用意(resultsは、文字列に変換している)
		is_success = True
		ack_message = ack_results.pop(0)
		for result in ack_results:
			ack_message = '{}\n{}'.format(ack_message, result)
		
		return (is_success, ack_message)
