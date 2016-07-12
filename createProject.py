import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
ir = SourceFileLoader("InfoReader", os.path.join(sublime.packages_path(), "User", "infoReader.py")).load_module()
iw = SourceFileLoader("InfoWriter", os.path.join(sublime.packages_path(), "User", "infoWriter.py")).load_module()

class CreateProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, name, path = os.path.expanduser('~/')):
		info = ir.InfoReader()
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()

		if cT.fileExistence(name + ".pem", path):
			print("Project path is already busy.")
			return 0

		infoWriter = iw.InfoWriter()
		if infoWriter.addProject(name, path):
			print("Project already exists.")
		infoWriter.switchProject(ir.InfoReader().getProjectNumber(name))

		projectFile = open(os.path.join(path, name) + ".pem", 'w')
		projectFile.write("project_name = " + name + '\n\n')
		projectFile.write("specification:" + "\n\n")
		projectFile.write("source:" + "\n\n")
		projectFile.close();