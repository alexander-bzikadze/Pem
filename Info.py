import sublime, sublime_plugin, os

class InfoCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		infoFileName = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")

		if (os.path.isfile(infoFileName) != True) or (os.stat(infoFileName).st_size == 0):
			self.infoFileCreation(infoFileName)

		if not (int(self.infoFileCorrectnessCheck(infoFileName)) == -1):
			print("Reading failed. ", self.infoFileCorrectnessCheck(infoFileName))
			return 0

		infoFile = open(infoFileName, 'r')

		lines = infoFile.readlines()
		n = int(lines[0])
		if n != -1:
			print(lines[n])
		else:
			print("No project is active now.")

		infoFile.close()

	def infoFileCreation(self, infoFileName):
		file = open(infoFileName, 'w')
		file.write("-1")
		file.close()

	def infoFileCorrectnessCheck(self, infoFileName):
		infoFile = open(infoFileName, 'r')
		lines = infoFile.readlines()
		if len(lines[0].split()) > 1:
			return 0
		n = int(lines[0])
		if len(lines) > n + 1 and n != -1:
			return -2
		for i in range(1, n):
			if len(lines[i].split()) != 2:
				return i
		infoFile.close()
		return -1

