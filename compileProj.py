import sublime, sublime_plugin, os
import subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "Pem", "Staff", "correctnessTests.py")).load_module()
rw = SourceFileLoader("ReaderWriter", os.path.join(sublime.packages_path(), "Pem", "Staff", "readerWriter.py")).load_module()

csextension = ".cs"

# Compiles project into chosen target (.exe, .dll, .winexe, .netmodule)
# Creates makefile, then executes it, then deletes it. Console output is printed.
# You can see the list of checks in code.
class CompileProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, target = 0):
		target = int(target)
		targetExtension = target
		if target == 0:
			target = "exe"
			targetExtension = ".exe"
		elif target == 1:
			target = "library"
			targetExtension = ".dll"
		elif target == 2:
			target = "winexe"
			targetExtension = ".winexe"
		elif target == 3:
			target = "module"
			targetExtension = ".netmodule"
		else:
			print("Wrong target input.")
			return 0

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

		projectReader = rw.ProjectReader()
		makefile = open(os.path.join(info.getCurrentProjectPath(), "Makefile"), 'w')
		makefile.write("all:\n")
		makefile.write("\tcd " + "\ ".join(info.getCurrentProjectPath().split()) + '\n')
		makefile.write("\t/usr/local/bin/mcs")
		for file in projectReader.getSource():
			makefile.write(" ./" + "\ ".join(file.split()) + csextension)
		makefile.write(" -target:" + target + " -out:" + info.getCurrentProject() + targetExtension + "\n")
		makefile.write('\n')
		makefile.close()
		makeProcess = subprocess.Popen(["make", "-C", info.getCurrentProjectPath()], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
		if makeProcess.wait():
			print("Error occured. Following text has come as a error message.")
			for line in makeProcess.stderr:
				print(line)
		print("\nConsole output:")
		for line in makeProcess.stdout:
			print(line.strip())
		os.remove(os.path.join(info.getCurrentProjectPath(), "Makefile"))




