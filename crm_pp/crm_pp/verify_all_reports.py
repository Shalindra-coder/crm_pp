#!/usr/bin/env python3
"""
Verify All Custom Reports
Checks existence and details of all 4 custom reports
"""

import frappe


def verify_all_reports():
	"""Verify all custom reports exist and are properly configured"""
	
	reports = [
		"Lead MQL SQL - AK",
		"Lead report -Priyanka",
		"Daily Leads Report-Shreya",
		"Opportunities Closed Won This Q by Type"
	]
	
	print("\n" + "="*80)
	print("CUSTOM REPORTS VERIFICATION")
	print("="*80 + "\n")
	
	for report_name in reports:
		if frappe.db.exists("Report", report_name):
			report_data = frappe.db.get_value(
				"Report",
				report_name,
				["name", "ref_doctype", "report_type", "is_standard"],
				as_dict=True
			)
			print(f"✅ {report_name}")
			print(f"   DocType: {report_data.ref_doctype}")
			print(f"   Type: {report_data.report_type}")
			print(f"   Standard: {report_data.is_standard}")
			print()
		else:
			print(f"❌ {report_name} - NOT FOUND")
			print()
	
	print("="*80)
	print(f"TOTAL REPORTS: {len(reports)}")
	print("="*80 + "\n")


if __name__ == "__main__":
	verify_all_reports()

