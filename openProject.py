import sublime, sublime_plugin, os, subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "Pem", "Staff", "correctnessTests.py")).load_module()
rw = SourceFileLoader("ReaderWriter", os.path.join(sublime.packages_path(), "Pem", "Staff", "readerWriter.py")).load_module()

extension = ".pem"
csextension = ".cs"

# Opens all files, connected to the current project.
# You can see the list of checks in code.
# Uses switch_project and delete_file commands.
class OpenProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
		if name == "-1":
			print("Cannot open nothing.")
			return 0
		self.view.run_command("switch_project", {"name" : name})
		info = rw.InfoReader()
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()

		if cT.projectSelection():
			# print("Project is not selected.")
			return 0
		if not name == info.getCurrentProject():
			# print ("No such project.")
			return 0
		if cT.projectFileExistence(info.getCurrentProject(), info.getCurrentProjectPath()):
			print("Project file not found or it is empty.")
			return 0

		projectReader = rw.ProjectReader()
		for file in projectReader.getSource():
			self.view.run_command("open_file", {"name" : file})