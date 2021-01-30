import datetime


class DataGenerator:

	def __init__(self):
		pass

	
	# ------------------------------------------------------------------------------------------------
	# 月のDate情報を生成する 
	# ------------------------------------------------------------------------------------------------
	def __GenerateOneMonthDate(self, date):

		WEEKDAY_KEY = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
		
		# 時刻を取得
		curr_date = datetime.datetime(date.year, date.month, 1)
		
		# 日時リストを取得
		infos = []
		week_id = 0
		while True:

			# 今現在の月を超えたら、ループを抜ける
			if date.month != curr_date.month:
				break
			
			# 日時、日にちID(カレンダー位置)、曜日、経過した日時かどうか、を取得
			date_str = curr_date.strftime('%Y/%m/%d')
			day_id = curr_date.weekday()
			weekday = WEEKDAY_KEY[day_id]
			day_exist = (date.day >= curr_date.day)
			
			# 初日のタイミングでプルダウンメニューを決める
			pulldown_item = ''
			if curr_date.day == 1:
				pulldown_item = '/scsk_mileage_campaigns/{}/{}'.format(date.year, date.month)

			# 辞書を作成し、リストに格納
			info = {
				'Date'    : date_str,
				'Pulldown': pulldown_item,
				'Week'    : {'Id': week_id},
				'Day'     : {'Id': (day_id + 1)%7, 'DayOfWeek': weekday},
				'Exist'   : day_exist
			}
			infos.append(info)

			# 週のID（第何週か）を計算
			curr_date = curr_date + datetime.timedelta(days=1)
			if ((curr_date.weekday() + 1) % 7) == 0:
				week_id += 1
		
		return infos
	

	# ----------------------------------------------------------------------------------------------------
	# マイレージ内の日付ボタン押下用のDate情報を用意
	# ----------------------------------------------------------------------------------------------------
	def Generate(self):
		ALLOW_LAST_MONTH_THRESH_DAY = 10

		# 現在の時刻を取得
		now_date = datetime.datetime.now()
		# 本月の日程を取得
		infos = self.__GenerateOneMonthDate(now_date)
		# 入力締め切り前なら、前月の日程を取得
		if now_date.day < ALLOW_LAST_MONTH_THRESH_DAY:
			prev_date = datetime.datetime(now_date.year, now_date.month, 1)
			prev_date = prev_date - datetime.timedelta(days=1)
			prev_info = self.__GenerateOneMonthDate(prev_date)
			infos.extend(prev_info)

		return infos
		