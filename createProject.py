import sublime, sublime_plugin, os

class CreateProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, name, path = os.path.expanduser('~/')):
		infoFileName = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")
		if (os.path.isfile(infoFileName) != True) or (os.stat(infoFileName).st_size == 0):
			self.infoFileCreation(infoFileName)

		if os.path.isfile(os.path.join(path, name) + ".pem"):
			print("Project path is already busy.")
			return 0

		projectFile = open(os.path.join(path, name) + ".pem", 'w')
		projectFile.write("project_name = " + name + '\n\n')
		projectFile.write("specification:" + "\n\n")
		projectFile.write("source:" + "\n\n")
		projectFile.close();

		self.addProjectToInfoFile(infoFileName, name, path)

	def addProjectToInfoFile(self, infoFileName, name, path):
		file = open(infoFileName, "r")
		lines = file.readlines()
		file.close()

		lines[0] = str(len(lines)) + " " + str(name + " " + path) + "\n"
		lines.append(str(name + " " + path) + "\n")

		file = open(infoFileName, "w")
		file.writelines(lines)
		file.close()

	def infoFileCreation(self, infoFileName):
		file = open(infoFileName, 'w')
		file.write("-1")
		file.close()