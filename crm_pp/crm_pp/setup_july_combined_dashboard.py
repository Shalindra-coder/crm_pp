import frappe
from frappe import _
from frappe.utils import add_days, today, get_first_day, get_last_day
import json


def create_july_combined_dashboard():
	"""Create July - Marketing - All verticals combined Dashboard"""

	# Filter for July 2025 (you can adjust the year as needed)
	july_start = "2025-07-01"
	july_end = "2025-07-31"
	
	# Verticals to include: L&D, LLC, Perm, Temp
	verticals = [
		"Learning & Development",
		"Labour Law Advisory & Compliance",
		"Permanent Staffing",
		"Temporary Staffing"
	]
	
	# Marketing sources
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
	
	# Combined filter for all verticals + marketing sources + July
	combined_filter_july = json.dumps([
		["Lead", "custom_vertical", "in", verticals],
		["Lead", "source", "in", marketing_sources],
		["Lead", "creation", ">=", july_start],
		["Lead", "creation", "<=", july_end]
	])
	
	combined_opp_filter_july = json.dumps([
		["Opportunity", "custom_vertical", "in", verticals],
		["Opportunity", "source", "in", marketing_sources],
		["Opportunity", "creation", ">=", july_start],
		["Opportunity", "creation", "<=", july_end]
	])

	# Create Number Cards
	number_cards = [
		{
			"name": "Total Leads - July Marketing - All Verticals",
			"label": "Total Leads - July Marketing - All Verticals",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Lead",
			"document_type": "Lead",
			"report_function": "Sum",
			"filters_json": combined_filter_july,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Total Opportunities - July Marketing - All Verticals",
			"label": "Total Opportunities - July Marketing - All Verticals",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": combined_opp_filter_july,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Total Opportunity Value - July Marketing - All Verticals",
			"label": "Total Opportunity Value - July Marketing - All Verticals",
			"function": "Sum",
			"aggregate_function_based_on": "opportunity_amount",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": combined_opp_filter_july,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Closed Won - July Marketing - All Verticals",
			"label": "Closed Won - July Marketing - All Verticals",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "in", verticals],
				["Opportunity", "source", "in", marketing_sources],
				["Opportunity", "status", "=", "Closed"],
				["Opportunity", "creation", ">=", july_start],
				["Opportunity", "creation", "<=", july_end]
			]),
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
	]

	print("Creating Number Cards for July Combined Dashboard...")
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

	# Create Dashboard Charts
	dashboard_charts = [
		# 1. July Lead Source - All Vertical (Donut Chart)
		{
			"name": "July Lead Source - All Vertical - Marketing",
			"chart_name": "July (Mrkt)- Lead source - All Vertical",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "source",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": combined_filter_july,
		},
		# 2. July Lead Status - All Vertical (Donut Chart)
		{
			"name": "July Lead Status - All Vertical - Marketing",
			"chart_name": "July (Mrkt) -Lead Status -All Vertical",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "status",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": combined_filter_july,
		},
		# 3. July Unqualified Reason - All Vertical (Bar Chart)
		{
			"name": "July Unqualified Reason - All Vertical - Marketing",
			"chart_name": "July (Mrkt) - Lead Status - All Ver - Unq",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "custom_unqualified_reason",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "in", verticals],
				["Lead", "source", "in", marketing_sources],
				["Lead", "status", "=", "Do Not Contact"],
				["Lead", "creation", ">=", july_start],
				["Lead", "creation", "<=", july_end]
			]),
		},
		# 4. July All Vertical (by Vertical - Bar Chart)
		{
			"name": "July All Vertical - Marketing",
			"chart_name": "July (Mrkt) - All Vertical",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "custom_vertical",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": combined_filter_july,
		},
		# 5. July Opportunity by Stage - All Vertical (Donut Chart)
		{
			"name": "July Opportunity by Stage - All Vertical - Marketing",
			"chart_name": "July (Mrkt) -Opportunity by Stage",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "sales_stage",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": combined_opp_filter_july,
		},
		# 6. July Lead by Industry - All Vertical (Donut Chart)
		{
			"name": "July Lead by Industry - All Vertical - Marketing",
			"chart_name": "July (Mrkt) - Lead by Industry",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "industry",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": combined_filter_july,
			"number_of_groups": 15,
		},
		# 7. July Lead Rating - All Vertical (Donut Chart)
		{
			"name": "July Lead Rating - All Vertical - Marketing",
			"chart_name": "July (Mrkt) - Lead Rating",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "custom_rating",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": combined_filter_july,
		},
		# 8. July Leads Trend (Line Chart)
		{
			"name": "July Leads Trend - All Vertical - Marketing",
			"chart_name": "July Leads Trend - All Vertical - Marketing",
			"chart_type": "Count",
			"document_type": "Lead",
			"based_on": "creation",
			"timeseries": 1,
			"time_interval": "Daily",
			"timespan": "Select Date Range",
			"from_date": july_start,
			"to_date": july_end,
			"is_public": 1,
			"module": "CRM PP",
			"type": "Line",
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "in", verticals],
				["Lead", "source", "in", marketing_sources]
			]),
		},
		# 9. July Opportunities Trend (Line Chart)
		{
			"name": "July Opportunities Trend - All Vertical - Marketing",
			"chart_name": "July Opportunities Trend - All Vertical - Marketing",
			"chart_type": "Count",
			"document_type": "Opportunity",
			"based_on": "creation",
			"timeseries": 1,
			"time_interval": "Daily",
			"timespan": "Select Date Range",
			"from_date": july_start,
			"to_date": july_end,
			"is_public": 1,
			"module": "CRM PP",
			"type": "Line",
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "in", verticals],
				["Opportunity", "source", "in", marketing_sources]
			]),
		},
		# 10. Leads by Vertical and Source (Bar Chart)
		{
			"name": "July Leads by Vertical - All Marketing",
			"chart_name": "July Leads by Vertical - All Marketing",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "custom_vertical",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": combined_filter_july,
		},
		# 11. Opportunities by Vertical (Bar Chart)
		{
			"name": "July Opportunities by Vertical - All Marketing",
			"chart_name": "July Opportunities by Vertical - All Marketing",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "custom_vertical",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": combined_opp_filter_july,
		},
		# 12. Expected Revenue by Vertical (Bar Chart)
		{
			"name": "July Expected Revenue by Vertical - Marketing",
			"chart_name": "July Expected Revenue by Vertical - Marketing",
			"chart_type": "Sum",
			"document_type": "Opportunity",
			"based_on": "custom_vertical",
			"value_based_on": "opportunity_amount",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": combined_opp_filter_july,
		},
		# 13. Lead Owner Allocation - All Verticals (Donut Chart)
		{
			"name": "July Lead Owner - All Vertical - Marketing",
			"chart_name": "July Lead Owner - All Vertical - Marketing",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "lead_owner",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": combined_filter_july,
			"number_of_groups": 10,
		},
	]

	print("\nCreating Dashboard Charts for July Combined Dashboard...")
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
	dashboard_name = "July - Marketing - All verticals combined (L&D, LLC, Perm, and Temp only)"
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
						{"card": "Total Leads - July Marketing - All Verticals"},
						{"card": "Total Opportunities - July Marketing - All Verticals"},
						{"card": "Total Opportunity Value - July Marketing - All Verticals"},
						{"card": "Closed Won - July Marketing - All Verticals"},
					],
					"charts": [
						{"chart": "July (Mrkt)- Lead source - All Vertical", "width": "Half"},
						{"chart": "July (Mrkt) -Lead Status -All Vertical", "width": "Half"},
						{"chart": "July (Mrkt) - Lead Status - All Ver - Unq", "width": "Half"},
						{"chart": "July (Mrkt) - All Vertical", "width": "Half"},
						{"chart": "July (Mrkt) -Opportunity by Stage", "width": "Half"},
						{"chart": "July (Mrkt) - Lead by Industry", "width": "Half"},
						{"chart": "July (Mrkt) - Lead Rating", "width": "Half"},
						{"chart": "July Leads Trend - All Vertical - Marketing", "width": "Half"},
						{"chart": "July Opportunities Trend - All Vertical - Marketing", "width": "Half"},
						{"chart": "July Leads by Vertical - All Marketing", "width": "Half"},
						{"chart": "July Opportunities by Vertical - All Marketing", "width": "Half"},
						{"chart": "July Expected Revenue by Vertical - Marketing", "width": "Half"},
						{"chart": "July Lead Owner - All Vertical - Marketing", "width": "Half"},
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
	print("\n✅ July Combined Dashboard components created successfully!")
	print(f"\nYou can now access the dashboard at: /app/dashboard-view/{dashboard_name}")


def update_july_combined_dashboard():
	"""Update existing July Combined Dashboard to add all charts"""
	dashboard_name = "July - Marketing - All verticals combined (L&D, LLC, Perm, and Temp only)"
	
	if frappe.db.exists("Dashboard", dashboard_name):
		print(f"Updating dashboard: {dashboard_name}")
		dashboard = frappe.get_doc("Dashboard", dashboard_name)
		
		# Clear existing charts and cards
		dashboard.charts = []
		dashboard.cards = []
		
		# Add number cards
		cards_to_add = [
			"Total Leads - July Marketing - All Verticals",
			"Total Opportunities - July Marketing - All Verticals",
			"Total Opportunity Value - July Marketing - All Verticals",
			"Closed Won - July Marketing - All Verticals",
		]
		
		for card_name in cards_to_add:
			if frappe.db.exists("Number Card", card_name):
				dashboard.append("cards", {"card": card_name})
		
		# Add charts
		charts_to_add = [
			("July (Mrkt)- Lead source - All Vertical", "Half"),
			("July (Mrkt) -Lead Status -All Vertical", "Half"),
			("July (Mrkt) - Lead Status - All Ver - Unq", "Half"),
			("July (Mrkt) - All Vertical", "Half"),
			("July (Mrkt) -Opportunity by Stage", "Half"),
			("July (Mrkt) - Lead by Industry", "Half"),
			("July (Mrkt) - Lead Rating", "Half"),
			("July Leads Trend - All Vertical - Marketing", "Half"),
			("July Opportunities Trend - All Vertical - Marketing", "Half"),
			("July Leads by Vertical - All Marketing", "Half"),
			("July Opportunities by Vertical - All Marketing", "Half"),
			("July Expected Revenue by Vertical - Marketing", "Half"),
			("July Lead Owner - All Vertical - Marketing", "Half"),
		]
		
		for chart_name, width in charts_to_add:
			if frappe.db.exists("Dashboard Chart", chart_name):
				dashboard.append("charts", {"chart": chart_name, "width": width})
		
		dashboard.save(ignore_permissions=True)
		frappe.db.commit()
		print("✓ Dashboard updated successfully with all charts")
		print(f"\nYou can now access the dashboard at: /app/dashboard-view/{dashboard_name}")
	else:
		print(f"Dashboard '{dashboard_name}' does not exist. Run create_july_combined_dashboard() first.")


def delete_july_combined_dashboard():
	"""Delete the July Combined Dashboard and all its components"""
	dashboard_name = "July - Marketing - All verticals combined (L&D, LLC, Perm, and Temp only)"
	
	# Delete dashboard
	if frappe.db.exists("Dashboard", dashboard_name):
		frappe.delete_doc("Dashboard", dashboard_name, ignore_permissions=True)
		print(f"✓ Deleted Dashboard: {dashboard_name}")
	
	# Delete charts
	charts = [
		"July Lead Source - All Vertical - Marketing",
		"July Lead Status - All Vertical - Marketing",
		"July Unqualified Reason - All Vertical - Marketing",
		"July All Vertical - Marketing",
		"July Opportunity by Stage - All Vertical - Marketing",
		"July Lead by Industry - All Vertical - Marketing",
		"July Lead Rating - All Vertical - Marketing",
		"July Leads Trend - All Vertical - Marketing",
		"July Opportunities Trend - All Vertical - Marketing",
		"July Leads by Vertical - All Marketing",
		"July Opportunities by Vertical - All Marketing",
		"July Expected Revenue by Vertical - Marketing",
		"July Lead Owner - All Vertical - Marketing",
	]
	
	for chart_name in charts:
		if frappe.db.exists("Dashboard Chart", chart_name):
			frappe.delete_doc("Dashboard Chart", chart_name, ignore_permissions=True)
			print(f"✓ Deleted Dashboard Chart: {chart_name}")
	
	# Delete number cards
	cards = [
		"Total Leads - July Marketing - All Verticals",
		"Total Opportunities - July Marketing - All Verticals",
		"Total Opportunity Value - July Marketing - All Verticals",
		"Closed Won - July Marketing - All Verticals",
	]
	
	for card_name in cards:
		if frappe.db.exists("Number Card", card_name):
			frappe.delete_doc("Number Card", card_name, ignore_permissions=True)
			print(f"✓ Deleted Number Card: {card_name}")
	
	frappe.db.commit()
	print("\n✅ All July Combined Dashboard components deleted successfully!")


if __name__ == "__main__":
	create_july_combined_dashboard()



