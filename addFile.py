import sublime, sublime_plugin, os
import subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "Pem", "Staff", "correctnessTests.py")).load_module()
rw = SourceFileLoader("ReaderWriter", os.path.join(sublime.packages_path(), "Pem", "Staff", "readerWriter.py")).load_module()

csextension = ".cs"

class AddFileCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
		info = rw.InfoReader()
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()

		if cT.projectSelection():
			print("Project is not selected.")
			return 0
		if cT.projectFileExistence(info.getCurrentProject(), info.getCurrentProjectPath()):
			print("Project file not found or it is empty.")
			return 0
		if cT.projectFileCorrectness(info.getCurrentProject(), info.getCurrentProjectPath()):
			print("Project file is not correct.")
			return 0
		if cT.fileExistence(name + csextension, info.getCurrentProjectPath()):
			print("File already exists.")
			return 0

		projectWriter = rw.ProjectWriter()
		if projectWriter.addFile(name):
			print("File is already in the project.")
			return 0

		filePath = os.path.join(info.getCurrentProjectPath(), name + csextension)
		file = open(filePath, 'w')
		namespace = info.getCurrentProject()
		file.write("using System;\nusing System.Collections.Generic;\n")
		file.write("\n\n")
		file.write("namespace " + namespace + "\n{\n\tpublic class " + "".join(name) + "\n\t{\n\t\t\n\t}\n}")
		file.close()
		return 0