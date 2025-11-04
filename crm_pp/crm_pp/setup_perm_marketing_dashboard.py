import frappe
from frappe import _
from frappe.utils import add_days, today
import json


def create_perm_marketing_dashboard():
	"""Create Perm Leads & Opportunities (Marketing) Dashboard with all charts and number cards"""

	# Calculate date 90 days ago in YYYY-MM-DD format (ISO format for Frappe filters)
	date_90_days_ago = add_days(today(), -90)  # Returns in YYYY-MM-DD format
	
	# Marketing sources (based on Salesforce dashboard)
	marketing_sources = [
		"Social Media Ads",
		"Google AdWords",
		"Smatbot_SEO",
		"Email Marketing",
		"Direct_Emails_SEO",
		"Website_form_SEO",
		"what's_App-Marketing",
		"Conference",
		"RAI"
	]
	
	# Filter for Permanent Staffing vertical with Marketing sources (90 days)
	# Use json.dumps to properly format the list for JSON
	perm_mrkt_filter_90_days = f'[["Lead","custom_vertical","=","Permanent Staffing"],["Lead","source","in",{json.dumps(marketing_sources)}],["Lead","creation",">=","{date_90_days_ago}"]]'
	perm_mrkt_opp_filter_90_days = f'[["Opportunity","custom_vertical","=","Permanent Staffing"],["Opportunity","source","in",{json.dumps(marketing_sources)}],["Opportunity","creation",">=","{date_90_days_ago}"]]'

	# Create Number Cards for Perm Marketing Dashboard
	number_cards = [
		{
			"name": "Total Perm Leads - Marketing (90 Days)",
			"label": "Total Perm Leads - Marketing (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Lead",
			"document_type": "Lead",
			"report_function": "Sum",
			"filters_json": perm_mrkt_filter_90_days,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Total Perm Opportunities - Marketing (90 Days)",
			"label": "Total Perm Opportunities - Marketing (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": perm_mrkt_opp_filter_90_days,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Total Perm Opportunity Value - Marketing (90 Days)",
			"label": "Total Perm Opportunity Value - Marketing (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "opportunity_amount",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": perm_mrkt_opp_filter_90_days,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Perm Closed Won - Marketing (90 Days)",
			"label": "Perm Closed Won - Marketing (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": f'[["Opportunity","custom_vertical","=","Permanent Staffing"],["Opportunity","source","in",{json.dumps(marketing_sources)}],["Opportunity","status","=","Closed"],["Opportunity","creation",">=","{date_90_days_ago}"]]',
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
	]

	print("Creating Number Cards for Perm Marketing Dashboard...")
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

	# Create Dashboard Charts for Perm Marketing Dashboard
	dashboard_charts = [
		# 1. Lead Status - Perm - 90 Days Marketing (Bar Chart)
		{
			"name": "Lead Status - Perm - Marketing - 90 Days",
			"chart_name": "(Mrkt) - Lead Status - Perm - 90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "status",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": perm_mrkt_filter_90_days,
		},
		# 2. Opportunity by Stage - Perm Marketing (Donut Chart)
		{
			"name": "Opportunity by Stage - Perm - Marketing",
			"chart_name": "(Mrkt) - Opportunity by Stage - Perm",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "sales_stage",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": f'[["Opportunity","custom_vertical","=","Permanent Staffing"],["Opportunity","source","in",{json.dumps(marketing_sources)}]]',
		},
		# 3. Leads Allocated by BD - Perm Marketing (Donut Chart)
		{
			"name": "Leads Allocated by BD - Perm - Marketing",
			"chart_name": "(Mrkt) - Leads Allocated by BD - Perm",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "lead_owner",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": f'[["Lead","custom_vertical","=","Permanent Staffing"],["Lead","source","in",{json.dumps(marketing_sources)}]]',
			"number_of_groups": 10,
		},
		# 4. Perm - 90 Days Marketing Lead Source (Donut Chart)
		{
			"name": "Perm Lead Source - Marketing - 90 Days",
			"chart_name": "(Mrkt) - Perm - 90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "source",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": perm_mrkt_filter_90_days,
		},
		# 5. Unqualified Reason - Perm Marketing (Bar Chart)
		{
			"name": "Unqualified Reason - Perm - Marketing",
			"chart_name": "Unqualified Reason - Perm - (Mrkt)",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "custom_unqualified_reason",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": f'[["Lead","custom_vertical","=","Permanent Staffing"],["Lead","source","in",{json.dumps(marketing_sources)}],["Lead","status","=","Do Not Contact"],["Lead","creation",">=","{date_90_days_ago}"]]',
		},
		# 6. Industry Wise Leads - Perm Marketing (Donut Chart)
		{
			"name": "Industry Wise Leads - Perm - Marketing - 60 Days",
			"chart_name": "Industry Wise Leads - Perm - Past 60 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "industry",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": f'[["Lead","custom_vertical","=","Permanent Staffing"],["Lead","source","in",{json.dumps(marketing_sources)}],["Lead","creation",">=","{add_days(today(), -60)}"]]',
			"number_of_groups": 15,
		},
		# 7. Lead Source - Industry Marketing 90 Days (Donut Chart)
		{
			"name": "Lead Source - Industry - Marketing - 90 Days",
			"chart_name": "Lead Source - Industry - (Mrkt) - 90Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "industry",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": perm_mrkt_filter_90_days,
			"number_of_groups": 15,
		},
		# 8. TAT Todays Date - Perm Marketing 90 Days (Donut Chart)
		{
			"name": "TAT Todays Date - Perm - Marketing - 90 Days",
			"chart_name": "TAT Todays Date - Perm - 90 Days - (Mrkt)",
			"chart_type": "Count",
			"document_type": "Lead",
			"based_on": "creation",
			"timeseries": 0,
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": perm_mrkt_filter_90_days,
		},
		# 9. Salary Offering - Perm Marketing All Leads (Bar Chart)
		{
			"name": "Salary Offering - Perm - Marketing - All Leads",
			"chart_name": "Salary Offerings - Perm - (Mrkt)",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "custom_salary_offering",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": perm_mrkt_filter_90_days,
		},
		# 10. Salary Offering - Perm Marketing Pipeline (Bar Chart)
		{
			"name": "Salary Offering - Perm - Marketing - Pipeline",
			"chart_name": "(Mrkt) - Perm Salary Offering",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "custom_salary_band",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": f'[["Opportunity","custom_vertical","=","Permanent Staffing"],["Opportunity","source","in",{json.dumps(marketing_sources)}],["Opportunity","status","in",["Open","Quotation"]],["Opportunity","creation",">=","{date_90_days_ago}"]]',
		},
		# 11. Opportunities by Owner - Perm Marketing (Bar Chart)
		{
			"name": "Opportunities by Owner - Perm - Marketing",
			"chart_name": "Opportunities by Owner - Perm - Marketing",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "opportunity_owner",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": perm_mrkt_opp_filter_90_days,
			"number_of_groups": 10,
		},
		# 12. Perm Marketing Leads Trend - Last 90 Days (Line Chart)
		{
			"name": "Perm Marketing Leads Trend - 90 Days",
			"chart_name": "Perm Marketing Leads Trend - Last 90 Days",
			"chart_type": "Count",
			"document_type": "Lead",
			"based_on": "creation",
			"timeseries": 1,
			"time_interval": "Weekly",
			"timespan": "Last Quarter",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Line",
			"filters_json": f'[["Lead","custom_vertical","=","Permanent Staffing"],["Lead","source","in",{json.dumps(marketing_sources)}]]',
		},
		# 13. Perm Marketing Opportunities Trend - Last 90 Days (Line Chart)
		{
			"name": "Perm Marketing Opportunities Trend - 90 Days",
			"chart_name": "Perm Marketing Opportunities Trend - Last 90 Days",
			"chart_type": "Count",
			"document_type": "Opportunity",
			"based_on": "creation",
			"timeseries": 1,
			"time_interval": "Weekly",
			"timespan": "Last Quarter",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Line",
			"filters_json": f'[["Opportunity","custom_vertical","=","Permanent Staffing"],["Opportunity","source","in",{json.dumps(marketing_sources)}]]',
		},
	]

	print("\nCreating Dashboard Charts for Perm Marketing Dashboard...")
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
	dashboard_name = "Perm Leads & Opportunities (Marketing)"
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
						{"card": "Total Perm Leads - Marketing (90 Days)"},
						{"card": "Total Perm Opportunities - Marketing (90 Days)"},
						{"card": "Total Perm Opportunity Value - Marketing (90 Days)"},
						{"card": "Perm Closed Won - Marketing (90 Days)"},
					],
					"charts": [
						{"chart": "(Mrkt) - Lead Status - Perm - 90 Days", "width": "Half"},
						{"chart": "(Mrkt) - Opportunity by Stage - Perm", "width": "Half"},
						{"chart": "TAT Todays Date - Perm - 90 Days - (Mrkt)", "width": "Half"},
						{"chart": "Industry Wise Leads - Perm - Past 60 Days", "width": "Half"},
						{"chart": "Unqualified Reason - Perm - (Mrkt)", "width": "Half"},
						{"chart": "(Mrkt) - Perm - 90 Days", "width": "Half"},
						{"chart": "(Mrkt) - Leads Allocated by BD - Perm", "width": "Half"},
						{"chart": "Lead Source - Industry - (Mrkt) - 90Days", "width": "Half"},
						{"chart": "Salary Offerings - Perm - (Mrkt)", "width": "Half"},
						{"chart": "(Mrkt) - Perm Salary Offering", "width": "Half"},
						{"chart": "Opportunities by Owner - Perm - Marketing", "width": "Half"},
						{"chart": "Perm Marketing Leads Trend - Last 90 Days", "width": "Half"},
						{"chart": "Perm Marketing Opportunities Trend - Last 90 Days", "width": "Half"},
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
	print("\n✅ Perm Marketing Dashboard components created successfully!")
	print(f"\nYou can now access the dashboard at: /app/dashboard-view/{dashboard_name}")


def update_perm_marketing_dashboard():
	"""Update existing Perm Marketing Dashboard to add all charts"""
	dashboard_name = "Perm Leads & Opportunities (Marketing)"
	
	if frappe.db.exists("Dashboard", dashboard_name):
		print(f"Updating dashboard: {dashboard_name}")
		dashboard = frappe.get_doc("Dashboard", dashboard_name)
		
		# Clear existing charts and cards
		dashboard.charts = []
		dashboard.cards = []
		
		# Add number cards
		cards_to_add = [
			"Total Perm Leads - Marketing (90 Days)",
			"Total Perm Opportunities - Marketing (90 Days)",
			"Total Perm Opportunity Value - Marketing (90 Days)",
			"Perm Closed Won - Marketing (90 Days)",
		]
		
		for card_name in cards_to_add:
			if frappe.db.exists("Number Card", card_name):
				dashboard.append("cards", {"card": card_name})
		
		# Add charts
		charts_to_add = [
			("(Mrkt) - Lead Status - Perm - 90 Days", "Half"),
			("(Mrkt) - Opportunity by Stage - Perm", "Half"),
			("TAT Todays Date - Perm - 90 Days - (Mrkt)", "Half"),
			("Industry Wise Leads - Perm - Past 60 Days", "Half"),
			("Unqualified Reason - Perm - (Mrkt)", "Half"),
			("(Mrkt) - Perm - 90 Days", "Half"),
			("(Mrkt) - Leads Allocated by BD - Perm", "Half"),
			("Lead Source - Industry - (Mrkt) - 90Days", "Half"),
			("Salary Offerings - Perm - (Mrkt)", "Half"),
			("(Mrkt) - Perm Salary Offering", "Half"),
			("Opportunities by Owner - Perm - Marketing", "Half"),
			("Perm Marketing Leads Trend - Last 90 Days", "Half"),
			("Perm Marketing Opportunities Trend - Last 90 Days", "Half"),
		]
		
		for chart_name, width in charts_to_add:
			if frappe.db.exists("Dashboard Chart", chart_name):
				dashboard.append("charts", {"chart": chart_name, "width": width})
		
		dashboard.save(ignore_permissions=True)
		frappe.db.commit()
		print("✓ Dashboard updated successfully with all charts")
		print(f"\nYou can now access the dashboard at: /app/dashboard-view/{dashboard_name}")
	else:
		print(f"Dashboard '{dashboard_name}' does not exist. Run create_perm_marketing_dashboard() first.")


def delete_perm_marketing_dashboard():
	"""Delete the Perm Marketing Dashboard and all its components"""
	dashboard_name = "Perm Leads & Opportunities (Marketing)"
	
	# Delete dashboard
	if frappe.db.exists("Dashboard", dashboard_name):
		frappe.delete_doc("Dashboard", dashboard_name, ignore_permissions=True)
		print(f"✓ Deleted Dashboard: {dashboard_name}")
	
	# Delete charts
	charts = [
		"Lead Status - Perm - Marketing - 90 Days",
		"Opportunity by Stage - Perm - Marketing",
		"Leads Allocated by BD - Perm - Marketing",
		"Perm Lead Source - Marketing - 90 Days",
		"Unqualified Reason - Perm - Marketing",
		"Industry Wise Leads - Perm - Marketing - 60 Days",
		"Lead Source - Industry - Marketing - 90 Days",
		"TAT Todays Date - Perm - Marketing - 90 Days",
		"Salary Offering - Perm - Marketing - All Leads",
		"Salary Offering - Perm - Marketing - Pipeline",
		"Opportunities by Owner - Perm - Marketing",
		"Perm Marketing Leads Trend - 90 Days",
		"Perm Marketing Opportunities Trend - 90 Days",
	]
	
	for chart_name in charts:
		if frappe.db.exists("Dashboard Chart", chart_name):
			frappe.delete_doc("Dashboard Chart", chart_name, ignore_permissions=True)
			print(f"✓ Deleted Dashboard Chart: {chart_name}")
	
	# Delete number cards
	cards = [
		"Total Perm Leads - Marketing (90 Days)",
		"Total Perm Opportunities - Marketing (90 Days)",
		"Total Perm Opportunity Value - Marketing (90 Days)",
		"Perm Closed Won - Marketing (90 Days)",
	]
	
	for card_name in cards:
		if frappe.db.exists("Number Card", card_name):
			frappe.delete_doc("Number Card", card_name, ignore_permissions=True)
			print(f"✓ Deleted Number Card: {card_name}")
	
	frappe.db.commit()
	print("\n✅ All Perm Marketing Dashboard components deleted successfully!")


if __name__ == "__main__":
	create_perm_marketing_dashboard()

