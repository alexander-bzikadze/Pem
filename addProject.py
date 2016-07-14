import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "Pem", "Staff", "correctnessTests.py")).load_module()
rw = SourceFileLoader("ReaderWriter", os.path.join(sublime.packages_path(), "Pem", "Staff", "readerWriter.py")).load_module()

csprojextension = ".csproj"

class AddProjectCommand(sublime_plugin.TextCommand):
	def __openCsprof(self, name, path):  
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()
		if cT.infoFileCorrectnessLite():
			print("Info file is not correct")
			return 0
		wayTofile = os.path.join(path, name + csprojextension)
		print(wayTofile)
		readerWriter = rw.ProjectWriter()
		if cT.fileExistence(name + csprojextension, path):
			if cT.projectFileExistence(name, path):					
				csprojFile = open(wayTofile, 'r')
				self.view.run_command("create_project", {"name" : name, "path" : path})
				#pemFile.write("\n" + "Specification: " + "\n")
				check = 0 			
				for line in csprojFile:
					if len(line) > 27:
						output = ""
						if line[5] == "R" and line[6] == "e" and line[7] == "f": 
							i = 24
							while line[i] != '"': 
								output = output + line[i] 
								i = i + 1
							#=pemFile.write("    " + output + "\n")
						elif line[5] == "C" and line[6] == "o" and line[7] == "m" and line[8] == "p": 
							#if check == 0: pemFile.write("\n" + "Source: " + "\n")
							check = check + 1
							i = 22
							while line[i] != '.': 
								output = output + line[i] 
								i = i + 1
							readerWriter.addFile(output)
				csprojFile.close()
			else:
				print("Project file is existence")
		else:
			print("Csproj file not found")
	def __getFileExtension(self, name):
		chekc = 0
		typeOfFile = ""
		for symbol in name:
			if chekc == 1:
				typeOfFile = typeOfFile + symbol
			if symbol == ".":
				chekc = 1
		if typeOfFile == "pem":
			return 1
		elif typeOfFile == "csproj":
			return 2
		return 0

	def run(self, edit, file):
		cT = ct.CorrectnessTests()
		infoWriter = rw.InfoWriter()
		if cT.fileExistence(file, os.path.join(sublime.packages_path(), "User")):
			typeFile = self.__getFileExtension(file)
			name = ""
			i = 0
			while file[i] != '.': 
				name = name + file[i] 
				i = i + 1
			if typeFile == 2:
				self.__openCsprof(name, os.path.join(sublime.packages_path(), "User"))
			elif typeFile == 1:
				infoWriter.addProject(name, os.path.join(sublime.packages_path(), "User"))
			else:
				print("Type of file is not correct")
		else:
			print("File did not found")
