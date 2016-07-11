import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
ir = SourceFileLoader("InfoReader", os.path.join(sublime.packages_path(), "User", "infoReader.py")).load_module()

class InfoCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		info = ir.InfoReader()
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()
		print(info.getCurrentProject() + " " + info.getCurrentProjectPath())

