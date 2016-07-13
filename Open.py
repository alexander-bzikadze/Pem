import sublime, sublime_plugin, sys, os

from importlib.machinery import SourceFileLoader
iw = SourceFileLoader("InfoWriter", os.path.join(sublime.packages_path(), "User", "infoWriter.py")).load_module()

csprojextension = ".csproj"
pemextension = ".pem"

class OpenCommand(sublime_plugin.TextCommand):
	def run(self, edit, name, path):     
		wayTofile = os.path.join(path, name + csprojextension)
		print(wayTofile)
		if wayTofile:			
			csprojFile = open(wayTofile, 'r')
			wayTofile = os.path.join(path, name + pemextension)
			pemFile = open(wayTofile, 'w')
			infoWriter = iw.InfoWriter()
			if infoWriter.addProject(name, path):
				print("Project already exists")
				return 0
			pemFile.write("Project_name: " + name + "\n")
			pemFile.write("\n" + "Specification: " + "\n")
			check = 0
			for line in csprojFile:
				if len(line) > 27:
					output = ""
					if line[5] == "R" and line[6] == "e" and line[7] == "f": 
						i = 24
						while line[i] != '"': 
							output = output + line[i] 
							i = i + 1
						pemFile.write("    " + output + "\n")
					else:
						if line[5] == "C" and line[6] == "o" and line[7] == "m" and line[8] == "p": 
							if check == 0: pemFile.write("\n" + "Source: " + "\n")
							check = check + 1
							i = 22
							while line[i] != '.': 
								output = output + line[i] 
								i = i + 1
							pemFile.write("    " + output + "\n")
			csprojFile.close()
			pemFile.close()
			print("All ok")



