import frappe


@frappe.whitelist()
def test_api(first_name=None):
    all_employee = []
    if first_name:
        all_employee = frappe.db.sql(""" select * from `tabEmployee`
        where first_name like %s  """, first_name, as_dict=1)
    return all_employee


@frappe.whitelist()
def create_attendance(attendance_date, check_in, check_out, user=None):
    if user:
        if not attendance_date:
            return "Invalid Input attendance date"

        if not check_in:
            return "Invalid Input check_in"

        if not check_out:
            return "Invalid Input check_out"

        user = frappe.session.user
        # employee = frappe.get_doc("Employee", {"user": user.name})
        employee = frappe.db.exists("Employee", {"user": user})
        new_attendance = frappe.new_doc("Attendance")
        new_attendance.employee = employee
        new_attendance.attendance_date = attendance_date
        new_attendance.check_in = check_in
        new_attendance.check_out = check_out
        new_attendance.insert()
        frappe.db.commit()
        return "Attendance created successfully"

    else:
        return "Invalid User"
