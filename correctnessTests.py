#!/usr/bin/python

import os

extension = ".pem"

class CorrectnessTests:
	__infoFilePath = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")

	@staticmethod
	def infoFileExistence(self):
		if (os.path.isfile(self.__infoFilePath) != True) or (os.stat(self.__infoFilePath).st_size == 0):
			self.infoFileCreation(self.__infoFilePath)
			return 1
		return 0

	@staticmethod
	def __infoFileCreation(self):
		infoFile = open(self.__infoFilePath, 'w')
		infoFile.write("-1")
		infoFile.close()

	@staticmethod
	def projectSelection(self):
		infoFile = open(self.__infoFilePath, 'r')
		line = infoFile.readline()
		infoFile.close()
		return not ((len(line.split()) == 3) and (line.split()[0].isdigit()) and (line.split()[0] == "-1"))

	@staticmethod
	def projectFileExistence(self, line):
		projectName = line.split()[1]
		projectPath = os.path.join(line.split()[2], projectName + extension)
		return not (os.path.isfile(projectPath) or os.stat(projectPath).st_size == 0)

	@staticmethod
	def projectFileCorrectness(self, line):
		projectName = line.split()[1]
		projectPath = os.path.join(line.split()[2], projectName + extension)
		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		projectFile.close()
		if not "project_name = " in lines[0]:
			return 1
		elif not "specifications:\n" in lines:
			return 2
		elif not "source:\n" in lines:
			return 3
		return 0

	@staticmethod
	def fileExistence(self, filePath):
		return os.path.isfile(filePath)

	@staticmethod
	def infoFileCorrectnessLite(self):
		infoFile = open(self.__infoFilePath, 'r')
		lines = infoFile.readlines()
		line = lines[0].split()
		infoFile.close()
		if len(line) == 1:
			if line.isdigit():
				if int(line) == -1:
					return 0
				return 1
			return 2
		elif len(line == 3):
			if line[0].isdigit():
				n = int(line[0])
				for i in range(1, n):
					if len(lines[i].split()) != 2:
						return 3
				return 0
			return 2
		return 4

	@staticmethod
	def infoFileCorrectnessHard(self):
		infoFile = open(self.__infoFilePath, 'r')
		lines = infoFile.readlines()
		infoFile.close()
		linesWithFails = []
		projectsThatDoesNotExist = []
		if (self.infoFileCorrectnessLite()):
			return self.infoFileCorrectnessLite()
		if line[0].isdigit():
			for i in range(1, len(lines)):
				if len(lines[i].split()) != 2:
					linesWithFails += i
				else:
					if self.projectFileExistence(lines[i]):
						projectsThatDoesNotExist += i
		if (len(linesWithFails)):
			return 5
		if (len(projectsThatDoesNotExist)):
			return 6
		


