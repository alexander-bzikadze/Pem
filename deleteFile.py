import sublime, sublime_plugin, os, subprocess

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "User", "correctnessTests.py")).load_module()
ir = SourceFileLoader("InfoReader", os.path.join(sublime.packages_path(), "User", "infoReader.py")).load_module()

extension = ".pem"
csextension = ".cs"

class DeleteFileCommand(sublime_plugin.TextCommand):
	def run(self, edit, name):
		info = ir.InfoReader()
		cT = ct.CorrectnessTests()
		cT.infoFileExistence()

		if cT.projectSelection():
			print("Project is not selected.")
			return 0
		if cT.projectFileExistence(info.getCurrentProject(), info.getCurrentProjectPath()):
			print("Project file not found or it is empty.")
			return 0

		projectPath = os.path.join(info.getCurrentProjectPath(), info.getCurrentProject() + extension)
		projectFile = open(projectPath, 'r')
		lines = projectFile.readlines()
		projectFile.close()
		if ('\t' + name + '\n' in lines) and (lines.index("source:\n") < lines.index('\t' + name + '\n')):
			os.remove(os.path.join(info.getCurrentProjectPath(), name + csextension))
			lines.remove('\t' + name + '\n')
			projectFile = open(projectPath, 'w')
			projectFile.writelines(lines)
			projectFile.close()
		else:
			print("Project does not contain such a file: ", name, ".")