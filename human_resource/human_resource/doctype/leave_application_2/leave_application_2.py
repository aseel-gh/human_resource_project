# Copyright (c) 2023, aseel-gh and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import date_diff


class LeaveApplication2(Document):

# on update.
	def validate(self):
		self.set_total_leave_days()
		self.get_total_leaves_allocated()
		self.check_leave_balance()

# when submitted.
	def on_submit(self):
		self.update_balance_allocation_after_submit()

	def on_cancel(self):
		self.update_balance_allocation_after_cancel()

	def set_total_leave_days(self):
		if self.to_date and self.from_date:
			total_leave_days = date_diff(self.to_date, self.from_date) + 1
			if total_leave_days >= 0:
				self.total_leave_days = total_leave_days

	def get_total_leaves_allocated(self):
		if self.employee and self.from_date and self.to_date and self.leave_type:
			leaves_allocated = frappe.db.sql(""" select total_leaves_allocated from `tabLeave Allocation2` 
			where employee = %s and leave_type = %s and from_date <= %s and to_date >= %s""", (self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)
			# error in your SQL syntax

			if leaves_allocated:
				self.leave_balance_before_application = str(leaves_allocated[0].total_leaves_allocated)


	def check_leave_balance(self):
		if self.total_leave_days and self.leave_balance_before_application:
			if float(self.total_leave_days) > float(self.leave_balance_before_application):
				frappe.throw(_("not have balance for leave type " + self.leave_type))

	def update_balance_allocation_after_submit(self):
		new_balance_allocation = float(self.leave_balance_before_application) - self.total_leave_days
		frappe.db.sql(""" update `tabLeave Allocation2`  set  total_leaves_allocated = %s 
		where employee = %s and leave_type = %s and from_date <= %s 
		and to_date >= %s""", (new_balance_allocation, self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)


		frappe.db.commit

	def update_balance_allocation_after_cancel(self):
		leaves_allocated = frappe.db.sql(""" select total_leaves_allocated from `tabLeave Allocation2` 
			where employee = %s and leave_type = %s and from_date <= %s and to_date >= %s""", (self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)


		if leaves_allocated:
			self.leave_balance_before_application = str(leaves_allocated[0].total_leaves_allocated)

		new_balance_allocation = float(self.leave_balance_before_application) - self.total_leave_days
		frappe.db.sql(""" update 'tabLeave Allocation2' set  total_leaves_allocated = %s 
		where employee = %s and leave_type = %s and from_date <= %s 
		and to_date >= %s""", (new_balance_allocation, self.employee, self.leave_type, self.from_date, self.to_date), as_dict=1)
		# error in your SQL syntax

		frappe.db.commit


