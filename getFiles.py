import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()

extension = ".pem"

class GetFilesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		infoFilePath = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")
		cT = ct.CorrectnessTests(infoFilePath)
		cT.infoFileExistence()

		infoFile = open(infoFilePath, 'r')
		line = infoFile.readline()
		infoFile.close()

		if cT.projectSelection():
			print("Project is not selected.")
			return 0
		if cT.projectFileExistence(line):
			print("Project file not found or it is empty.")
			return 0
		if cT.projectFileCorrectness(line):
			print("Project file is not correst.")
			return 0

		projectName = line.split()[1]
		projectPath = os.path.join(line.split()[2], projectName + extension)
		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		projectFile.close()
		for i in range(lines.index("source:\n") + 1, len(lines)):
			print(lines[i][0 : len(lines[i]) - 1])