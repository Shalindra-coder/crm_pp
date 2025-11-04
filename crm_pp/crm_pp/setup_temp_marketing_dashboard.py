import frappe
from frappe import _
from frappe.utils import add_days, today
import json


def create_temp_marketing_dashboard():
	"""Create Temp Leads & Opportunities (Marketing) Dashboard with all charts and number cards"""

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
		"RAI",
		"Direct Calls"
	]
	
	# Filter for Temporary Staffing vertical with Marketing sources (90 days)
	# Use json.dumps to properly format the list for JSON
	temp_mrkt_filter_90_days = json.dumps([
		["Lead", "custom_vertical", "=", "Temporary Staffing"],
		["Lead", "source", "in", marketing_sources],
		["Lead", "creation", ">=", date_90_days_ago]
	])
	
	temp_mrkt_opp_filter_90_days = json.dumps([
		["Opportunity", "custom_vertical", "=", "Temporary Staffing"],
		["Opportunity", "source", "in", marketing_sources],
		["Opportunity", "creation", ">=", date_90_days_ago]
	])

	# Create Number Cards for Temp Marketing Dashboard
	number_cards = [
		{
			"name": "Total Temp Leads - Marketing (90 Days)",
			"label": "Total Temp Leads - Marketing (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Lead",
			"document_type": "Lead",
			"report_function": "Sum",
			"filters_json": temp_mrkt_filter_90_days,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Total Temp Opportunities - Marketing (90 Days)",
			"label": "Total Temp Opportunities - Marketing (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": temp_mrkt_opp_filter_90_days,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Total Temp Opportunity Value - Marketing (90 Days)",
			"label": "Total Temp Opportunity Value - Marketing (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "opportunity_amount",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": temp_mrkt_opp_filter_90_days,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Temp Closed Won - Marketing (90 Days)",
			"label": "Temp Closed Won - Marketing (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "=", "Temporary Staffing"],
				["Opportunity", "source", "in", marketing_sources],
				["Opportunity", "status", "=", "Closed"],
				["Opportunity", "creation", ">=", date_90_days_ago]
			]),
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
	]

	print("Creating Number Cards for Temp Marketing Dashboard...")
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

	# Create Dashboard Charts for Temp Marketing Dashboard
	dashboard_charts = [
		# 1. Lead Status - Temp Marketing (Bar Chart)
		{
			"name": "Lead Status - Temp - Marketing - 90 Days",
			"chart_name": "Lead Status - Temp (Marketing)",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "status",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": temp_mrkt_filter_90_days,
		},
		# 2. Opportunity by Stage - Temp Marketing (Donut Chart)
		{
			"name": "Opportunity by Stage - Temp - Marketing",
			"chart_name": "Opportunity by Stage - Temp - (Marketing)",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "sales_stage",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "=", "Temporary Staffing"],
				["Opportunity", "source", "in", marketing_sources]
			]),
		},
		# 3. Allocated by BD - Temp Marketing (Donut Chart)
		{
			"name": "Allocated by BD - Temp - Marketing",
			"chart_name": "Allocated by BD - Temp - 90 (Mrkt)",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "lead_owner",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Temporary Staffing"],
				["Lead", "source", "in", marketing_sources]
			]),
			"number_of_groups": 10,
		},
		# 4. Lead Source - Temp Marketing (Donut Chart)
		{
			"name": "Lead Source - Temp - Marketing - 90 Days",
			"chart_name": "All Source- Lead source -Temp - (Mrkt)",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "source",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": temp_mrkt_filter_90_days,
		},
		# 5. Unqualified Reason - Temp Marketing (Bar Chart)
		{
			"name": "Unqualified Reason - Temp - Marketing",
			"chart_name": "Unqualified Reason - Temp - Mktg - 90",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "custom_unqualified_reason",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Temporary Staffing"],
				["Lead", "source", "in", marketing_sources],
				["Lead", "status", "=", "Do Not Contact"],
				["Lead", "creation", ">=", date_90_days_ago]
			]),
		},
		# 6. Lead Rating - Temp Marketing Pipeline (Donut Chart)
		{
			"name": "Lead Rating - Temp - Marketing - Pipeline",
			"chart_name": "Lead Rating - Temp - Mktg - 90 (Pipeline)",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "custom_rating",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "=", "Temporary Staffing"],
				["Opportunity", "source", "in", marketing_sources],
				["Opportunity", "status", "in", ["Open", "Quotation"]],
				["Opportunity", "creation", ">=", date_90_days_ago]
			]),
		},
		# 7. Lead Industry - Temp Marketing (Donut Chart)
		{
			"name": "Lead Industry - Temp - Marketing - 90 Days",
			"chart_name": "Lead Industry-Temp - (Mrkt) - 90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "industry",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": temp_mrkt_filter_90_days,
			"number_of_groups": 15,
		},
		# 8. TAT Todays Date - Temp Marketing (Bar Chart)
		{
			"name": "TAT Todays Date - Temp - Marketing - 90 Days",
			"chart_name": "TAT Todays Date - Temp - 90 Days - Marketing",
			"chart_type": "Count",
			"document_type": "Lead",
			"based_on": "creation",
			"timeseries": 0,
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": temp_mrkt_filter_90_days,
		},
		# 9. Temp Salary Offering - Marketing All Leads (Bar Chart)
		{
			"name": "Temp Salary Offering - Marketing - All Leads",
			"chart_name": "Temp Salary Offering - Mktg - All Leads - 90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "custom_salary_offering",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": temp_mrkt_filter_90_days,
		},
		# 10. Salary Offering - Temp Marketing Pipeline (Bar Chart)
		{
			"name": "Salary Offering - Temp - Marketing - Pipeline",
			"chart_name": "Salary Offerings - Temp - Open Opps - Marketing - 90 Days",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "custom_salary_band",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "=", "Temporary Staffing"],
				["Opportunity", "source", "in", marketing_sources],
				["Opportunity", "status", "in", ["Open", "Quotation"]],
				["Opportunity", "creation", ">=", date_90_days_ago]
			]),
		},
		# 11. Opportunities by Owner - Temp Marketing (Bar Chart)
		{
			"name": "Opportunities by Owner - Temp - Marketing",
			"chart_name": "Opportunities by Owner - Temp - Marketing",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "opportunity_owner",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": temp_mrkt_opp_filter_90_days,
			"number_of_groups": 10,
		},
		# 12. Temp Marketing Leads Trend - Last 90 Days (Line Chart)
		{
			"name": "Temp Marketing Leads Trend - 90 Days",
			"chart_name": "Temp Marketing Leads Trend - Last 90 Days",
			"chart_type": "Count",
			"document_type": "Lead",
			"based_on": "creation",
			"timeseries": 1,
			"time_interval": "Weekly",
			"timespan": "Last Quarter",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Line",
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Temporary Staffing"],
				["Lead", "source", "in", marketing_sources]
			]),
		},
		# 13. Temp Marketing Opportunities Trend - Last 90 Days (Line Chart)
		{
			"name": "Temp Marketing Opportunities Trend - 90 Days",
			"chart_name": "Temp Marketing Opportunities Trend - Last 90 Days",
			"chart_type": "Count",
			"document_type": "Opportunity",
			"based_on": "creation",
			"timeseries": 1,
			"time_interval": "Weekly",
			"timespan": "Last Quarter",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Line",
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "=", "Temporary Staffing"],
				["Opportunity", "source", "in", marketing_sources]
			]),
		},
	]

	print("\nCreating Dashboard Charts for Temp Marketing Dashboard...")
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
	dashboard_name = "Temp Leads & Opportunities (Marketing)"
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
						{"card": "Total Temp Leads - Marketing (90 Days)"},
						{"card": "Total Temp Opportunities - Marketing (90 Days)"},
						{"card": "Total Temp Opportunity Value - Marketing (90 Days)"},
						{"card": "Temp Closed Won - Marketing (90 Days)"},
					],
					"charts": [
						{"chart": "Lead Status - Temp (Marketing)", "width": "Half"},
						{"chart": "Opportunity by Stage - Temp - (Marketing)", "width": "Half"},
						{"chart": "TAT Todays Date - Temp - 90 Days - Marketing", "width": "Half"},
						{"chart": "Allocated by BD - Temp - 90 (Mrkt)", "width": "Half"},
						{"chart": "Unqualified Reason - Temp - Mktg - 90", "width": "Half"},
						{"chart": "Lead Rating - Temp - Mktg - 90 (Pipeline)", "width": "Half"},
						{"chart": "All Source- Lead source -Temp - (Mrkt)", "width": "Half"},
						{"chart": "Lead Industry-Temp - (Mrkt) - 90 Days", "width": "Half"},
						{"chart": "Temp Salary Offering - Mktg - All Leads - 90 Days", "width": "Half"},
						{"chart": "Salary Offerings - Temp - Open Opps - Marketing - 90 Days", "width": "Half"},
						{"chart": "Opportunities by Owner - Temp - Marketing", "width": "Half"},
						{"chart": "Temp Marketing Leads Trend - Last 90 Days", "width": "Half"},
						{"chart": "Temp Marketing Opportunities Trend - Last 90 Days", "width": "Half"},
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
	print("\n✅ Temp Marketing Dashboard components created successfully!")
	print(f"\nYou can now access the dashboard at: /app/dashboard-view/{dashboard_name}")


def update_temp_marketing_dashboard():
	"""Update existing Temp Marketing Dashboard to add all charts"""
	dashboard_name = "Temp Leads & Opportunities (Marketing)"
	
	if frappe.db.exists("Dashboard", dashboard_name):
		print(f"Updating dashboard: {dashboard_name}")
		dashboard = frappe.get_doc("Dashboard", dashboard_name)
		
		# Clear existing charts and cards
		dashboard.charts = []
		dashboard.cards = []
		
		# Add number cards
		cards_to_add = [
			"Total Temp Leads - Marketing (90 Days)",
			"Total Temp Opportunities - Marketing (90 Days)",
			"Total Temp Opportunity Value - Marketing (90 Days)",
			"Temp Closed Won - Marketing (90 Days)",
		]
		
		for card_name in cards_to_add:
			if frappe.db.exists("Number Card", card_name):
				dashboard.append("cards", {"card": card_name})
		
		# Add charts
		charts_to_add = [
			("Lead Status - Temp (Marketing)", "Half"),
			("Opportunity by Stage - Temp - (Marketing)", "Half"),
			("TAT Todays Date - Temp - 90 Days - Marketing", "Half"),
			("Allocated by BD - Temp - 90 (Mrkt)", "Half"),
			("Unqualified Reason - Temp - Mktg - 90", "Half"),
			("Lead Rating - Temp - Mktg - 90 (Pipeline)", "Half"),
			("All Source- Lead source -Temp - (Mrkt)", "Half"),
			("Lead Industry-Temp - (Mrkt) - 90 Days", "Half"),
			("Temp Salary Offering - Mktg - All Leads - 90 Days", "Half"),
			("Salary Offerings - Temp - Open Opps - Marketing - 90 Days", "Half"),
			("Opportunities by Owner - Temp - Marketing", "Half"),
			("Temp Marketing Leads Trend - Last 90 Days", "Half"),
			("Temp Marketing Opportunities Trend - Last 90 Days", "Half"),
		]
		
		for chart_name, width in charts_to_add:
			if frappe.db.exists("Dashboard Chart", chart_name):
				dashboard.append("charts", {"chart": chart_name, "width": width})
		
		dashboard.save(ignore_permissions=True)
		frappe.db.commit()
		print("✓ Dashboard updated successfully with all charts")
		print(f"\nYou can now access the dashboard at: /app/dashboard-view/{dashboard_name}")
	else:
		print(f"Dashboard '{dashboard_name}' does not exist. Run create_temp_marketing_dashboard() first.")


def delete_temp_marketing_dashboard():
	"""Delete the Temp Marketing Dashboard and all its components"""
	dashboard_name = "Temp Leads & Opportunities (Marketing)"
	
	# Delete dashboard
	if frappe.db.exists("Dashboard", dashboard_name):
		frappe.delete_doc("Dashboard", dashboard_name, ignore_permissions=True)
		print(f"✓ Deleted Dashboard: {dashboard_name}")
	
	# Delete charts
	charts = [
		"Lead Status - Temp - Marketing - 90 Days",
		"Opportunity by Stage - Temp - Marketing",
		"Allocated by BD - Temp - Marketing",
		"Lead Source - Temp - Marketing - 90 Days",
		"Unqualified Reason - Temp - Marketing",
		"Lead Rating - Temp - Marketing - Pipeline",
		"Lead Industry - Temp - Marketing - 90 Days",
		"TAT Todays Date - Temp - Marketing - 90 Days",
		"Temp Salary Offering - Marketing - All Leads",
		"Salary Offering - Temp - Marketing - Pipeline",
		"Opportunities by Owner - Temp - Marketing",
		"Temp Marketing Leads Trend - 90 Days",
		"Temp Marketing Opportunities Trend - 90 Days",
	]
	
	for chart_name in charts:
		if frappe.db.exists("Dashboard Chart", chart_name):
			frappe.delete_doc("Dashboard Chart", chart_name, ignore_permissions=True)
			print(f"✓ Deleted Dashboard Chart: {chart_name}")
	
	# Delete number cards
	cards = [
		"Total Temp Leads - Marketing (90 Days)",
		"Total Temp Opportunities - Marketing (90 Days)",
		"Total Temp Opportunity Value - Marketing (90 Days)",
		"Temp Closed Won - Marketing (90 Days)",
	]
	
	for card_name in cards:
		if frappe.db.exists("Number Card", card_name):
			frappe.delete_doc("Number Card", card_name, ignore_permissions=True)
			print(f"✓ Deleted Number Card: {card_name}")
	
	frappe.db.commit()
	print("\n✅ All Temp Marketing Dashboard components deleted successfully!")


if __name__ == "__main__":
	create_temp_marketing_dashboard()



