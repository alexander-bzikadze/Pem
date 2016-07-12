#!/usr/bin/python

import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
ir = SourceFileLoader("InfoReader", os.path.join(sublime.packages_path(), "User", "infoReader.py")).load_module()

class InfoWriter:
	__info = ir.InfoReader()

	def addProject(self, name, path):
		infoFilePath = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")
		file = open(infoFilePath, "r")
		lines = file.readlines()
		file.close()

		if not name in self.__info.getProjects():
			lines.append(str(name + " " + path) + "\n")
			file = open(infoFilePath, "w")
			file.writelines(lines)
			file.close()
			self.__info = ir.InfoReader()
			return 0
		return 1

	def deleteProject(self, number):
		infoFilePath = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")
		file = open(infoFilePath, "r")
		lines = file.readlines()
		file.close()

		if number < len(lines) - 1 and number >= 0:
			lines.pop(number + 1)
			file = open(infoFilePath, "w")
			file.writelines(lines)
			file.close()
			self.__info = ir.InfoReader()
			return 0
		return 1

	def switchProject(self, number):
		infoFilePath = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")
		file = open(infoFilePath, "r")
		lines = file.readlines()
		file.close()

		if number < len(lines) - 1 and number >= 0:
			lines[0] = " ".join([str(number + 1), self.__info.getProjects()[number], self.__info.getProjectPaths()[number], '\n'])
			file = open(infoFilePath, "w")
			file.writelines(lines)
			file.close()
			return 0
		elif number == -1:
			lines[0] = "-1\n"
			file = open(infoFilePath, "w")
			file.writelines(lines)
			file.close()
			return 0
		return 1