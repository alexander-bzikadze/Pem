#!/usr/bin/python

import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
ir = SourceFileLoader("InfoReader", os.path.join(sublime.packages_path(), "User", "infoReader.py")).load_module()

extension = ".pem"

class ProjectReader:
	__projectName = ""
	__projectPath = ""
	__specification = []
	__source = []

	def __init__(self):
		info = ir.InfoReader()
		cT = ct.CorrectnessTests()
		projectPath = os.path.join(info.getCurrentProjectPath(), info.getCurrentProject() + extension)

		if cT.projectFileExistence(info.getCurrentProject(), info.getCurrentProjectPath()):
			print("Unable to load project file. It is not found.")
			return 0

		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		self.__projectName = info.getCurrentProject()
		self.__projectPath = info.getCurrentProjectPath()
		self.__specification = [lines[i][1:len(lines[i]) - 1] for i in range(lines.index("specification:\n") + 1, lines.index("source:\n") - 1) if i]
		self.__source = [lines[i][1:len(lines[i]) - 1] for i in range(lines.index("source:\n") + 1, len(lines)) if i]
		projectFile.close()


	def getProjectName(self):
		return self.__projectName

	def getProjectPath(self):
		return self.__projectPath

	def getSpecification(self):
		return self.__specification

	def getSource(self):
		return self.__source