import frappe
import os
import json


def install_lead_mql_report():
	"""Install Lead MQL SQL - AK report"""
	
	report_name = "Lead MQL SQL - AK"
	
	print(f"\n{'='*70}")
	print(f"INSTALLING REPORT: {report_name}")
	print(f"{'='*70}\n")
	
	# Check if report already exists
	if frappe.db.exists("Report", report_name):
		print(f"✅ Report already exists: {report_name}")
		print(f"   URL: /app/query-report/{report_name}")
		return
	
	# Get the report JSON file path
	report_json_path = os.path.join(
		frappe.get_app_path("crm_pp"),
		"crm_pp", "report", "lead_mql_sql_ak", "lead_mql_sql_ak.json"
	)
	
	# Read the JSON file
	with open(report_json_path, 'r') as f:
		report_data = json.load(f)
	
	# Create the report
	try:
		report = frappe.get_doc(report_data)
		report.insert(ignore_permissions=True)
		frappe.db.commit()
		print(f"✅ Created Report: {report_name}")
		print(f"   Type: Script Report")
		print(f"   Module: CRM PP")
		print(f"   Reference DocType: Lead")
		print(f"\n   URL: /app/query-report/{report_name}")
	except Exception as e:
		print(f"✗ Error creating report: {str(e)}")
		frappe.log_error(message=str(e), title=f"Error creating report: {report_name}")
	
	print(f"\n{'='*70}")
	print(f"✅ Report installation complete!")
	print(f"{'='*70}\n")


if __name__ == "__main__":
	install_lead_mql_report()



