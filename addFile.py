import sublime, sublime_plugin, os
import subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "Pem", "Staff", "correctnessTests.py")).load_module()
rw = SourceFileLoader("ReaderWriter", os.path.join(sublime.packages_path(), "Pem", "Staff", "readerWriter.py")).load_module()

csextension = ".cs"

# Adds file to the current project. In the code you can see a list of checks.
class AddFileCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
		info = rw.InfoReader()
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()

		if cT.projectSelection():
			sublime.error_message("Project is not selected.")
			return 0
		if cT.projectFileExistence(info.getCurrentProject(), info.getCurrentProjectPath()):
			sublime.error_message("Project file not found or it is empty.")
			return 0
		if cT.projectFileCorrectness(info.getCurrentProject(), info.getCurrentProjectPath()):
			sublime.error_message("Project file is not correct.")
			return 0
		if cT.fileExistence(name + csextension, info.getCurrentProjectPath()):
			sublime.error_message("File already exists.")
			return 0
		projectWriter = rw.ProjectWriter()
		if projectWriter.addFile(name):
			sublime.error_message("File is already in the project.")
			return 0
			
		filePath = os.path.join(os.path.expanduser('~'), info.getCurrentProjectPath(), name + csextension)
		if not os.path.exists(os.path.dirname(filePath)):
			os.makedirs(os.path.dirname(filePath))
		file = open(filePath, 'w')
		namespace = info.getCurrentProject()
		file.write("using System;\nusing System.Collections.Generic;\n")
		file.write("\n\n")
		file.write("namespace " + namespace + "\n{\n\tpublic class " + os.path.basename(filePath[0:len(filePath) - 3]) + "\n\t{\n\t\t\n\t}\n}")
		file.close()