import sublime, sublime_plugin, os, subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()

extension = ".pem"
csextension = ".cs"

class DeleteProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
		infoFilePath = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")
		cT = ct.CorrectnessTests(infoFilePath)
		cT.infoFileExistence()

		self.view.run_command("switch_project", {"name" : name})

		infoFile = open(infoFilePath, 'r')
		line = infoFile.readline()
		infoFile.close()

		if not name in line:
			print ("No such project.")
			return 0
		if cT.projectSelection():
			print("Project is not selected.")
			return 0
		if cT.projectFileExistence(line):
			print("Project file not found or it is empty.")
			return 0

		projectName = line.split()[1]
		projectPath = os.path.join(line.split()[2], projectName + extension)
		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		projectFile.close()
		for i in range(lines.index("source:\n") + 1, len(lines)):
			self.view.run_command("delete_file", {"name" : lines[i][1: len(lines[i]) - 1]})
		os.remove(projectPath)
		infoFile = open(infoFilePath, 'r')
		infoLines = infoFile.readlines()
		infoFile.close()

		n = int(infoLines[0].split()[0])
		infoLines.pop(n)
		infoLines[0] = str(-1) + '\n'

		infoFile = open(infoFilePath, 'w')
		infoFile.writelines(infoLines)
		infoFile.close()