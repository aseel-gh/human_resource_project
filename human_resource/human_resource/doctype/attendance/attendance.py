# Copyright (c) 2023, aseel-gh and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Attendance(Document):
	def validate(self):
		pass
		# return
		# self.work_hours(),
		# self.late_hours()

	def on_submit(self):
		self.get_work_hours()
		self.get_late_hours()
		self.update_status()

	def get_work_hours(self):
		pass

	def get_late_hours(self):
		pass

	def update_status(self):
		pass
