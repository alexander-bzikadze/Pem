import sublime, sublime_plugin, os

class InfoCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		infoFileName = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")

		infoFile = open(infoFileName)

		# if os.system(infoFileCheck):
		# 	os.system(infoFileCreation)

		# if os.system(infoFileCorrectionCheck):
		# 	print("!!!")
		# 	return 0

		lines = infoFile.readlines()
		n = int(lines[0])
		print(lines[n])

		infoFile.close()

