# Copyright (c) 2023, aseel-gh and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	data = get_all_attendance(filters)
	columns = get_columns()
	return columns, data


def get_all_attendance(filters):
	return frappe.db.get_all("Attendance", ['employee_name', 'attendance_date', 'department', 'status', 'check_in', 'check_out', 'work_hours', 'late_hours'], filters = filters)


def get_columns():
	columns = [
		{'fieldname': 'employee_name', 'label': 'employee name', 'fieldtype': 'Data'},
		{'fieldname': 'attendance_date', 'label': 'attendance date', 'fieldtype': 'Date'},
		{'fieldname': 'department', 'label': 'department', 'fieldtype': 'Link', 'options': 'Department' },
		{'fieldname': 'status', 'label': 'status', 'fieldtype': 'Data'},
		{'fieldname': 'check_in', 'label': 'check in', 'fieldtype': 'Time'},
		{'fieldname': 'check_out', 'label': 'check out', 'fieldtype': 'Time'},
		{'fieldname': 'work_hours', 'label': 'work hours', 'fieldtype': 'Float'},
		{'fieldname': 'late_hours', 'label': 'late hours', 'fieldtype': 'Float'}
	]

	return columns
