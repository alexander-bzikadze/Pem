import sublime, sublime_plugin, os
import subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()

extension = ".pem"
csextension = ".cs"
project_name = "project_name = "
source = "source:"
specification = "specification:"

class AddFileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		infoFilePath = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")
		cT = ct.CorrectnessTests(infoFilePath)
		cT.infoFileExistence()

		infoFile = open(infoFilePath, 'r')
		line = infoFile.readline()
		infoFile.close()

		if cT.projectSelection():
			print("Project is not selected.")
			return 0

		if cT.projectFileExistence(line):
			print("Project file not found or it is empty.")
			return 0

		if cT.projectFileCorrectness(line):
			print("Project file is not correct.")
			return 0

		projectName = line.split()[1]