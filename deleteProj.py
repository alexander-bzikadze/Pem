import sublime, sublime_plugin, os, subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
ir = SourceFileLoader("InfoReader", os.path.join(sublime.packages_path(), "User", "infoReader.py")).load_module()

extension = ".pem"
csextension = ".cs"

class DeleteProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
		self.view.run_command("switch_project", {"name" : name})
		info = ir.InfoReader()
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()

		if cT.projectSelection():
			# print("Project is not selected." #As it means, that project has not been found.
			return 0
		if name != info.getCurrentProject():
			print ("No such project.")
			return 0
		if cT.projectFileExistence(info.getCurrentProject(), info.getCurrentProjectPath()):
			print("Project file not found or it is empty.")
			return 0

		projectPath = os.path.join(info.getCurrentProjectPath(), info.getCurrentProject() + extension)
		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		projectFile.close()
		for i in range(lines.index("source:\n") + 1, len(lines)):
			if lines[i] != '\n':
				self.view.run_command("delete_file", {"name" : lines[i][1: len(lines[i]) - 1]})
		os.remove(projectPath)
		infoFile = open(os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt"), 'r')
		infoLines = infoFile.readlines()
		infoFile.close()

		n = int(infoLines[0].split()[0])
		infoLines.pop(n)
		infoLines[0] = str(-1) + '\n'

		infoFile = open(os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt"), 'w')
		infoFile.writelines(infoLines)
		infoFile.close()