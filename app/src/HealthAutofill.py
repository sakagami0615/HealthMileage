from app.src.HealthAutofillValue import HealthAutofillValue
from app.src.HealthAutofillCheck import HealthAutofillCheck
from app.src.DataGenerator import DataGenerator
from app.src.RandomGenerator import RandomGenerator
from app.src import LinePushMessage
from app.src import ErrorLog
from app.src.Parameter import PARAM
from app.src.Parameter import XPATH


class HealthAutofill:
	"""
	各種項目の自動入力を実施するクラス

	Attributes
	----------
	web_driver : WebDriver
		ChromeのWebドライバ用のクラス
	"""

	def __init__(self, web_driver):
		
		self.web_driver = web_driver


	def Record(self, flg_param, value_param):
		"""
		自動入力を実施する

		Returns
		----------
		flg_param : dict
			歩数、睡眠時間、チェックの自動入力実施フラグ
		value_param : dict
			歩数、睡眠時間の最大値、最小値
		"""
		# メッセージ格納リスト
		ack_results = []

		# わくわくマイレージにアクセス
		self.web_driver.driver.get(PARAM.MILLAGE_URL)
		self.web_driver.Sleep()

		# マイレージ内の日付ボタン押下用のDate情報を用意
		data_generator = DataGenerator()
		date_list = data_generator.Generate()
		
		# 自動入力用クラスを用意
		autofill_value = HealthAutofillValue(self.web_driver)
		autofill_check = HealthAutofillCheck(self.web_driver)

		# 歩数を入力
		if flg_param['StepInputFlg']:
			mileage_name = PARAM.STEP_MILEAGE_TYPE['Name']
			mileage_id = PARAM.STEP_MILEAGE_TYPE['Id']
			LinePushMessage.line_msg_obj.PushMessage(mileage_name + ' Process Now')

			step_generator = RandomGenerator(value_param['StepValueMin'], value_param['StepValueMax'], 1)
			results = autofill_value.RecordValue(date_list, mileage_name, mileage_id, step_generator)
			ack_results.extend(results)
		
		# 睡眠時間を入力
		if flg_param['SleepInputFlg']:
			mileage_name = PARAM.SLEEP_MILEAGE_TYPE['Name']
			mileage_id = PARAM.SLEEP_MILEAGE_TYPE['Id']
			LinePushMessage.line_msg_obj.PushMessage(mileage_name + ' Process Now')

			sleep_generator = RandomGenerator(value_param['SleepValueMin'], value_param['SleepValueMax'], 0.1)
			results = autofill_value.RecordValue(date_list, mileage_name, mileage_id, sleep_generator)
			if len(results) > 0: ack_results.append('')
			ack_results.extend(results)
		
		# 各種チェックを入力
		if flg_param['CheckFlg']:
			for check_type in PARAM.CHECK_MILEAGE_TYPES:
				mileage_name = check_type['Name']
				mileage_id = check_type['Id']
				LinePushMessage.line_msg_obj.PushMessage(mileage_name + ' Process Now')

				results = autofill_check.RecordCheck(date_list, mileage_name, mileage_id)
				if len(results) > 0: ack_results.append('')
				ack_results.extend(results)

		ack_message = '\n'.join(ack_results)
		return ack_message
