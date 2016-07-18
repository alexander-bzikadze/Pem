#!/usr/bin/python

import os

# Signals that one cannot get projectname or projectpath as they do not exist as project not selected.
class ProjectNotSelectedException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

# Signals that given project is not contained by infofile.
class ProjectAbsenceInInfofile(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

# Signals that project file is not correct.
class ProjectFileNotCorrect(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

# Signals that project file does not exist.
class ProjectFileDoesNotExistException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)