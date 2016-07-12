#!/usr/bin/python

import sublime, sublime_plugin, os

extension = ".pem"

class CorrectnessTests:
	__infoFilePath = ""

	def __init__(self):
		self.__infoFilePath = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")

	def infoFileExistence(self):
		if (os.path.isfile(self.__infoFilePath) != True) or (os.stat(self.__infoFilePath).st_size == 0):
			self.infoFileCreation(self.__infoFilePath)
			return 1
		return 0

	def __infoFileCreation(self):
		infoFile = open(self.__infoFilePath, 'w')
		infoFile.write("-1")
		infoFile.close()

	def projectSelection(self):
		infoFile = open(self.__infoFilePath, 'r')
		line = infoFile.readline()
		infoFile.close()
		return not ((len(line.split()) == 3) and (line.split()[0].isdigit()) and (int(line.split()[0]) > 0))

	def projectFileExistence(self, projectName, projectDir):
		projectPath = os.path.join(projectDir, projectName + extension)
		if os.path.isfile(projectPath):
			return os.stat(projectPath).st_size == 0
		return not (os.path.isfile(projectPath))

	def projectFileCorrectness(self, projectName, projectDir):
		projectPath = os.path.join(projectDir, projectName + extension)
		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		projectFile.close()
		if not "project_name = " in lines[0]:
			return 1
		elif not "specification:\n" in lines:
			return 2
		elif not "source:\n" in lines:
			return 3
		return 0

	def fileExistence(self, fileName, filePath):
		return os.path.isfile(os.path.join(filePath, fileName))

	def infoFileCorrectnessLite(self):
		infoFile = open(self.__infoFilePath, 'r')
		lines = infoFile.readlines()
		line = lines[0].split()
		infoFile.close()
		if len(line) == 1:
			return str(line) != "-1"
		elif len(line) == 3:
			if str(line[0]).isdigit():
				n = int(line[0])
				for i in range(1, n):
					if len(lines[i].split()) != 2:
						return 3
				return 0
			return 2
		return 4

	def infoFileCorrectnessHard(self):
		infoFile = open(self.__infoFilePath, 'r')
		lines = infoFile.readlines()
		infoFile.close()
		linesWithFails = []
		projectsThatDoesNotExist = []
		if (self.infoFileCorrectnessLite()):
			return self.infoFileCorrectnessLite()
		if str(lines[0].split()[0]).isdigit():
			for i in range(1, len(lines)):
				if len(lines[i].split()) != 2:
					linesWithFails += i
				else:
					if self.projectFileExistence(lines[i].split()[0], lines[i].split()[1]):
						projectsThatDoesNotExist += i
		if (len(linesWithFails)):
			return 5
		if (len(projectsThatDoesNotExist)):
			return 6
		
