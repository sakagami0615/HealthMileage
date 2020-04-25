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
# Confirmクラス
# ----------------------------------------------------------------------------------------------------
class HealthRunConfirm(HealthDriver):
	
	def __init__(self):
		super().__init__()

		# ログイン情報ファイルの読み込み
		with open(HEALTHPARAM.PROFILE_PATH, 'r', encoding='utf-8') as f:
			self.__profile = json.load(f)

	
	# --------------------------------------------------------------------------------
	# テキスト入力箇所（歩数、睡眠時間）の値を取得する
	# --------------------------------------------------------------------------------
	def __ConfirmInput(self, date_infos, millage_name, millage_id):
		
		header = '● Item : {}'.format(millage_name)
		results = []

		# 日付情報に基づいてデータを取得
		for date_info in tqdm(date_infos):

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
			
			# 日付ボタンのxpathを取得し、クリック
			try:
				date_xpath = XPATH.MILLAGE_DAY_BUTTON.format(millage_id, date_info['Week']['Id'] + 1, date_info['Day']['Id'] + 1)
				self.driver.find_element_by_xpath(date_xpath).click()
				HealthUtility.Sleep()
			except:
				results.append('{} : <Empty>'.format(date_info['Date']))
				continue
			
			# テキストボックスのelement取得
			textbox_elem = self.driver.find_element_by_xpath(XPATH.INPUT_TEXTBOX)
			
			# 入力データの確認
			value = textbox_elem.get_attribute('value')
			if value != '':
				results.append('{} : {}'.format(date_info['Date'], value))
			else:
				results.append('{} : <Empty>'.format(date_info['Date']))
			
			# 閉じるをクリック
			try:
				self.driver.find_element_by_xpath(XPATH.INPUT_CANCEL_BUTTON).click()
				HealthUtility.Sleep()
			except:
				self.driver.find_element_by_xpath(XPATH.INPUT_CLOSE_BUTTON).click()
				HealthUtility.Sleep()

		# ヘッダ格納
		ack = [header]
		ack.extend(results)

		return ack


	# --------------------------------------------------------------------------------
	# チェック入力箇所（睡眠、アルコール、食生活）のチェック状態を取得する
	# --------------------------------------------------------------------------------
	def __ConfirmCheck(self, date_infos, millage_name, millage_id):
				
		header = '● Item : {}'.format(millage_name)
		results = []

		# 日付情報に基づいてデータを入力
		for date_info in tqdm(date_infos):

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

			# 日付格納
			results.append('・{}'.format(date_info['Date']))

			# 日付ボタンのxpathを取得し、クリック
			try:
				date_xpath = XPATH.MILLAGE_DAY_BUTTON.format(millage_id, date_info['Week']['Id'] + 1, date_info['Day']['Id'] + 1)
				self.driver.find_element_by_xpath(date_xpath).click()
				HealthUtility.Sleep()
			except:
				results.append(' - <Empty>')
				continue
			
			
			# 各チェックボックスにチェック処理を行う
			check_list = self.driver.find_elements_by_xpath(XPATH.CHECK_CHECKLIST)

			for idx in range(len(check_list) - 1):
				# チェックボックスのelement取得
				checkbox_elem = self.driver.find_element_by_xpath(XPATH.CHECK_CHECKBOX.format(idx + 1))
				checktext_elem = self.driver.find_element_by_xpath(XPATH.CHECK_CHECKTEXT.format(idx + 1))
				HealthUtility.Sleep('delta')

				if checkbox_elem.get_attribute("checked") != None:
					results.append(' - Checked [{}]'.format(checktext_elem.text))

				else: 
					results.append(' - Not Checked [{}]'.format(checktext_elem.text))
			
			# 閉じるをクリック
			self.driver.find_element_by_xpath(XPATH.CHECK_CLOSE_BUTTON.format(len(check_list))).click()
			HealthUtility.Sleep()
		
		# ヘッダ格納
		ack = [header]
		ack.extend(results)

		return ack
	

	# ----------------------------------------------------------------------------------------------------
	# 入力データ確認処理
	# ----------------------------------------------------------------------------------------------------
	def RunConfirm(self):

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
			millage_name = key
			mileage_type = HEALTHPARAM.MILEAGE_TYPES[key]['Type']
			mileage_id = HEALTHPARAM.MILEAGE_TYPES[key]['Id']

			if mileage_type == 'Input':
				print('■ {}'.format(millage_name))
				results = self.__ConfirmInput(date_infos, millage_name, mileage_id)
				ack_results.extend(results)
			
			elif mileage_type == 'Check':
				print('■ {}'.format(millage_name))
				results = self.__ConfirmCheck(date_infos, millage_name, mileage_id)
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
