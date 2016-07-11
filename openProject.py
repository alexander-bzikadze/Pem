import sublime, sublime_plugin, os, subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
ir = SourceFileLoader("InfoReader", os.path.join(sublime.packages_path(), "User", "infoReader.py")).load_module()

extension = ".pem"
csextension = ".cs"

class OpenProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
		info = ir.InfoReader()
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()
		self.view.run_command("switch_project", {"name" : name})

		if cT.projectSelection():
			# print("Project is not selected.")
			return 0
		if not name == info.getCurrentProject():
			print ("No such project.")
			return 0
		if cT.projectFileExistence(info.getCurrentProject(), info.getCurrentProjectPath()):
			print("Project file not found or it is empty.")
			return 0

		projectPath = os.path.join(info.getCurrentProjectPath(), info.getCurrentProject() + extension)
		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		self.view.window().open_file(projectPath, sublime.ENCODED_POSITION)
		for i in range(lines.index("source:\n") + 1, len(lines)):
			self.view.run_command("open_file", {"name" : lines[i][1: len(lines[i]) - 1]})
		projectFile.close()