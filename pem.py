import sublime, sublime_plugin, os, platform

from importlib.machinery import SourceFileLoader
ct = SourceFileLoader("CorrectnessTests", os.path.join(sublime.packages_path(), "Pem", "Staff", "correctnessTests.py")).load_module()
rw = SourceFileLoader("ReaderWriter", os.path.join(sublime.packages_path(), "Pem", "Staff", "readerWriter.py")).load_module()

commandsWithoutArgs = ["get_all_proj", "get_files", "info", "run_project"]
oneArgCommands = ["add_file", "compile_project", "delete_file", "delete_project", "switch_project", "open_file", "open_project"]
twoArgsCommands = ["create_project"]

# Command to integrate GUI. Should be run from right button context menu.
class PemCommand(sublime_plugin.TextCommand):
	__command = ""
	def run(self, edit, args):
		try:
			if not args:
				sublime.active_window().show_input_panel("Pem command:", "Type command.", self.__setCommand, None, None)
			else:
				self.__command = args
				if not self.__command in commandsWithoutArgs:
					sublime.active_window().show_input_panel("Pem command:", "Type args. Split them with \"\\:\".", self.__onDone, None, None)
				else:
					self.__onDone()
		except Exception as exc:
			printBuf = []
			printBuf.append(type(exc))
			printBuf.append(exc.args)
			sublime.error_message("\n".join(printBuf))


	def __setCommand(self, args):
		self.__command = args
		if not self.__command in commandsWithoutArgs:
			sublime.active_window().show_input_panel("Pem command:", "Type args. Split them with \"\\:\".", self.__onDone, None, None)
		else:
			self.__onDone()

	def __onDone(self, args = ""):
		if args:
			args = args.split("\\:")
		if self.__command in commandsWithoutArgs:
			self.view.run_command(self.__command)
			if args:
				sublime.message_dialog("Unexpected arguments number - " + str(len(args)) + ". Expected 0. Ran anyway.")
		elif self.__command in oneArgCommands:
			if args:
				if self.__command in ["compile_project"]:
					self.view.run_command(self.__command, {"target" : args[0]})
				elif self.__command in ["add_file", "delete_project", "delete_file", "switch_project", "open_project", "open_file"]:
					self.view.run_command(self.__command, {"name" : args[0]})
				if len(args) > 1:
					sublime.message_dialog("Unexpected arguments number - " + str(len(args)) + ". Expected 1. Ran anyway.")
			else:
				sublime.error_message("Unexpected arguments number - 0. Expected 1. Cannot be run.")
		elif self.__command in twoArgsCommands:
			if self.__command in ["create_project"]:
				if not args:
					sublime.error_message("Unexpected arguments number - 0. Expected 1 or 2. Cannot be run.")
				elif len(args) == 1:
					self.view.run_command(self.__command, {"name" : args[0]})
				elif len(args) >= 2:
					self.view.run_command(self.__command, {"name" : args[0], "path" : args[1]})
					if len(args) > 2:
						sublime.message_dialog("Unexpected arguments number - " + str(len(args)) + ". Expected 1 or 2. Ran anyway.")
		else:
			sublime.error_message("Command " + str(self.__command) + " not found!")
