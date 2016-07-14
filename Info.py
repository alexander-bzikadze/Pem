import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "Pem", "Staff", "correctnessTests.py")).load_module()
rw = SourceFileLoader("ReaderWriter", os.path.join(sublime.packages_path(), "Pem", "Staff", "readerWriter.py")).load_module()

class InfoCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		info = rw.InfoReader()
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()
		print(info.getCurrentProject() + " " + info.getCurrentProjectPath())