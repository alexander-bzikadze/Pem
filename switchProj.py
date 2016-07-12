import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
ir = SourceFileLoader("InfoReader", os.path.join(sublime.packages_path(), "User", "infoReader.py")).load_module()
iw = SourceFileLoader("InfoWriter", os.path.join(sublime.packages_path(), "User", "infoWriter.py")).load_module()
Exceptions = SourceFileLoader("Exceptions", os.path.join(sublime.packages_path(), "User", "projectNotSelectedException.py")).load_module()

class SwitchProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
		infoFilePath = os.path.join(sublime.packages_path(), "User", "Pem", "Info.txt")
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()

		infoReader = ir.InfoReader()
		infoWriter = iw.InfoWriter()
		try:
			if name == infoReader.getCurrentProject():
				return
		except Exceptions.ProjectNotSelectedException:
			a = 3
		try:
			infoWriter.switchProject(infoReader.getProjectNumber(name))
		except ValueError:
			print("No such project", name, ".")