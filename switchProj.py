import sublime, sublime_plugin, os

class SwitchProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
		infoFileName = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")
		file = open(infoFileName, 'r')
		lines = file.readlines()
		pos = 0
		if (os.path.isfile(infoFileName) == True):
			projectNames = [i.split()[0] for i in lines]
			projectNames.pop(0)
			if name in projectNames:
				pos = projectNames.index(name)
			else:
				print("Project not found.")
		else:
			print("Info-file not found.")

		lines[0] = str(pos + 1) + "\n"
		file.close()

		file = open(infoFileName, 'w')
		file.writelines(lines)
		file.close()
