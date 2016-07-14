#!/usr/bin/python

import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "Pem", "Staff", "correctnessTests.py")).load_module()
Exceptions = SourceFileLoader("Exceptions", os.path.join(sublime.packages_path(), "Pem", "Staff", "exceptions.py")).load_module()

extension = ".pem"
csextension = ".cs"

class InfoReader:
	__infoFileName = "Info.txt"
	__infoFilePath = ""
	__currentProject = ""
	__currentProjectPath = ""
	__projects = []
	__projectPaths = []

	def __init__(self):
		self.__infoFilePath = os.path.join(sublime.packages_path(), "Pem", self.__infoFileName)
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()

		infoFile = open(self.__infoFilePath, 'r')
		lines = infoFile.readlines()
		infoFile.close()

		if len(lines[0].split()) == 3:
			self.__currentProject = lines[0].split()[1]
			self.__currentProjectPath = " ".join(lines[0].split()[2].split("\\:"))
		lines.pop(0)
		self.__projects = [line.split()[0] for line in lines]
		self.__projectPaths = [" ".join(line.split()[1].split("\\:")) for line in lines]

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

	def getProjectNumber(self, name):
		try:
			return self.__projects.index(name)
		except ValueError:
			raise Exceptions.ProjectAbsenceInInfofile("No such project.")


class InfoWriter:
	def addProject(self, name, path):
		info = InfoReader()
		infoFilePath = os.path.join(sublime.packages_path(), "Pem", "Info.txt")
		file = open(infoFilePath, "r")
		lines = file.readlines()
		file.close()

		if not name in info.getProjects():
			lines.append(str(name + " " + "\\:".join(path.split())) + "\n")
			file = open(infoFilePath, "w")
			file.writelines(lines)
			file.close()
			return 0
		return 1

	def deleteProject(self, number):
		info = InfoReader()
		infoFilePath = os.path.join(sublime.packages_path(), "Pem", "Info.txt")
		file = open(infoFilePath, "r")
		lines = file.readlines()
		file.close()

		if number < len(lines) - 1 and number >= 0:
			lines.pop(number + 1)
			file = open(infoFilePath, "w")
			file.writelines(lines)
			file.close()
			return 0
		return 1

	def switchProject(self, number):
		info = InfoReader()
		infoFilePath = os.path.join(sublime.packages_path(), "Pem", "Info.txt")
		file = open(infoFilePath, "r")
		lines = file.readlines()
		file.close()

		if number == -1:
			lines[0] = "-1\n"
			file = open(infoFilePath, "w")
			file.writelines(lines)
			file.close()
			return 0
		elif number < len(lines) - 1 and number >= 0:
			lines[0] = " ".join([str(number + 1), info.getProjects()[number], "\\:".join(info.getProjectPaths()[number].split()), '\n'])
			file = open(infoFilePath, "w")
			file.writelines(lines)
			file.close()
			return 0
		return 1

class ProjectReader:
	__projectName = ""
	__projectPath = ""
	__specification = []
	__source = []

	def __init__(self):
		info = InfoReader()
		cT = ct.CorrectnessTests()
		projectPath = os.path.join(info.getCurrentProjectPath(), info.getCurrentProject() + extension)

		if cT.projectFileExistence(info.getCurrentProject(), info.getCurrentProjectPath()):
			print("Unable to load project file. It is not found.")
			return 0

		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		try:
			self.__projectName = info.getCurrentProject()
			self.__projectPath = info.getCurrentProjectPath()
		except ProjectNotSelectedException:
			self.__projectName = ""
			self.__projectPath = ""

		if cT.projectFileCorrectness(info.getCurrentProject(), info.getCurrentProjectPath()):
			raise Exceptions.ProjectFileNotCorrect("Project file is incorrect.")

		self.__specification = [" ".join(lines[i][1:len(lines[i]) - 1].split("\\:")) for i in range(lines.index("specification:\n") + 1, lines.index("source:\n") - 1) if i]
		self.__source = [" ".join(lines[i][1:len(lines[i]) - 1].split("\\:")) for i in range(lines.index("source:\n") + 1, len(lines)) if i]
		projectFile.close()


	def getProjectName(self):
		if not self.__projectName:
			raise Exceptions.ProjectNotSelectedException("No project selected.")
		return self.__projectName

	def getProjectPath(self):
		if not self.__projectPath:
			raise Exceptions.ProjectNotSelectedException("No project selected.")
		return self.__projectPath

	def getSpecification(self):
		return self.__specification

	def getSource(self):
		return self.__source

class ProjectWriter:
	def addFile(self, name):
		info = InfoReader()
		project = ProjectReader()
		projectPath = os.path.join(info.getCurrentProjectPath(), info.getCurrentProject() + extension)
		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		projectFile.close()

		if not name in project.getSource():
			name = "\\:".join(name.split())
			lines.append('\t' + name + '\n')
			projectFile = open(projectPath, 'w')
			projectFile.writelines(lines)
			projectFile.close()
			project = ProjectReader()
			return 0
		return 1

	def deleteFile(self, name):
		info = InfoReader()
		project = ProjectReader()
		projectPath = os.path.join(info.getCurrentProjectPath(), info.getCurrentProject() + extension)
		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		projectFile.close()
		if name in project.getSource():
			os.remove(os.path.join(info.getCurrentProjectPath(), name + csextension))
			name = "\\:".join(name.split())
			lines.remove('\t' + name + '\n')
			projectFile = open(projectPath, 'w')
			projectFile.writelines(lines)
			projectFile.close()
			return 0
		return 1
