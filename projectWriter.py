import sublime, sublime_plugin, os

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
ir = SourceFileLoader("InfoReader", os.path.join(sublime.packages_path(), "User", "infoReader.py")).load_module()
pr = SourceFileLoader("ProjectReader", os.path.join(sublime.packages_path(), "User", "projectReader.py")).load_module()

extension = ".pem"
csextension = ".cs"

class ProjectWriter:
	def addFile(self, name):
		info = ir.InfoReader()
		project = pr.ProjectReader()
		projectPath = os.path.join(info.getCurrentProjectPath(), info.getCurrentProject() + extension)
		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		projectFile.close()

		if not name in project.getSource():
			lines.append('\t' + name + '\n')
			projectFile = open(projectPath, 'w')
			projectFile.writelines(lines)
			projectFile.close()
			project = pr.ProjectReader()
			return 0
		return 1

	def deleteFile(self, name):
		info = ir.InfoReader()
		project = pr.ProjectReader()
		projectPath = os.path.join(info.getCurrentProjectPath(), info.getCurrentProject() + extension)
		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		projectFile.close()
		if name in project.getSource():
			os.remove(os.path.join(info.getCurrentProjectPath(), name + csextension))
			lines.remove('\t' + name + '\n')
			projectFile = open(projectPath, 'w')
			projectFile.writelines(lines)
			projectFile.close()
			return 0
		return 1