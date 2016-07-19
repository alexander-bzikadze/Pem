import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "Pem", "Staff", "correctnessTests.py")).load_module()
rw = SourceFileLoader("ReaderWriter", os.path.join(sublime.packages_path(), "Pem", "Staff", "readerWriter.py")).load_module()

# Prints list of all project, found in infofile.
# You can see the list of checks in code.
class GetAllProjCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		info = rw.InfoReader()
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()
		printBuf = ["Command result (might be empty):"]
		
		if cT.infoFileCorrectnessHard():
			sublime.error_message("Prepare yourself. Incorrect info-file is coming.")

		for project in info.getProjects():
			printBuf.append(project)

		sublime.message_dialog("\n".join([str(i) for i in printBuf]))