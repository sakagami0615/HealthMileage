import math
import random


class RandomGenerator:
	"""
	乱数生成クラス

	Attributes
	----------
	max_value : int or float
		乱数生成範囲(最大値)
	min_value : int or float
		乱数生成範囲(最小値)
	step_value : int or float
		生成乱数の刻み幅
	"""

	def __init__(self, value_1, value_2, step_value):
		
		self.__max_value = max(value_1, value_2)
		self.__min_value = min(value_1, value_2)
		self.__step_value = step_value
	
	# ----------------------------------------------------------------------------------------------------
	# 指定されたレンジとステップ値を利用して、乱数を生成
	# ----------------------------------------------------------------------------------------------------
	def Generate(self):
		"""
		予め指定したレンジとステップ値を利用して、乱数を生成

		Returns
		----------
		generate_value : int or float
			生成乱数
		"""

		# 小数を整数に変換するため、一括管理
		datas = [self.__max_value, self.__min_value, self.__step_value]
		
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
		max_scale_value = scale*self.__max_value
		min_scale_value = scale*self.__min_value
		step_scale_value = scale*self.__step_value
		
		# 乱数を取得
		scale_value = random.randrange(int(min_scale_value), int(max_scale_value), int(step_scale_value))
		# 取得した乱数のスケールを戻す
		generate_value = scale_value/scale
		
		# 整数の場合は、intでキャスト
		if scale == 1:
			generate_value = int(generate_value)
		
		return generate_value
