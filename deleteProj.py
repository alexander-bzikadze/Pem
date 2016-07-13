import sublime, sublime_plugin, os, subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "Pem", "Staff", "correctnessTests.py")).load_module()
rw = SourceFileLoader("ReaderWriter", os.path.join(sublime.packages_path(), "Pem", "Staff", "readerWriter.py")).load_module()

extension = ".pem"

class DeleteProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
		if name == "-1":
			print("Cannot delete nothing.")
			return 0
		self.view.run_command("switch_project", {"name" : name})
		info = rw.InfoReader()
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()

		if cT.projectSelection():
			# print("Project is not selected." # As it means, that project has not been found.
			return 0
		if name != info.getCurrentProject():
			# print ("No such project.") # As it means, that message will be sent in switch_project.
			return 0
		if cT.projectFileExistence(info.getCurrentProject(), info.getCurrentProjectPath()):
			print("Project file not found or it is empty.")
			return 0

		projectReader = rw.ProjectReader()
		for file in projectReader.getSource():
			self.view.run_command("delete_file", {"name" : file})
		os.remove(os.path.join(info.getCurrentProjectPath(), info.getCurrentProject() + extension))
		infoWriter = rw.InfoWriter()
		infoWriter.deleteProject(info.getProjectNumber(info.getCurrentProject()))
		infoWriter.switchProject(-1)