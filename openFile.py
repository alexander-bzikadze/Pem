import sublime, sublime_plugin, os, subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "Pem", "Staff", "correctnessTests.py")).load_module()
rw = SourceFileLoader("ReaderWriter", os.path.join(sublime.packages_path(), "Pem", "Staff", "readerWriter.py")).load_module()

extension = ".pem"
csextension = ".cs"

class OpenFileCommand(sublime_plugin.TextCommand):
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
		if not cT.fileExistence(name + csextension, info.getCurrentProjectPath()):
			print("File to be opened not found.")
			return 0

		projectReader = rw.ProjectReader()
		if name in projectReader.getSource():
			self.view.window().open_file(os.path.join(info.getCurrentProjectPath(), name + csextension), sublime.ENCODED_POSITION)
		else:
			print("Project does not contain such a file.")