import sublime, sublime_plugin, os

class CreateProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, name, path = os.getcwd()):
		infoFileName = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")
		if not os.path.isfile(infoFileName):
			self.infoFileCreation(infoFileName)

		projectFile = open(os.path.join(path, name) + ".pem", 'w')
		projectFile.write("project_name = " + name + '\n\n')
		projectFile.write("specification:" + "\n\n")
		projectFile.write("source:" + "\n\n")
		projectFile.close();



	def infoFileCreation(self, infoFileName):
		open(infoFileName, 'w').write("-1")
