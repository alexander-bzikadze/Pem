import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "Pem", "Staff", "correctnessTests.py")).load_module()
rw = SourceFileLoader("ReaderWriter", os.path.join(sublime.packages_path(), "Pem", "Staff", "readerWriter.py")).load_module()

extension = ".pem"

# Prints list of all the files, connected to the selected project.
# You can see the list of checks in code.
class GetFilesCommand(sublime_plugin.TextCommand):
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

		projectReader = rw.ProjectReader()
		for file in projectReader.getSource():
			printBuf.append(file)
		sublime.message_dialog("\n".join([str(i) for i in printBuf]))