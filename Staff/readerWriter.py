#!/usr/bin/python

import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "Pem", "Staff", "correctnessTests.py")).load_module()
Exceptions = SourceFileLoader("Exceptions", os.path.join(sublime.packages_path(), "Pem", "Staff", "exceptions.py")).load_module()

extension = ".pem"
csextension = ".cs"

# This file contains classes to interact with infofile and projectfiles. Any other interaction is not allowed, except projectfile creation.

# Allows to read infofile: get current project info, info of all the project and number of needed project.
class InfoReader:
	__infoFileName = "Info.txt"
	__infoFilePath = ""
	__currentProject = ""
	__currentProjectPath = ""
	__projects = []
	__projectPaths = []

	# Constructor finds infofile and reades information from it.
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

	# Returns name of the project selected at the moment. It is the same project as the one in the first line of the infofile.
	# Throws ProjectNotSelectedException, if project not selected. 
	def getCurrentProject(self):
		if not self.__currentProject:
			raise Exceptions.ProjectNotSelectedException("No project selected.")
		return self.__currentProject

	# Returns path to the selected project.
	# Throws ProjectNotSelectedException, if project not selected. 
	def getCurrentProjectPath(self):
		if not self.__currentProjectPath:
			raise Exceptions.ProjectNotSelectedException("No project selected.")
		return self.__currentProjectPath

	# Returns list of all the project, that infofile knows about.
	def getProjects(self):
		return self.__projects

	# Returns list of all paths to to the projects. Has tha same numeration as self.getProjects.
	def getProjectPaths(self):
		return self.__projectPaths

	# Returns number of given project. If there is no such project, throws ProjectAbsenceInInfofile.
	# Attention! The returned number does not match with the line number in infofile, that contains the project info.
	# The returned number + 1 = the line number.
	def getProjectNumber(self, name):
		try:
			return self.__projects.index(name)
		except ValueError:
			raise Exceptions.ProjectAbsenceInInfofile("No such project.")

# Allows to write in infofile: add project or delete one.
class InfoWriter:
	# Adds project to infofile. If a project with the same name is already contained by infofile, returns 1 and does nothing. 
	# Otherwise returns 0.
	# Attention! Does not run tests for correcness of given project!
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

	# Deletes project by number. If number does not lay in range(0, projects number), return 1 and does nothing.
	# Otherwise returns 0.
	# Attention! Numeration does not match with the line numeration, but with InfoReader.getProject() numeration.
	def deleteProject(self, number):
		info = InfoReader()
		infoFilePath = os.path.join(sublime.packages_path(), "Pem", "Info.txt")
		file = open(infoFilePath, "r")
		lines = file.readlines()
		file.close()

		if number < len(lines) - 1 and number >= 0:
			lines.pop(number + 1)
			if lines[0] != "-1\n":
				if info.getCurrentProject() != info.getProjects()[number]:
					number = lines.index(" ".join([info.getCurrentProject(), "\\:".join(info.getCurrentProjectPath().split()), '\n']))
					lines[0] = " ".join([number, info.getCurrentProject(), "\\:".join(info.getCurrentProjectPath().split()), '\n'])
				else:
					lines[0] = "-1\n"	
			file = open(infoFilePath, "w")
			file.writelines(lines)
			file.close()
			return 0
		return 1

	# Switches project to given number. If number does not lay in range(0, projects number), return 1 and does nothing.
	# Allows to switch to no project, if given number is -1.
	# Attention! Numeration does not match with the line numeration, but with InfoReader.getProject() numeration.
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

# Class that allows to read selected projectfile: get its name, path, specification list and source list.
class ProjectReader:
	__projectName = ""
	__projectPath = ""
	__specification = []
	__source = []

	# Constructor gets project info from InfoReader, then finds projectfile and reads it.
	# Can fall with ProjectNotSelectedException, that will come from InfoReader, if no project selected.
	# Can fall with ProjectFileDoesNotExistException, if projectfile will not be found.
	# Can fall with ProjectFileNotCorrect, if projectfile is not correct.
	def __init__(self):
		info = InfoReader()
		cT = ct.CorrectnessTests()
		projectPath = os.path.join(info.getCurrentProjectPath(), info.getCurrentProject() + extension)

		if cT.projectFileExistence(info.getCurrentProject(), info.getCurrentProjectPath()):
			raise Exceptions.ProjectFileDoesNotExistException("Projectfile not found.")

		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		self.__projectName = info.getCurrentProject()
		self.__projectPath = info.getCurrentProjectPath()

		if cT.projectFileCorrectness(info.getCurrentProject(), info.getCurrentProjectPath()):
			raise Exceptions.ProjectFileNotCorrect("Projectfile is incorrect.")

		self.__specification = [" ".join(lines[i][1:len(lines[i]) - 1].split("\\:")) for i in range(lines.index("specification:\n") + 1, lines.index("source:\n") - 1) if i]
		self.__source = [" ".join(lines[i][1:len(lines[i]) - 1].split("\\:")) for i in range(lines.index("source:\n") + 1, len(lines)) if i]
		projectFile.close()

	# Returns name of the project.
	def getProjectName(self):
		if not self.__projectName:
			raise Exceptions.ProjectNotSelectedException("No project selected.")
		return self.__projectName

	# Returns path to the project.
	def getProjectPath(self):
		if not self.__projectPath:
			raise Exceptions.ProjectNotSelectedException("No project selected.")
		return self.__projectPath

	# Returns list of specifications.
	def getSpecification(self):
		return self.__specification

	# Returns list of sources.
	def getSource(self):
		return self.__source

# Class that allows to write to projectfile: eighter add file or delete one.
class ProjectWriter:
	# If file is not in source list, addes it and returns 0. Otherwise 1.
	# Can fall with ProjectReader exceptions, as creates it.
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

	# If file is in source list, deletes it and return 0. Otherwise 1.
	# Can fall with ProjectReader exceptions, as creates it.
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
