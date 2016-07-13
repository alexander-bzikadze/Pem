import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "Pem", "Staff", "correctnessTests.py")).load_module()
rw = SourceFileLoader("ReaderWriter", os.path.join(sublime.packages_path(), "Pem", "Staff", "readerWriter.py")).load_module()
Exceptions = SourceFileLoader("Exceptions", os.path.join(sublime.packages_path(), "Pem", "Staff", "exceptions.py")).load_module()

class SwitchProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()

		infoReader = rw.InfoReader()
		infoWriter = rw.InfoWriter()
		try:
			if name == infoReader.getCurrentProject():
				return
		except Exceptions.ProjectNotSelectedException:
			a = 3
		try:
			infoWriter.switchProject(infoReader.getProjectNumber(name))
		except Exceptions.ProjectAbsenceInInfofile:
			print("No such project", name, ".")