import sublime, sublime_plugin, os, subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()

extension = ".pem"
csextension = ".cs"

class DeleteFileCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
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

		projectName = line.split()[1]
		projectPath = os.path.join(line.split()[2], projectName + extension)
		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		projectFile.close()
		if ('\t' + name + '\n' in lines) and (lines.index("source:\n") < lines.index('\t' + name + '\n')):
			os.remove(os.path.join(line.split()[2], name + csextension))
			lines.remove('\t' + name + '\n')
			projectFile = open(projectPath, 'w')
			projectFile.writelines(lines)
			projectFile.close()
		else:
			print("Project does not contain such a file.")