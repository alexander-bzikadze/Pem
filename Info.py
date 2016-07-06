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

		line = infoFile.readline()
		info = line.split()
		print(info[1] + " " + info[2])

		infoFile.close()

	def infoFileCreation(self, infoFileName):
		file = open(infoFileName, 'w')
		file.write("-1")
		file.close()

	def infoFileCorrectnessCheck(self, infoFileName):
		infoFile = open(infoFileName, 'r')
		lines = infoFile.readlines()
		if (len(lines[0].split()) != 3) or (len(lines[0].split()) == 1):
			if (lines[0].isdigit()):
				if int(lines[0]) != -1:
					return 0
			else:
				return 0;
		n = int(lines[0].split()[0])
		if len(lines) > n + 1 and n != -1:
			return -2
		for i in range(1, n):
			if len(lines[i].split()) != 2:
				return i
		infoFile.close()
		return -1

