import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
ir = SourceFileLoader("InfoReader", os.path.join(sublime.packages_path(), "User", "infoReader.py")).load_module()

class CreateProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, name, path = os.path.expanduser('~/')):
		infoFilePath = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")
		cT = ct.CorrectnessTests(infoFilePath)
		cT.infoFileExistence()

		if cT.fileExistence(os.path.join(path, name) + ".pem"):
			print("Project path is already busy.")
			return 0

		projectFile = open(os.path.join(path, name) + ".pem", 'w')
		projectFile.write("project_name = " + name + '\n\n')
		projectFile.write("specification:" + "\n\n")
		projectFile.write("source:" + "\n\n")
		projectFile.close();

		self.addProjectToInfoFile(infoFilePath, name, path)

	def addProjectToInfoFile(self, infoFilePath, name, path):
		file = open(infoFilePath, "r")
		lines = file.readlines()
		file.close()

		lines[0] = str(len(lines)) + " " + str(name + " " + path) + "\n"
		lines.append(str(name + " " + path) + "\n")

		file = open(infoFilePath, "w")
		file.writelines(lines)
		file.close()