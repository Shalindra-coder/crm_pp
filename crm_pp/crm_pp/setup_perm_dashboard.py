import frappe
from frappe import _
from frappe.utils import add_days, today, formatdate


def create_perm_dashboard():
	"""Create Perm Leads & Opportunities (All Source) Dashboard with all charts and number cards"""

	# Calculate date 90 days ago in YYYY-MM-DD format (ISO format for Frappe filters)
	date_90_days_ago = add_days(today(), -90)  # Returns in YYYY-MM-DD format
	
	# Filter for Permanent Staffing vertical (90 days)
	perm_filter_90_days = f'[["Lead","custom_vertical","=","Permanent Staffing"],["Lead","creation",">=","{date_90_days_ago}"]]'
	perm_opp_filter_90_days = f'[["Opportunity","custom_vertical","=","Permanent Staffing"],["Opportunity","creation",">=","{date_90_days_ago}"]]'

	# Create Number Cards for Perm Dashboard
	number_cards = [
		{
			"name": "Total Perm Leads - 90 Days",
			"label": "Total Perm Leads (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Lead",
			"document_type": "Lead",
			"report_function": "Sum",
			"filters_json": perm_filter_90_days,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Total Perm Opportunities - 90 Days",
			"label": "Total Perm Opportunities (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": perm_opp_filter_90_days,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Total Perm Opportunity Value - 90 Days",
			"label": "Total Perm Opportunity Value (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "opportunity_amount",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": perm_opp_filter_90_days,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Perm Closed Won - 90 Days",
			"label": "Perm Closed Won (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": f'[["Opportunity","custom_vertical","=","Permanent Staffing"],["Opportunity","status","=","Closed"],["Opportunity","creation",">=","{date_90_days_ago}"]]',
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
	]

	print("Creating Number Cards for Perm Dashboard...")
	for card_data in number_cards:
		if not frappe.db.exists("Number Card", card_data["name"]):
			try:
				card = frappe.get_doc({"doctype": "Number Card", **card_data})
				card.insert(ignore_permissions=True)
				print(f"✓ Created Number Card: {card_data['name']}")
			except Exception as e:
				print(f"✗ Error creating {card_data['name']}: {str(e)}")
		else:
			print(f"- Number Card already exists: {card_data['name']}")

	# Create Dashboard Charts for Perm Dashboard
	dashboard_charts = [
		# 1. Lead Status - Perm - 90 Days (Bar Chart)
		{
			"name": "Lead Status - Perm - 90 Days",
			"chart_name": "Lead Status - Perm - 90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "status",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": perm_filter_90_days,
		},
		# 2. Opportunity by Stage - Perm - Past 90 Days (Donut Chart)
		{
			"name": "Opportunity by Stage - Perm - 90 Days",
			"chart_name": "Opportunity by Stage - Perm - Past 90 Days",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "sales_stage",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": perm_opp_filter_90_days,
		},
		# 3. Leads Allocated to BD - Perm - Last 90 Days (Donut Chart)
		{
			"name": "Leads Allocated to BD - Perm - 90 Days",
			"chart_name": "Leads Allocated to BD - Perm - Last 90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "lead_owner",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": perm_filter_90_days,
			"number_of_groups": 10,
		},
		# 4. Total Leads - Perm - 90 Days by Source (Donut Chart)
		{
			"name": "Total Leads by Source - Perm - 90 Days",
			"chart_name": "Total Leads - Perm - 90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "source",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": perm_filter_90_days,
		},
		# 5. Unqualified Reason - Perm - 90 Days (Bar Chart)
		{
			"name": "Unqualified Reason - Perm - 90 Days",
			"chart_name": "Unqualified Reason - Perm - 90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "custom_unqualified_reason",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": f'[["Lead","custom_vertical","=","Permanent Staffing"],["Lead","status","=","Do Not Contact"],["Lead","creation",">=","{date_90_days_ago}"]]',
		},
		# 6. Industry Wise Leads - Perm - Past 90 Days (Donut Chart)
		{
			"name": "Industry Wise Leads - Perm - 90 Days",
			"chart_name": "Industry Wise Leads - Perm - Past 90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "industry",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": perm_filter_90_days,
			"number_of_groups": 15,
		},
		# 7. Rating - Perm - Past 90 Days Pipeline (Donut Chart)
		{
			"name": "Rating - Perm - 90 Days Pipeline",
			"chart_name": "Rating - Perm - Past 90 Days (Pipeline)",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "custom_rating",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": f'[["Opportunity","custom_vertical","=","Permanent Staffing"],["Opportunity","status","in",["Open","Quotation"]],["Opportunity","creation",">=","{date_90_days_ago}"]]',
		},
		# 8. Opportunities by Owner - Perm - 90 Days (Bar Chart)
		{
			"name": "Opportunities by Owner - Perm - 90 Days",
			"chart_name": "Opportunities by Owner - Perm - 90 Days",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "opportunity_owner",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": perm_opp_filter_90_days,
			"number_of_groups": 10,
		},
		# 9. Salary Offering - Perm - 90 Days - All Leads (Bar Chart)
		{
			"name": "Salary Offering - Perm - 90 Days All Leads",
			"chart_name": "Salary Offering - Perm - 90 Days - All Leads",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "custom_salary_offering",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": perm_filter_90_days,
		},
		# 10. Salary Offering - Perm - 90 Days Pipeline (Bar Chart)
		{
			"name": "Salary Offering - Perm - 90 Days Pipeline",
			"chart_name": "Salary Offering - Perm - 90 Days - (Pipeline)",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "custom_salary_band",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": f'[["Opportunity","custom_vertical","=","Permanent Staffing"],["Opportunity","status","in",["Open","Quotation"]],["Opportunity","creation",">=","{date_90_days_ago}"]]',
		},
		# 11. Perm Leads Trend - Last 90 Days (Line Chart)
		{
			"name": "Perm Leads Trend - 90 Days",
			"chart_name": "Perm Leads Trend - Last 90 Days",
			"chart_type": "Count",
			"document_type": "Lead",
			"based_on": "creation",
			"timeseries": 1,
			"time_interval": "Weekly",
			"timespan": "Last Quarter",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Line",
			"filters_json": '[["Lead","custom_vertical","=","Permanent Staffing"]]',
		},
		# 12. Perm Opportunities Trend - Last 90 Days (Line Chart)
		{
			"name": "Perm Opportunities Trend - 90 Days",
			"chart_name": "Perm Opportunities Trend - Last 90 Days",
			"chart_type": "Count",
			"document_type": "Opportunity",
			"based_on": "creation",
			"timeseries": 1,
			"time_interval": "Weekly",
			"timespan": "Last Quarter",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Line",
			"filters_json": '[["Opportunity","custom_vertical","=","Permanent Staffing"]]',
		},
		# 13. Expected vs Actual Revenue - Perm - 90 Days (Bar Chart)
		{
			"name": "Expected Revenue - Perm - 90 Days",
			"chart_name": "Expected Revenue - Perm - 90 Days",
			"chart_type": "Sum",
			"document_type": "Opportunity",
			"based_on": "party_name",
			"value_based_on": "opportunity_amount",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": perm_opp_filter_90_days,
			"number_of_groups": 10,
		},
	]

	print("\nCreating Dashboard Charts for Perm Dashboard...")
	for chart_data in dashboard_charts:
		if not frappe.db.exists("Dashboard Chart", chart_data["name"]):
			try:
				chart = frappe.get_doc({"doctype": "Dashboard Chart", **chart_data})
				chart.insert(ignore_permissions=True)
				print(f"✓ Created Dashboard Chart: {chart_data['name']}")
			except Exception as e:
				print(f"✗ Error creating {chart_data['name']}: {str(e)}")
		else:
			print(f"- Dashboard Chart already exists: {chart_data['name']}")

	# Create the Dashboard
	dashboard_name = "Perm Leads & Opportunities (All Source)"
	if not frappe.db.exists("Dashboard", dashboard_name):
		try:
			dashboard = frappe.get_doc(
				{
					"doctype": "Dashboard",
					"dashboard_name": dashboard_name,
					"module": "CRM PP",
					"is_standard": 0,
					"is_default": 0,
					"cards": [
						{"card": "Total Perm Leads (90 Days)"},
						{"card": "Total Perm Opportunities (90 Days)"},
						{"card": "Total Perm Opportunity Value (90 Days)"},
						{"card": "Perm Closed Won (90 Days)"},
					],
					"charts": [
						{"chart": "Lead Status - Perm - 90 Days", "width": "Half"},
						{"chart": "Opportunity by Stage - Perm - Past 90 Days", "width": "Half"},
						{"chart": "Salary Offering - Perm - 90 Days - (Pipeline)", "width": "Half"},
						{"chart": "Salary Offering - Perm - 90 Days - All Leads", "width": "Half"},
						{"chart": "Leads Allocated to BD - Perm - Last 90 Days", "width": "Half"},
						{"chart": "Total Leads - Perm - 90 Days", "width": "Half"},
						{"chart": "Unqualified Reason - Perm - 90 Days", "width": "Full"},
						{"chart": "Industry Wise Leads - Perm - Past 90 Days", "width": "Half"},
						{"chart": "Rating - Perm - Past 90 Days (Pipeline)", "width": "Half"},
						{"chart": "Opportunities by Owner - Perm - 90 Days", "width": "Half"},
						{"chart": "Expected Revenue - Perm - 90 Days", "width": "Half"},
						{"chart": "Perm Leads Trend - Last 90 Days", "width": "Half"},
						{"chart": "Perm Opportunities Trend - Last 90 Days", "width": "Half"},
					],
				}
			)
			dashboard.insert(ignore_permissions=True)
			print(f"\n✓ Created Dashboard: {dashboard_name}")
		except Exception as e:
			print(f"\n✗ Error creating Dashboard: {str(e)}")
			frappe.log_error(message=str(e), title=f"Error creating Dashboard: {dashboard_name}")
	else:
		print(f"\n- Dashboard already exists: {dashboard_name}")

	frappe.db.commit()
	print("\n✅ Perm Dashboard components created successfully!")
	print(f"\nYou can now access the dashboard at: /app/dashboard-view/{dashboard_name}")


def update_perm_dashboard():
	"""Update existing Perm Dashboard to add all charts"""
	dashboard_name = "Perm Leads & Opportunities (All Source)"
	
	if frappe.db.exists("Dashboard", dashboard_name):
		print(f"Updating dashboard: {dashboard_name}")
		dashboard = frappe.get_doc("Dashboard", dashboard_name)
		
		# Clear existing charts and cards
		dashboard.charts = []
		dashboard.cards = []
		
		# Add number cards - use exact names from Number Card
		cards_to_add = [
			"Total Perm Leads (90 Days)",
			"Total Perm Opportunities (90 Days)",
			"Total Perm Opportunity Value (90 Days)",
			"Perm Closed Won (90 Days)",
		]
		
		for card_name in cards_to_add:
			if frappe.db.exists("Number Card", card_name):
				dashboard.append("cards", {"card": card_name})
		
		# Add charts - use exact names from Dashboard Chart
		charts_to_add = [
			("Lead Status - Perm - 90 Days", "Half"),
			("Opportunity by Stage - Perm - Past 90 Days", "Half"),
			("Salary Offering - Perm - 90 Days - (Pipeline)", "Half"),
			("Salary Offering - Perm - 90 Days - All Leads", "Half"),
			("Leads Allocated to BD - Perm - Last 90 Days", "Half"),
			("Total Leads - Perm - 90 Days", "Half"),
			("Unqualified Reason - Perm - 90 Days", "Full"),
			("Industry Wise Leads - Perm - Past 90 Days", "Half"),
			("Rating - Perm - Past 90 Days (Pipeline)", "Half"),
			("Opportunities by Owner - Perm - 90 Days", "Half"),
			("Expected Revenue - Perm - 90 Days", "Half"),
			("Perm Leads Trend - Last 90 Days", "Half"),
			("Perm Opportunities Trend - Last 90 Days", "Half"),
		]
		
		for chart_name, width in charts_to_add:
			if frappe.db.exists("Dashboard Chart", chart_name):
				dashboard.append("charts", {"chart": chart_name, "width": width})
		
		dashboard.save(ignore_permissions=True)
		frappe.db.commit()
		print("✓ Dashboard updated successfully with all charts")
		print(f"\nYou can now access the dashboard at: /app/dashboard-view/{dashboard_name}")
	else:
		print(f"Dashboard '{dashboard_name}' does not exist. Run create_perm_dashboard() first.")


def delete_perm_dashboard():
	"""Delete the Perm Dashboard and all its components for a fresh start"""
	dashboard_name = "Perm Leads & Opportunities (All Source)"
	
	# Delete dashboard
	if frappe.db.exists("Dashboard", dashboard_name):
		frappe.delete_doc("Dashboard", dashboard_name, ignore_permissions=True)
		print(f"✓ Deleted Dashboard: {dashboard_name}")
	
	# Delete charts
	charts = [
		"Lead Status - Perm - 90 Days",
		"Opportunity by Stage - Perm - 90 Days",
		"Opportunity by Stage - Perm - Past 90 Days",  # Old name
		"Leads Allocated to BD - Perm - 90 Days",
		"Total Leads by Source - Perm - 90 Days",
		"Unqualified Reason - Perm - 90 Days",
		"Industry Wise Leads - Perm - 90 Days",
		"Rating - Perm - 90 Days Pipeline",
		"Opportunities by Owner - Perm - 90 Days",
		"Salary Offering - Perm - 90 Days All Leads",
		"Salary Offering - Perm - 90 Days Pipeline",
		"Salary Offering - Perm - 90 Days - (Pipeline)",  # Old name
		"Perm Leads Trend - 90 Days",
		"Perm Opportunities Trend - 90 Days",
		"Expected Revenue - Perm - 90 Days",
	]
	
	for chart_name in charts:
		if frappe.db.exists("Dashboard Chart", chart_name):
			frappe.delete_doc("Dashboard Chart", chart_name, ignore_permissions=True)
			print(f"✓ Deleted Dashboard Chart: {chart_name}")
	
	# Delete number cards
	cards = [
		"Total Perm Leads (90 Days)",
		"Total Perm Opportunities (90 Days)",
		"Total Perm Opportunity Value (90 Days)",
		"Perm Closed Won (90 Days)",
	]
	
	for card_name in cards:
		if frappe.db.exists("Number Card", card_name):
			frappe.delete_doc("Number Card", card_name, ignore_permissions=True)
			print(f"✓ Deleted Number Card: {card_name}")
	
	frappe.db.commit()
	print("\n✅ All Perm Dashboard components deleted successfully!")


if __name__ == "__main__":
	create_perm_dashboard()

