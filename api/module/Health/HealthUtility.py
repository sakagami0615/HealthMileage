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
import datetime
import math
import random
import time

from module.Health.HealthParam import Param as HEALTHPARAM


# ----------------------------------------------------------------------------------------------------
# 指定されたレンジとステップ値を利用して、乱数を取得
# ----------------------------------------------------------------------------------------------------
def GetRand(range, step, switch=''):

	# レンジから最大、最小を取得
	max_value = max(range)
	min_value = min(range)

	# 小数を整数に変換するため、一括管理
	datas = [max_value, min_value, step]
	
	# 小数を整数に変換するためのスケール値算出
	scale = 1
	while True:
		# 小数が存在する値のみ残す
		datas = [(d*scale*10) for d in datas if ((d - math.floor(d)) != 0)]
		# 小数が存在しない場合はbreak
		if not datas:
			break
		# スケール値を10倍していく
		scale *= 10

	# 小数を整数に変換
	max_scale_value = scale*max_value
	min_scale_value = scale*min_value
	step_scale_value = scale*step
	
	# 条件がある場合は、それに従って乱数を生成
	if switch:
		while True:
			# 乱数を取得
			scale_value = random.randrange(int(min_scale_value), int(max_scale_value), int(step_scale_value))
			# 取得した乱数のスケールを戻す
			value = scale_value/scale
			# 条件を満たす場合は抜ける(xはcondition内で利用されている)
			x = value
			if eval(switch):
				break
			del x
	
	# 条件がない場合は、そのまま乱数を取得
	else:
		# 乱数を取得
		scale_value = random.randrange(int(min_scale_value), int(max_scale_value), int(step_scale_value))
		# 取得した乱数のスケールを戻す
		value = scale_value/scale
	
	# 整数の場合は、intでキャスト
	if scale == 1:
		value = int(value)
	
	return value


# ----------------------------------------------------------------------------------------------------
# 指定時間待機
# ----------------------------------------------------------------------------------------------------
def Sleep(mode='rand'):

	if mode == 'rand':
		# ランダム待機時間(ミリ秒)を取得
		waittime_ms = GetRand(HEALTHPARAM.SLEEP_TIME_MS_RANGE, HEALTHPARAM.SLEEP_TIME_MS_STEP)
		# ミリ秒を秒に変換
		waittime_s = waittime_ms * HEALTHPARAM.COEF_MSEC2SEC
		# 待機
		time.sleep(waittime_s)
	
	elif mode == 'delta':
		# 微小時間待機
		waittime_s = 0.1
		time.sleep(waittime_s)
	
	else:
		waittime_s = 0

	# 何秒待機したかを返す
	return waittime_s


# ----------------------------------------------------------------------------------------------------
# マイレージ内の日付ボタン押下用のDate情報を用意
# ----------------------------------------------------------------------------------------------------
def GetDateInfo():
	
	# ------------------------------------------------------------------------------------------------
	# 月のDate情報を取得する 
	# ------------------------------------------------------------------------------------------------
	def OneMonth(date):

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
			weekday = HEALTHPARAM.WEEKDAY_KEY[day_id]
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
	# ------------------------------------------------------------------------------------------------
	# ------------------------------------------------------------------------------------------------
	

	# 現在の時刻を取得
	now_date = datetime.datetime.now()
	# 本月の日程を取得
	infos = OneMonth(now_date)
	# 入力締め切り前なら、前月の日程を取得
	if now_date.day < HEALTHPARAM.ALLOW_LAST_MONTH_THRESH_DAY:
		prev_date = datetime.datetime(now_date.year, now_date.month, 1)
		prev_date = prev_date - datetime.timedelta(days=1)
		prev_info = OneMonth(prev_date)
		infos.extend(prev_info)

	return infos