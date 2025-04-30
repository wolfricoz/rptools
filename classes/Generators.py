import json
from abc import ABC, abstractmethod
import random


# noinspection PyMethodParameters
class Gen(ABC) :
	@staticmethod
	@abstractmethod
	async def name(gtype, amount) :
		with open(f'tools/{gtype}names.json', 'r') as f :
			data = json.load(f)
			x = 0
			names = []
			while x < amount :
				r = random.randint(0, len(data['names']))
				names.append(data['names'][r])
				x += 1
			return names
