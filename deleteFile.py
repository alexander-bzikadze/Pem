import sublime, sublime_plugin, os, subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
ir = SourceFileLoader("InfoReader", os.path.join(sublime.packages_path(), "User", "infoReader.py")).load_module()
pw = SourceFileLoader("ProjectWriter", os.path.join(sublime.packages_path(), "User", "projectWriter.py")).load_module()

extension = ".pem"
csextension = ".cs"

class DeleteFileCommand(sublime_plugin.TextCommand):
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

		projectWriter = pw.ProjectWriter()
		if projectWriter.deleteFile(name):
			print("No such file", name, "in", info.getCurrentProject(), ".")