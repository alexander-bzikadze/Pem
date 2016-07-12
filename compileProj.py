import sublime, sublime_plugin, os
import subprocess, sys

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
ir = SourceFileLoader("InfoReader", os.path.join(sublime.packages_path(), "User", "infoReader.py")).load_module()
pr = SourceFileLoader("ProjectReader", os.path.join(sublime.packages_path(), "User", "projectReader.py")).load_module()

csextension = ".cs"

class CompileProjectCommand(sublime_plugin.TextCommand):
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

		projectReader = pr.ProjectReader()
		makefile = open(os.path.join(info.getCurrentProjectPath(), "Makefile"), 'w')
		makefile.write("all:\n")
		makefile.write("\tcd " + info.getCurrentProjectPath() + '\n')
		makefile.write("\tmcs")
		for file in projectReader.getSource():
			makefile.write(" " + file + csextension)
		makefile.write(" -target:exe -out:" + info.getCurrentProject() + ".exe\n")
		makefile.write('\n')
		makefile.close()
		make_process = subprocess.Popen(["make", "-C", info.getCurrentProjectPath()], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
		print(make_process.communicate())
		os.remove(os.path.join(info.getCurrentProjectPath(), "Makefile"))


		