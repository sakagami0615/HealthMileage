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

from module.Health.HealthParam import Param as HEALTHPARAM


# ----------------------------------------------------------------------------------------------------
# 定数パラメータ
# ----------------------------------------------------------------------------------------------------
IMG_SIZE_INCH = (12, 8)


# ----------------------------------------------------------------------------------------------------
# パラメータリストに記載した条件を満たすかどうかを判定する
# ----------------------------------------------------------------------------------------------------
def __GetSwitchFlg(switch, value):
		# 条件を満たす場合は抜ける(xはcondition内で利用されている)
		x = value
		if eval(switch):
			return 1
		del x
		return 0


# ----------------------------------------------------------------------------------------------------
# 指定された条件から、生成するrangeを取得する
# ----------------------------------------------------------------------------------------------------
def __GetCreateRandRange(input_thresh):

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
def SaveInputFlagValue(id, file_path, title, save_path):

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
	fig = plt.figure(id, figsize=IMG_SIZE_INCH)
	fig.canvas.set_window_title(title)
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
	print('Save Success : {}'.format(save_path))


# ----------------------------------------------------------------------------------------------------
# 条件パラメータをプロットする
# ----------------------------------------------------------------------------------------------------
def SaveSwitchValue(id, file_path, title, save_path):

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

		switch_thresh = __GetCreateRandRange(switch_data)
		data_range_min = switch_thresh[0] - switch_thresh[1]*0.1
		data_range_max = switch_thresh[1] + switch_thresh[1]*0.1

		x = numpy.arange(data_range_min, data_range_max, step_data*0.1)
		switch_y = [__GetSwitchFlg(switch_data, d) for d in x]
		range_y = [__GetSwitchFlg(range_data, d) for d in x]

		X.append(x)
		Y_switch.append(switch_y)
		Y_range.append(range_y)

	
	# グラフ描画
	fig = plt.figure(id, figsize=IMG_SIZE_INCH)
	fig.canvas.set_window_title(title)
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
	print('Save Success : {}'.format(save_path))


if __name__ == '__main__':

	SaveInputFlagValue(1, HEALTHPARAM.INPUT_FLG_PATH, 'Input Flg Value', 'log/[Param]input_flg_image.png')
	SaveSwitchValue(2, HEALTHPARAM.STEP_VALUE_INFO_PATH, 'Step Switch Value', 'log/[Param]step_value_image.png')
	SaveSwitchValue(3, HEALTHPARAM.SLEEP_VALUE_INFO_PATH, 'Sleep Switch Value', 'log/[Param]sleep_value_image.png')
