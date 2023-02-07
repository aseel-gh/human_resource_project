# Copyright (c) 2023, aseel-gh and contributors
# For license information, please see license.txt

import frappe
import datetime
from frappe.model.document import Document
from frappe.utils import getdate


def get_today():
	today = datetime.datetime.now().strftime("%Y-%m-%d")
	return today


class Employee(Document):
	# def __init__(self, *args, **kwargs):
	# 	super().__init__(args, kwargs)
	# 	self.employee_education = None
	# 	self.cv = None
	# 	self.dob = None
	# 	self.mobile = None
	# 	self.last_name = None
	# 	self.middle_name = None
	# 	self.first_name = None
	# 	self.full_name = None
	# 	self.cv_validation = None
	# 	self.age = None

	def validate(self):
		return
		self.cv_validation(),
		self.age(),
		self.full_name()

	def before_save(self):
		self.cv_validation_()
		self.validate_mobile()
		self.get_age()
		self.validate_age()
		self.get_fullname()

		self.validate_education()

	def cv_validation_(self):
		if 'English' in self.cv:
			self.cv_validation = 'Good'
		else:
			self.cv_validation = 'Not Good'

	def get_age(self):
		if self.dob < get_today():
			self.age = int((getdate(get_today()) - getdate(self.dob)).days / 356)
		else:
			frappe.throw("The date of birth can not be set as today's date!")

	def validate_age(self):
		if self.age >= 60 and self.status == "Active":
			frappe.throw("Age should be less than 60!")

	def get_fullname(self):
		self.full_name = self.first_name + " " + self.middle_name + " " + self.last_name

	def validate_mobile(self):
		if len(self.mobile) == 10:
			if self.mobile.startswith('05'):
				pass
			else:
				frappe.throw("Mobile number should start with 05")
		else:
			frappe.throw("Mobile number should be 10 digits!")

	def validate_education(self):
		# loop
		total_education = len(self.employee_education)

		# for x in self.employee_education:
		# 	total_education = total_education + 1

		if total_education >= 2:
			pass
		else:
			frappe.throw("Employee must have at least 2 educations")

