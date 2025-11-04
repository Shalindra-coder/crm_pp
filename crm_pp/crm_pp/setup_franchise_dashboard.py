import frappe
from frappe import _
from frappe.utils import add_days, today
import json


def create_franchise_dashboard():
	"""Create Franchise Dashboard with all charts and number cards"""

	# Calculate date 90 days ago in YYYY-MM-DD format (ISO format for Frappe filters)
	date_90_days_ago = add_days(today(), -90)  # Returns in YYYY-MM-DD format
	
	# Filter for Franchise vertical (90 days)
	franchise_filter_90_days = json.dumps([
		["Lead", "custom_vertical", "=", "Franchise"],
		["Lead", "creation", ">=", date_90_days_ago]
	])
	
	franchise_opp_filter_90_days = json.dumps([
		["Opportunity", "custom_vertical", "=", "Franchise"],
		["Opportunity", "creation", ">=", date_90_days_ago]
	])

	# Create Number Cards for Franchise Dashboard
	number_cards = [
		{
			"name": "Total Franchise Leads (90 Days)",
			"label": "Total Franchise Leads (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Lead",
			"document_type": "Lead",
			"report_function": "Sum",
			"filters_json": franchise_filter_90_days,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Total Franchise Opportunities (90 Days)",
			"label": "Total Franchise Opportunities (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": franchise_opp_filter_90_days,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Total Franchise Opportunity Value (90 Days)",
			"label": "Total Franchise Opportunity Value (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "opportunity_amount",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": franchise_opp_filter_90_days,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Franchise Closed Won (90 Days)",
			"label": "Franchise Closed Won (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "=", "Franchise"],
				["Opportunity", "status", "=", "Closed"],
				["Opportunity", "creation", ">=", date_90_days_ago]
			]),
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
	]

	print("Creating Number Cards for Franchise Dashboard...")
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

	# Create Dashboard Charts for Franchise Dashboard
	dashboard_charts = [
		# 1. Franchise Qualified and Unqualified (Donut Chart)
		{
			"name": "Franchise Qualified and Unqualified",
			"chart_name": "Franchise Qualified and Unqualified",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "status",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Franchise"],
				["Lead", "status", "in", ["Working", "Nurturing", "Qualified", "Do Not Contact"]]
			]),
		},
		# 2. Leads Report Franchise as per Rating (Donut Chart)
		{
			"name": "Leads Report Franchise as per Rating",
			"chart_name": "Leads Report Franchise as per Rating",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "custom_rating",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Franchise"]
			]),
		},
		# 3. Franchise Leads Unqualified Reason (Bar Chart)
		{
			"name": "Franchise Leads Unqualified Reason",
			"chart_name": "Franchise Leads Unqualified Reason",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "custom_unqualified_reason",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Franchise"],
				["Lead", "status", "=", "Do Not Contact"],
				["Lead", "creation", ">=", date_90_days_ago]
			]),
		},
		# 4. Leads Report Franchise as per City (Bar Chart)
		{
			"name": "Leads Report Franchise as per City",
			"chart_name": "Leads Report Franchise as per City",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "city",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Franchise"]
			]),
			"number_of_groups": 20,
		},
		# 5. Franchise Leads As per Source (Donut Chart)
		{
			"name": "Franchise Leads As per Source",
			"chart_name": "Franchise Leads As per Source",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "source",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Franchise"]
			]),
		},
		# 6. Opportunity by Stage - Franchise (Donut Chart)
		{
			"name": "Opportunity by Stage - Franchise - 90 Days",
			"chart_name": "Opportunity by Stage - Franchise - 90 Days",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "sales_stage",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": franchise_opp_filter_90_days,
		},
		# 7. Lead Status - Franchise (Bar Chart)
		{
			"name": "Lead Status - Franchise - 90 Days",
			"chart_name": "Lead Status - Franchise - 90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "status",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": franchise_filter_90_days,
		},
		# 8. Industry Wise Leads - Franchise (Donut Chart)
		{
			"name": "Industry Wise Leads - Franchise - 90 Days",
			"chart_name": "Industry Wise Leads - Franchise - 90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "industry",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": franchise_filter_90_days,
			"number_of_groups": 15,
		},
		# 9. Opportunities by Owner - Franchise (Bar Chart)
		{
			"name": "Opportunities by Owner - Franchise - 90 Days",
			"chart_name": "Opportunities by Owner - Franchise - 90 Days",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "opportunity_owner",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": franchise_opp_filter_90_days,
			"number_of_groups": 10,
		},
		# 10. Franchise Leads Trend - Last 90 Days (Line Chart)
		{
			"name": "Franchise Leads Trend - 90 Days",
			"chart_name": "Franchise Leads Trend - Last 90 Days",
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
				["Lead", "custom_vertical", "=", "Franchise"]
			]),
		},
		# 11. Franchise Opportunities Trend - Last 90 Days (Line Chart)
		{
			"name": "Franchise Opportunities Trend - 90 Days",
			"chart_name": "Franchise Opportunities Trend - Last 90 Days",
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
				["Opportunity", "custom_vertical", "=", "Franchise"]
			]),
		},
		# 12. Expected Revenue - Franchise (Bar Chart)
		{
			"name": "Expected Revenue - Franchise - 90 Days",
			"chart_name": "Expected Revenue - Franchise - 90 Days",
			"chart_type": "Sum",
			"document_type": "Opportunity",
			"based_on": "party_name",
			"value_based_on": "opportunity_amount",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": franchise_opp_filter_90_days,
			"number_of_groups": 10,
		},
		# 13. Leads Allocated to BD - Franchise (Donut Chart)
		{
			"name": "Leads Allocated to BD - Franchise - 90 Days",
			"chart_name": "Leads Allocated to BD - Franchise - 90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "lead_owner",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": franchise_filter_90_days,
			"number_of_groups": 10,
		},
	]

	print("\nCreating Dashboard Charts for Franchise Dashboard...")
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
	dashboard_name = "Franchise"
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
						{"card": "Total Franchise Leads (90 Days)"},
						{"card": "Total Franchise Opportunities (90 Days)"},
						{"card": "Total Franchise Opportunity Value (90 Days)"},
						{"card": "Franchise Closed Won (90 Days)"},
					],
					"charts": [
						{"chart": "Franchise Qualified and Unqualified", "width": "Half"},
						{"chart": "Leads Report Franchise as per Rating", "width": "Half"},
						{"chart": "Franchise Leads Unqualified Reason", "width": "Half"},
						{"chart": "Leads Report Franchise as per City", "width": "Half"},
						{"chart": "Franchise Leads As per Source", "width": "Half"},
						{"chart": "Opportunity by Stage - Franchise - 90 Days", "width": "Half"},
						{"chart": "Lead Status - Franchise - 90 Days", "width": "Half"},
						{"chart": "Industry Wise Leads - Franchise - 90 Days", "width": "Half"},
						{"chart": "Opportunities by Owner - Franchise - 90 Days", "width": "Half"},
						{"chart": "Leads Allocated to BD - Franchise - 90 Days", "width": "Half"},
						{"chart": "Expected Revenue - Franchise - 90 Days", "width": "Half"},
						{"chart": "Franchise Leads Trend - Last 90 Days", "width": "Half"},
						{"chart": "Franchise Opportunities Trend - Last 90 Days", "width": "Half"},
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
	print("\n✅ Franchise Dashboard components created successfully!")
	print(f"\nYou can now access the dashboard at: /app/dashboard-view/{dashboard_name}")


def update_franchise_dashboard():
	"""Update existing Franchise Dashboard to add all charts"""
	dashboard_name = "Franchise"
	
	if frappe.db.exists("Dashboard", dashboard_name):
		print(f"Updating dashboard: {dashboard_name}")
		dashboard = frappe.get_doc("Dashboard", dashboard_name)
		
		# Clear existing charts and cards
		dashboard.charts = []
		dashboard.cards = []
		
		# Add number cards
		cards_to_add = [
			"Total Franchise Leads (90 Days)",
			"Total Franchise Opportunities (90 Days)",
			"Total Franchise Opportunity Value (90 Days)",
			"Franchise Closed Won (90 Days)",
		]
		
		for card_name in cards_to_add:
			if frappe.db.exists("Number Card", card_name):
				dashboard.append("cards", {"card": card_name})
		
		# Add charts
		charts_to_add = [
			("Franchise Qualified and Unqualified", "Half"),
			("Leads Report Franchise as per Rating", "Half"),
			("Franchise Leads Unqualified Reason", "Half"),
			("Leads Report Franchise as per City", "Half"),
			("Franchise Leads As per Source", "Half"),
			("Opportunity by Stage - Franchise - 90 Days", "Half"),
			("Lead Status - Franchise - 90 Days", "Half"),
			("Industry Wise Leads - Franchise - 90 Days", "Half"),
			("Opportunities by Owner - Franchise - 90 Days", "Half"),
			("Leads Allocated to BD - Franchise - 90 Days", "Half"),
			("Expected Revenue - Franchise - 90 Days", "Half"),
			("Franchise Leads Trend - Last 90 Days", "Half"),
			("Franchise Opportunities Trend - Last 90 Days", "Half"),
		]
		
		for chart_name, width in charts_to_add:
			if frappe.db.exists("Dashboard Chart", chart_name):
				dashboard.append("charts", {"chart": chart_name, "width": width})
		
		dashboard.save(ignore_permissions=True)
		frappe.db.commit()
		print("✓ Dashboard updated successfully with all charts")
		print(f"\nYou can now access the dashboard at: /app/dashboard-view/{dashboard_name}")
	else:
		print(f"Dashboard '{dashboard_name}' does not exist. Run create_franchise_dashboard() first.")


def delete_franchise_dashboard():
	"""Delete the Franchise Dashboard and all its components"""
	dashboard_name = "Franchise"
	
	# Delete dashboard
	if frappe.db.exists("Dashboard", dashboard_name):
		frappe.delete_doc("Dashboard", dashboard_name, ignore_permissions=True)
		print(f"✓ Deleted Dashboard: {dashboard_name}")
	
	# Delete charts
	charts = [
		"Franchise Qualified and Unqualified",
		"Leads Report Franchise as per Rating",
		"Franchise Leads Unqualified Reason",
		"Leads Report Franchise as per City",
		"Franchise Leads As per Source",
		"Opportunity by Stage - Franchise - 90 Days",
		"Lead Status - Franchise - 90 Days",
		"Industry Wise Leads - Franchise - 90 Days",
		"Opportunities by Owner - Franchise - 90 Days",
		"Leads Allocated to BD - Franchise - 90 Days",
		"Expected Revenue - Franchise - 90 Days",
		"Franchise Leads Trend - 90 Days",
		"Franchise Opportunities Trend - 90 Days",
	]
	
	for chart_name in charts:
		if frappe.db.exists("Dashboard Chart", chart_name):
			frappe.delete_doc("Dashboard Chart", chart_name, ignore_permissions=True)
			print(f"✓ Deleted Dashboard Chart: {chart_name}")
	
	# Delete number cards
	cards = [
		"Total Franchise Leads (90 Days)",
		"Total Franchise Opportunities (90 Days)",
		"Total Franchise Opportunity Value (90 Days)",
		"Franchise Closed Won (90 Days)",
	]
	
	for card_name in cards:
		if frappe.db.exists("Number Card", card_name):
			frappe.delete_doc("Number Card", card_name, ignore_permissions=True)
			print(f"✓ Deleted Number Card: {card_name}")
	
	frappe.db.commit()
	print("\n✅ All Franchise Dashboard components deleted successfully!")


if __name__ == "__main__":
	create_franchise_dashboard()



