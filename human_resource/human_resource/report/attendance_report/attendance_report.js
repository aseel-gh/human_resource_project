// Copyright (c) 2023, aseel-gh and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Attendance Report"] = {
	"filters": [

	{ fieldname: 'employee', label: __('employee'), fieldtype: 'Link', options: 'Employee' },
	{ fieldname: 'attendance_date', label: __('attendance date'), fieldtype: 'Date'}

	]
};
