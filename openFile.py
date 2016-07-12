import sublime, sublime_plugin, os, subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
ir = SourceFileLoader("InfoReader", os.path.join(sublime.packages_path(), "User", "infoReader.py")).load_module()
pr = SourceFileLoader("ProjectReader", os.path.join(sublime.packages_path(), "User", "projectReader.py")).load_module()

extension = ".pem"
csextension = ".cs"

class OpenFileCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
		info = ir.InfoReader()
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()

		if cT.projectSelection():
			print("Project is not selected.")
			return 0
		if cT.projectFileExistence(info.getCurrentProject(), info.getCurrentProjectPath()):
			print("Project file not found or it is empty.")
			return 0

		projectReader = pr.ProjectReader()
		if name in projectReader.getSource():
			self.view.window().open_file(os.path.join(info.getCurrentProjectPath(), name + csextension), sublime.ENCODED_POSITION)
		else:
			print("Project does not contain such a file.")