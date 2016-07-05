import sublime, sublime_plugin, os

class GetAllProjCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		infoFileName = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")
		file = open(infoFileName, 'r')
		if (os.path.isfile(infoFileName) == True):
			for line in file.readlines():
				if len(line.split()) == 2:
					print(line.split()[0])