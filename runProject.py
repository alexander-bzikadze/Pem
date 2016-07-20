import sublime, sublime_plugin, os
import subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "Pem", "Staff", "correctnessTests.py")).load_module()
rw = SourceFileLoader("ReaderWriter", os.path.join(sublime.packages_path(), "Pem", "Staff", "readerWriter.py")).load_module()

# Runs project exe, if found. Creates a makefile, then runs it, then deletes it. Console output is printed.
# You can see the list of checks in code.
class RunProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		info = rw.InfoReader()
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()
		printBuf = ["Command result (might be empty):"]

		if cT.projectSelection():
			sublime.error_message("Project is not selected.")
			return 0
		if cT.projectFileExistence(info.getCurrentProject(), info.getCurrentProjectPath()):
			sublime.error_message("Project file not found or it is empty.")
			return 0
		if cT.projectFileCorrectness(info.getCurrentProject(), info.getCurrentProjectPath()):
			sublime.error_message("Project file is not correct.")
			return 0
		if not cT.fileExistence(info.getCurrentProject() + ".exe", info.getCurrentProjectPath()):
			sublime.error_message("No .exe to run.")
			return 0

		makefile = open(os.path.join(info.getCurrentProjectPath(), "Makefile"), 'w')
		makefile.write("all:\n")
		makefile.write("\t/usr/local/bin/mono " + info.getCurrentProject() + ".exe <input.txt")
		makefile.close()
		makeProcess = subprocess.Popen(["make", "-C", info.getCurrentProjectPath()], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
		if makeProcess.wait():
			printBuf.append("Error occured. Following text has come as a error message.")
			for line in makeProcess.stderr:
				printBuf.append(line.strip())
		printBuf.append("\nConsole output:")
		for line in makeProcess.stdout:
			printBuf.append(line.strip())
		os.remove(os.path.join(info.getCurrentProjectPath(), "Makefile"))
		sublime.message_dialog("\n".join([str(i) for i in printBuf]))


		