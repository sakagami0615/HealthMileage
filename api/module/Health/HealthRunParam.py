# ----------------------------------------------------------------------------------------------------
# モジュールフォルダのパスを追加
# ----------------------------------------------------------------------------------------------------
import os, sys
if os.path.basename(os.getcwd()) == 'HealthMileage':
	sys.path.append('api')
elif os.path.basename(os.getcwd()) == 'test':
	os.chdir('../../')
	sys.path.append('api')
elif os.path.basename(os.getcwd()) == 'api':
	os.chdir('../')
	sys.path.append('api')
else:
	exit()


# ----------------------------------------------------------------------------------------------------
# モジュールimport
# ----------------------------------------------------------------------------------------------------
import json
import numpy
import matplotlib.pyplot as plt

from module.Main.MainParam import Param as MAINPARAM
from module.Health.HealthParam import Param as HEALTHPARAM


# ----------------------------------------------------------------------------------------------------
# RunParamクラス
# ----------------------------------------------------------------------------------------------------
class HealthRunParam:
	
	def __init__(self):
		pass


	# ----------------------------------------------------------------------------------------------------
	# パラメータリストに記載した条件を満たすかどうかを判定する
	# ----------------------------------------------------------------------------------------------------
	def __GetSwitchFlg(self, switch, value):
			# 条件を満たす場合は抜ける(xはcondition内で利用されている)
			x = value
			if eval(switch):
				return 1
			del x
			return 0
	
	
	# ----------------------------------------------------------------------------------------------------
	# 指定された条件から、生成するrangeを取得する
	# ----------------------------------------------------------------------------------------------------
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
		
		if thresh_min < thresh_max:
			rand_range = [thresh_min, thresh_max]
		else:
			rand_range = [thresh_max, thresh_min]

		return rand_range


	# ----------------------------------------------------------------------------------------------------
	# 自動入力の有効/無効のパラメータをプロットする
	# ----------------------------------------------------------------------------------------------------
	def __SaveInputFlagValue(self, file_path, save_path):

		with open(file_path) as f:
			load_value_info = json.load(f)
		
		# データ作成
		X = []
		Y = []
		for mileage_key in HEALTHPARAM.MILEAGE_KEY:
			x = []
			y = []
			for week_key in HEALTHPARAM.WEEKDAY_KEY:
				x.append(week_key)
				y.append(load_value_info[week_key][mileage_key])
			X.append(x)
			Y.append(y)
		
		# グラフ描画
		fig = plt.figure(figsize=MAINPARAM.PARAM_IMG_SIZE_INCH)
		fig.patch.set_facecolor('xkcd:mint green')			# Figure背景色の設定

		for (idx, key) in enumerate(HEALTHPARAM.MILEAGE_KEY):

			ax = fig.add_subplot(3, 2, idx + 1)
			ax.step(X[idx], Y[idx], label='InputFlag')
			ax.set_title(key)
			ax.legend(loc="upper right")					# 凡例の表示 (locで表示位置を設定可)
			ax.grid(True)									# Gridの表示
			plt.setp(ax.get_xticklabels(), rotation=60)		# X軸ラベルを回転

		fig.tight_layout()              					# subplot表示位置の調整

		plt.savefig(save_path)
		plt.close(fig)


	# ----------------------------------------------------------------------------------------------------
	# 条件パラメータをプロットする
	# ----------------------------------------------------------------------------------------------------
	def __SaveSwitchValue(self, file_path, save_path):

		with open(file_path) as f:
			load_value_info = json.load(f)

		# データ作成
		X = []
		Y_switch = []
		Y_range = []
		for key in HEALTHPARAM.WEEKDAY_KEY:
			switch_data = load_value_info[key]['Switch']
			range_data = load_value_info[key]['Range']
			step_data = load_value_info[key]['Step']

			switch_thresh = self.__GetCreateRandRange(switch_data)
			data_range_min = switch_thresh[0] - switch_thresh[1]*0.1
			data_range_max = switch_thresh[1] + switch_thresh[1]*0.1

			x = numpy.arange(data_range_min, data_range_max, step_data*0.1)
			switch_y = [self.__GetSwitchFlg(switch_data, d) for d in x]
			range_y = [self.__GetSwitchFlg(range_data, d) for d in x]

			X.append(x)
			Y_switch.append(switch_y)
			Y_range.append(range_y)

		
		# グラフ描画
		fig = plt.figure(figsize=MAINPARAM.PARAM_IMG_SIZE_INCH)
		fig.patch.set_facecolor('xkcd:mint green')		# Figure背景色の設定
		
		for (idx, key) in enumerate(HEALTHPARAM.WEEKDAY_KEY):

			ax = fig.add_subplot(4, 2, idx + 1)
			ax.step(X[idx], Y_switch[idx], label='switch')
			ax.step(X[idx], Y_range[idx], linestyle='dashed', label='range')
			ax.set_title(key)
			ax.legend(loc="upper right")		# 凡例の表示 (locで表示位置を設定可)
			ax.grid(True)						# Gridの表示
		
		fig.tight_layout()              		#subplot表示位置の調整
		
		plt.savefig(save_path)
		plt.close(fig)
	

	# ----------------------------------------------------------------------------------------------------
	# パラメータ確認処理
	# ----------------------------------------------------------------------------------------------------
	def RunParam(self):

		# 各種パラメータ描画画像を作成して保存
		self.__SaveInputFlagValue(HEALTHPARAM.INPUT_FLG_PATH, MAINPARAM.PARAM_FLG_IMG_PATH)
		self.__SaveSwitchValue(HEALTHPARAM.STEP_VALUE_INFO_PATH, MAINPARAM.PARAM_STEP_IMG_PATH)
		self.__SaveSwitchValue(HEALTHPARAM.SLEEP_VALUE_INFO_PATH, MAINPARAM.PARAM_SLEEP_IMG_PATH)

		# 戻り値用変数の用意(resultsは、文字列に変換している)
		is_success = True
		ack_message = 'Send Parammeter Plot Images'
		for (idx, img_path) in enumerate(MAINPARAM.PARAM_IMG_PATHS):
			message = '・No.{} : {}'.format(idx, img_path)
			ack_message = '{}\n{}'.format(ack_message, message)

		return (is_success, ack_message)

