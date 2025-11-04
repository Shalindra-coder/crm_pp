import frappe


def install_priyanka_report():
	"""Install Lead report -Priyanka"""
	
	report_name = "Lead report -Priyanka"
	
	print(f"\n{'='*70}")
	print(f"INSTALLING REPORT: {report_name}")
	print(f"{'='*70}\n")
	
	# Check if report already exists
	if frappe.db.exists("Report", report_name):
		print(f"✅ Report already exists: {report_name}")
		print(f"   URL: /app/query-report/{report_name}")
		return
	
	# Create the report
	try:
		report = frappe.get_doc({
			"doctype": "Report",
			"report_name": report_name,
			"ref_doctype": "Lead",
			"report_type": "Script Report",
			"module": "CRM PP",
			"is_standard": "Yes",
			"add_total_row": 1,
			"roles": [
				{"role": "Sales User"},
				{"role": "Sales Manager"},
				{"role": "System Manager"}
			]
		})
		report.insert(ignore_permissions=True)
		frappe.db.commit()
		print(f"✅ Created Report: {report_name}")
		print(f"   Type: Script Report")
		print(f"   Module: CRM PP")
		print(f"   Reference DocType: Lead")
		print(f"   Features: Grouping, Subtotals, Grand Total, Summary")
		print(f"\n   URL: /app/query-report/{report_name}")
	except Exception as e:
		print(f"✗ Error creating report: {str(e)}")
		frappe.log_error(message=str(e), title=f"Error creating report: {report_name}")
	
	print(f"\n{'='*70}")
	print(f"✅ Report installation complete!")
	print(f"{'='*70}\n")


if __name__ == "__main__":
	install_priyanka_report()



