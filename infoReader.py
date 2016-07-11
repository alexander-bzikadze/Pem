#!/usr/bin/python

import os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
Exceptions = SourceFileLoader("Exceptions", os.path.join(sublime.packages_path(), "User", "projectNotSelectedException.py")).load_module()

class InfoReader:
	__infoFileName = "Info.txt"
	__infoFilePath = ""
	__currentProject = ""
	__currentProjectPath = ""
	__projects = []
	__projectPaths = []

	def __init__(self):
		self.__infoFilePath = os.path.join(sublime.packages_path(), "User", "Pem", self.__infoFileName)
		cT = ct.CorrectnessTests(self.__infoFilePath)
		cT.infoFileExistence()

		infoFile = open(self.__infoFilePath, 'r')
		lines = infoFile.readlines()
		infoFile.close()

		if len(lines[0].split()) != 1:
			self.__currentProject = lines[0].split()[1]
			self.__currentProjectPath = lines[0].split()[2]
		lines.pop(0)
		self.__projects = [line.split()[0] for line in lines]
		self.__projectPaths = [line.split()[1] for line in lines]

	def getCurrentProject(self):
		if not self.__currentProject:
			print(self.__currentProject)
			raise Exceptions.ProjectNotSelectedException("No project selected.")
		return self.__currentProject

	def getCurrentProjectPath(self):
		if not self.__currentProjectPath:
			raise Exceptions.ProjectNotSelectedException("No project selected.")
		return self.__currentProjectPath

	def getProjects(self):
		return self.__projects

	def getProjectPaths(self):
		return self.__projectPaths

