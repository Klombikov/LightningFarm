import json
import os

class LoadAndSaveFile():
	def LoadFile(self, file):
		data = {}
		if not os.path.exists(file):
			return data
		with open(file, "r",  encoding='utf-8') as file:
			data = json.load(file)
		return data

	def SaveFile(self, file, data):
		directory = os.path.dirname(file)
		if not os.path.exists(directory):
			os.makedirs(directory)
		with open(file, "w",  encoding='utf-8') as writeFile:
			json.dump(data, writeFile, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
			
jsonLoader = LoadAndSaveFile()