import sublime, sublime_plugin, os

extension = ".pem"

class GetFilesCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		infoFileName = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")

		if (os.path.isfile(infoFileName) != True) or (os.stat(infoFileName).st_size == 0):
			self.infoFileCreation(infoFileName)

		infoFileName = os.path.join(infoFileName)
		if not os.path.isfile(infoFileName):
			print("Info-file not found.")
			return 0
		if os.stat(infoFileName).st_size == 0:
			print("Info-file is empty.")
			return 0
		infoFile = open(infoFileName, 'r')
		line = infoFile.readline()
		infoFile.close()
		if (len(line.split()) != 3) or (not line.split()[0].isdigit()) or (line.split()[0] == "-1"):
			print("Project is not selected.")
			return 0
		projectName = line.split()[1]
		projectPath = os.path.join(line.split()[2], projectName + extension)
		if not (os.path.isfile(projectPath) or os.stat(projectPath).st_size == 0):
			print("Project file not found or it is empty.")
			return 0

		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		for i in range(lines.index("source:\n") + 1, len(lines)):
			print(lines[i][0 : len(lines[i]) - 1])
		projectFile.close()


	def infoFileCreation(self, infoFileName):
		file = open(infoFileName, 'w')
		file.write("-1")
		file.close()