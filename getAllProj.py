import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()

class GetAllProjCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		infoFilePath = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")
		cT = ct.CorrectnessTests(infoFilePath)
		cT.infoFileExistence()
		if cT.infoFileCorrectnessHard:
			print("Prepare yourself. Incorrect info-file is coming.")

		infoFile = open(infoFilePath, 'r')
		lines = infoFile.readlines()
		for i in range(1, len(lines)):
			print(lines[i].split()[0])
		infoFile.close()