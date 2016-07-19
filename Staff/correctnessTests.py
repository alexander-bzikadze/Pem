#!/usr/bin/python

import sublime, sublime_plugin, os

# List of tests to get needed kind of correctness.
# For now on, if test returns 0 - it went correctly, otherwise - incorrectly.

extension = ".pem"

class CorrectnessTests:
	__infoFilePath = ""

	# Constructor finds way to infofile.
	def __init__(self):
		self.__infoFilePath = os.path.join(sublime.packages_path(), "Pem", "Info.txt")

	# Checks infofile for existence and emptiness. If check failes, creates standart infofile.
	def infoFileExistence(self):
		if (os.path.isfile(self.__infoFilePath) != True) or (os.stat(self.__infoFilePath).st_size == 0):
			self.__infoFileCreation()
			return 1
		return 0

	# Creates standart infofile, that consists of "-1\n".
	def __infoFileCreation(self):
		if not os.path.exists(os.path.join(sublime.packages_path(), "Pem")):
			os.makedirs(os.path.join(sublime.packages_path(), "Pem"))
		infoFile = open(self.__infoFilePath, 'w')
		infoFile.write("-1\n")
		infoFile.close()

	# Checks if a project is selected in infofile.
	def projectSelection(self):
		infoFile = open(self.__infoFilePath, 'r')
		line = infoFile.readline()
		infoFile.close()
		return not ((len(line.split()) == 3) and (line.split()[0].isdigit()) and (int(line.split()[0]) > 0))

	# Checks if a projectfile existes in given directory by given name. Goes correctly if no PF existes.
	def projectFileExistence(self, projectName, projectDir):
		projectPath = os.path.join(projectDir, projectName + extension)
		if os.path.isfile(projectPath):
			return os.stat(projectPath).st_size == 0
		return not (os.path.isfile(projectPath))

	# Checks project-file for correctness. It is correct, if there is "project_name = ", "specification" and "source" lines in it.
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

	# Standart check for selected file existence. Goes correctly if file does exist.
	def fileExistence(self, fileName, filePath):
		return os.path.isfile(os.path.join(filePath, fileName))

	# Check for infofile correctness. Does not check all the infofile.
	# Checks first line for correctness and file till the current selected project.
	def infoFileCorrectnessLite(self):
		infoFile = open(self.__infoFilePath, 'r')
		lines = infoFile.readlines()
		line = lines[0].split()
		infoFile.close()
		if len(line) == 1:
			return str(lines[0]) != "-1\n"
		elif len(line) == 3:
			if str(line[0]).isdigit():
				n = int(line[0])
				for i in range(1, n):
					if len(lines[i].split()) != 2:
						return 3
				return 0
			return 2
		return 4

	# Checks infofile for correctness. Runs previous test. Then checks all the project contained.
	# Checks lines for correctness, then checks, that project are not a myth.
	def infoFileCorrectnessHard(self):
		infoFile = open(self.__infoFilePath, 'r')
		lines = infoFile.readlines()
		infoFile.close()
		linesWithFails = []
		projectsThatDoesNotExist = []
		if (self.infoFileCorrectnessLite()):
			return self.infoFileCorrectnessLite()
		for i in range(1, len(lines)):
			if len(lines[i].split()) != 2 and lines[i]:
				linesWithFails.append(i)
			else:
				if self.projectFileExistence(lines[i].split()[0], lines[i].split()[1]):
					projectsThatDoesNotExist.append(i)
		if (len(linesWithFails)):
			return 5
		if (len(projectsThatDoesNotExist)):
			return 6
		
