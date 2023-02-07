# Copyright (c) 2023, aseel-gh and contributors
# For license information, please see license.txt

from datetime import datetime
from datetime import timedelta
import frappe
from frappe.model.document import Document


class Attendance(Document):

    def validate(self):
        self.validate_check_time()
        self.get_work_hours()
        self.get_late_hours()

        return
        self.work_hours(),
        self.status()
        self.late_hours()

    def after_save(self):
        self.update_status()

    def on_submit(self):
        self.get_work_hours()
        self.get_late_hours()
        self.update_status()

    def validate_check_time(self):
        check_out = datetime.strptime(self.check_out, "%H:%M:%S")
        check_in = datetime.strptime(self.check_in, "%H:%M:%S")
        if check_in >= check_out:
            frappe.throw("Check-out time must be before than check-in time!")

    def get_work_hours(self):
        start_time = frappe.db.get_value('Attendance Settings', 'Main settings', 'start_time')
        end_time = frappe.db.get_value('Attendance Settings', 'Main settings', 'end_time')
        get_late_entry_grace = frappe.db.get_value('Attendance Settings', 'Main settings', 'late_entry_grace_period')
        get_early_exit_grace = frappe.db.get_value('Attendance Settings', 'Main settings', 'late_entry_grace_period')

        check_out = datetime.strptime(self.check_out, "%H:%M:%S")
        check_in = datetime.strptime(self.check_in, "%H:%M:%S")

        start_time_with_entry_grace = start_time + timedelta(minutes=get_late_entry_grace)
        end_time_with_exit_grace = end_time - timedelta(minutes=get_early_exit_grace)

        total_start_time = datetime.strptime(str(start_time_with_entry_grace), "%H:%M:%S")
        total_end_time = datetime.strptime(str(end_time_with_exit_grace), "%H:%M:%S")

        # employee came in time or early
        if check_in <= total_start_time:
            check_in = datetime.strptime(str(start_time), "%H:%M:%S")
        else:
            check_in = check_in - timedelta(minutes=get_late_entry_grace)

        # employee left in time or late
        if check_out >= total_end_time:
            check_out = datetime.strptime(str(end_time), "%H:%M:%S")
        else:
            check_out = check_out + timedelta(minutes=get_early_exit_grace)

        check_sum = check_out - check_in
        sec = check_sum.total_seconds()
        work_hours = sec / (60 * 60)
        self.work_hours = work_hours

    def get_late_hours(self):
        get_start_time = str(frappe.db.get_value('Attendance Settings', 'Main settings', 'start_time'))
        get_end_time = str(frappe.db.get_value('Attendance Settings', 'Main settings', 'end_time'))

        start_time = datetime.strptime(get_start_time, "%H:%M:%S")
        end_time = datetime.strptime(get_end_time, "%H:%M:%S")

        sum_official_working_hours = end_time - start_time
        sec = sum_official_working_hours.total_seconds()
        official_working_hours = sec / (60 * 60)

        self.late_hours = official_working_hours - self.work_hours

    def update_status(self):
        working_hours_threshold_for_absent = frappe.db.get_value('Attendance Settings', 'Main settings',
                                                                 'working_hours_threshold_for_absent')
        if self.late_hours >= working_hours_threshold_for_absent:
            self.status = 'Absent'
