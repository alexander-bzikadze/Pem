import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()

class SwitchProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
		infoFilePath = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")
		cT = ct.CorrectnessTests(infoFilePath)
		cT.infoFileExistence()

		file = open(infoFilePath, 'r')
		lines = file.readlines()
		file.close()
		pos = 0
		projectNames = [i.split()[0] for i in lines]
		projectNames.pop(0)
		if name in projectNames:
			pos = projectNames.index(name)
		else:
			print("Project not found.")
			return 0
		lines[0] = str(pos + 1) + " " + lines[pos + 1]

		file = open(infoFilePath, 'w')
		file.writelines(lines)
		file.close()

