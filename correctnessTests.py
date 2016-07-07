#!/usr/bin/python

import os

class CorrectnessTests:
	__infoFileName = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")

	def infoFileExistence(self):
		if (os.path.isfile(self.__infoFileName) != True) or (os.stat(self.__infoFileName).st_size == 0):
			self.infoFileCreation(self.__infoFileName)
			return 1
		return 0

	def __infoFileCreation(self):
		infoFile = open(self.__infoFileName, 'w')
		infoFile.write("-1")
		infoFile.close()

	def projectSelection(self):
		infoFile = open(self.__infoFileName, 'r')
		line = infoFile.readline()
		infoFile.close()
		return (len(line.split()) != 3) or (not line.split()[0].isdigit()) or (line.split()[0] == "-1")

	def projectFileExistence(self, line):
		projectName = line.split()[1]
		projectPath = os.path.join(line.split()[2], projectName + extension)
		return not (os.path.isfile(projectPath) or os.stat(projectPath).st_size == 0)

	def fileExistence(self, filePath):
		return os.path.isfile(filePath)