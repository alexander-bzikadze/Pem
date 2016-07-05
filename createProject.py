import sublime, sublime_plugin, os

class CreateProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, name, path = os.getcwd()):
		infoFileName = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")
		if not os.path.isfile(infoFileName):
			self.infoFileCreation(infoFileName)

		if os.path.isfile(os.path.join(path, name) + ".pem"):
			print("Project path is already busy.")
			return 0

		# projectFile = open(os.path.join(path, name) + ".pem", 'w')
		# projectFile.write("project_name = " + name + '\n\n')
		# projectFile.write("specification:" + "\n\n")
		# projectFile.write("source:" + "\n\n")
		# projectFile.close();

		self.addProjectToInfoFile(infoFileName, name, path)

	def addProjectToInfoFile(self, infoFileName, name, path):
		file = open(infoFileName, "r+")
		lines = file.readlines()
		print(lines)
		lines[0] = len(lines)
		lines += name + " " + path
		file.writelines(lines)
		file.close()

	def infoFileCreation(self, infoFileName):
		open(infoFileName, 'w').write("-1").close()
