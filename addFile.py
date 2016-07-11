import sublime, sublime_plugin, os
import subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
ir = SourceFileLoader("InfoReader", os.path.join(sublime.packages_path(), "User", "infoReader.py")).load_module()

extension = ".pem"
csextension = ".cs"
project_name = "project_name = "
source = "source:"
specification = "specification:"

class AddFileCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
		info = ir.InfoReader()
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()

		if cT.projectFileExistence(info.getCurrentProject(), info.getCurrentProjectPath()):
			print("Project file not found or it is empty.")
			return 0

		if cT.projectFileCorrectness(info.getCurrentProject(), info.getCurrentProjectPath()):
			print("Project file is not correct.")
			return 0

		if cT.fileExistence(name + csextension, info.getCurrentProjectPath()):
			print("File already exists.")
			return 0

		filePath = os.path.join(info.getCurrentProjectPath(), name + csextension)
		file = open(filePath, 'w')
		namespace = info.getCurrentProject()
		file.write("using System;\nusing System.Collections.Generic;\n")
		file.write("\n\n")
		file.write("namespace " + namespace + "\n{\n\tpublic class " + "".join(name) + "\n\t{\n\t\t\n\t}\n}")
		file.close()

		projectPath = os.path.join(info.getCurrentProjectPath(), info.getCurrentProject() + extension)
		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		projectFile.close()
		lines.append('\t' + name + '\n')
		projectFile = open(projectPath, 'w')
		projectFile.writelines(lines)
		projectFile.close()
		return 0