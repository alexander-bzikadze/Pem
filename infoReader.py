#!/usr/bin/python

import os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()

class InfoReader:
	__infoFileName = "Info.txt"
	__infoFilePath = " "
	__currecntProject = " "
	__currecntProjectPath = " "
	__projects = []
	__projectPaths = []

	def __init__(self):
		self.__infoFilePath = os.path.join(sublime.packages_path(), "User", "Pem", self.__infoFileName)
		cT = ct.CorrectnessTests(infoFilePath)
		cT.infoFileExistence()

		infoFile = open(infoFilePath, 'r')
		lines = infoFile.readlines()
		infoFile.close()

		self.__currecntProject = line[0].split()[1]
		self.__currecntProjectPath = line[0].split()[2]
		self.__projects = [line.split()[1] for line in lines]
		self.__projectPaths = [line.split()[2] for line in lines]

	def getCurrecntProject(self):
		return self.__currecntProject

	def getCurrentProjectPath(self):
		return self.__currecntProjectPath

	def getProjects(self):
		return self.__projects

	def getProjectPaths(self):
		return self.__projectPaths

