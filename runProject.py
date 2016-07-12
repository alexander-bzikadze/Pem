import sublime, sublime_plugin, os
import subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
ir = SourceFileLoader("InfoReader", os.path.join(sublime.packages_path(), "User", "infoReader.py")).load_module()
pr = SourceFileLoader("ProjectReader", os.path.join(sublime.packages_path(), "User", "projectReader.py")).load_module()

class RunProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		info = ir.InfoReader()
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
		if not cT.fileExistence(info.getCurrentProject() + ".exe", info.getCurrentProjectPath()):
			print("No .exe to run.")
			return 0

		projectReader = pr.ProjectReader()
		makefile = open(os.path.join(info.getCurrentProjectPath(), "Makefile"), 'w')
		makefile.write("all:\n")
		makefile.write("\tmono " + os.path.join(info.getCurrentProjectPath(), info.getCurrentProject() + ".exe"))
		makefile.close()
		makeProcess = subprocess.Popen(["make", "-C", info.getCurrentProjectPath()], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
		print(makeProcess.communicate())
		os.remove(os.path.join(info.getCurrentProjectPath(), "Makefile"))


		