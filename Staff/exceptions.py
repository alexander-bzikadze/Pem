#!/usr/bin/python

import os

class ProjectNotSelectedException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class ProjectAbsenceInInfofile(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class ProjectFileNotCorrect(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)