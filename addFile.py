import sublime, sublime_plugin, os
import subprocess

extension = ".pem"
csextension = ".cs"
project_name = "project_name = "
source = "source:"
specification = "specification:"

class AddFileCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
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
			print (len(line.split()) != 3)
			return 0
		projectName = line.split()[1]
		projectPath = os.path.join(line.split()[2], projectName + extension)
		if not (os.path.isfile(projectPath) or os.stat(projectPath).st_size == 0):
			print("Project file not found or it is empty.")
			return 0
		filePath = os.path.join(line.split()[2], name + csextension)

		if os.path.isfile(filePath):
			print("File already exists.")
			return 0

		file = open(filePath, 'w')
		namespace = projectName

		file.write("using System;\nusing System.Collections.Generic;\n")
		file.write("\n\n")
		file.write("namespace " + namespace + "\n{\n\tpublic class " + "".join(name) + "\n\t{\n\t\t\n\t}\n}")
		file.close()

		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		projectFile.close()
		lines.append('\t' + name + '\n')
		projectFile = open(projectPath, 'w')
		projectFile.writelines(lines)
		projectFile.close()
		return 0


	def infoFileCreation(self, infoFileName):
		file = open(infoFileName, 'w')
		file.write("-1")
		file.close()