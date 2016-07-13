import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "Pem", "Staff", "correctnessTests.py")).load_module()
rw = SourceFileLoader("ReaderWriter", os.path.join(sublime.packages_path(), "Pem", "Staff", "readerWriter.py")).load_module()

class CreateProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, name, path = os.path.expanduser('~/')):
		info = rw.InfoReader()
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()

		if cT.fileExistence(name + ".pem", path):
			print("Project path is already busy.")
			return 0

		infoWriter = rw.InfoWriter()
		if infoWriter.addProject(name, path):
			print("Project already exists.")
		infoWriter.switchProject(rw.InfoReader().getProjectNumber(name))

		projectFile = open(os.path.join(path, name) + ".pem", 'w')
		projectFile.write("project_name = " + name + '\n\n')
		projectFile.write("specification:" + "\n\n")
		projectFile.write("source:" + "\n\n")
		projectFile.close();