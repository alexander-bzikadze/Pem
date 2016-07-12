import sublime, sublime_plugin, os, subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
ir = SourceFileLoader("InfoReader", os.path.join(sublime.packages_path(), "User", "infoReader.py")).load_module()
iw = SourceFileLoader("InfoWriter", os.path.join(sublime.packages_path(), "User", "infoWriter.py")).load_module()
pr = SourceFileLoader("ProjectReader", os.path.join(sublime.packages_path(), "User", "projectReader.py")).load_module()
pw = SourceFileLoader("ProjectWriter", os.path.join(sublime.packages_path(), "User", "projectWriter.py")).load_module()

extension = ".pem"

class DeleteProjectCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
		self.view.run_command("switch_project", {"name" : name})
		info = ir.InfoReader()
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

		projectReader = pr.ProjectReader()
		for file in projectReader.getSource():
			self.view.run_command("delete_file", {"name" : file})
		os.remove(os.path.join(info.getCurrentProjectPath(), info.getCurrentProject() + extension))
		infoWriter = iw.InfoWriter()
		infoWriter.deleteProject(info.getProjectNumber(info.getCurrentProject()))
		infoWriter.switchProject(-1)