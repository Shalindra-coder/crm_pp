import frappe
from frappe import _
from frappe.utils import add_days, today
import json


def create_ld_marketing_dashboard():
	"""Create L&D Leads & Opportunities (Marketing) Dashboard with all charts and number cards"""

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
	
	# Filter for Learning & Development vertical with Marketing sources (90 days)
	# Use json.dumps to properly format the list for JSON
	ld_mrkt_filter_90_days = json.dumps([
		["Lead", "custom_vertical", "=", "Learning & Development"],
		["Lead", "source", "in", marketing_sources],
		["Lead", "creation", ">=", date_90_days_ago]
	])
	
	ld_mrkt_opp_filter_90_days = json.dumps([
		["Opportunity", "custom_vertical", "=", "Learning & Development"],
		["Opportunity", "source", "in", marketing_sources],
		["Opportunity", "creation", ">=", date_90_days_ago]
	])

	# Create Number Cards for L&D Marketing Dashboard
	number_cards = [
		{
			"name": "Total L&D Leads - Marketing (90 Days)",
			"label": "Total L&D Leads - Marketing (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Lead",
			"document_type": "Lead",
			"report_function": "Sum",
			"filters_json": ld_mrkt_filter_90_days,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Total L&D Opportunities - Marketing (90 Days)",
			"label": "Total L&D Opportunities - Marketing (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": ld_mrkt_opp_filter_90_days,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "Total L&D Opportunity Value - Marketing (90 Days)",
			"label": "Total L&D Opportunity Value - Marketing (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "opportunity_amount",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": ld_mrkt_opp_filter_90_days,
			"is_public": 1,
			"show_percentage_stats": 1,
			"stats_time_interval": "Monthly",
			"module": "CRM PP",
		},
		{
			"name": "L&D Closed Won - Marketing (90 Days)",
			"label": "L&D Closed Won - Marketing (90 Days)",
			"function": "Sum",
			"aggregate_function_based_on": "creation",
			"doctype_name": "Opportunity",
			"document_type": "Opportunity",
			"report_function": "Sum",
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "=", "Learning & Development"],
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

	print("Creating Number Cards for L&D Marketing Dashboard...")
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

	# Create Dashboard Charts for L&D Marketing Dashboard
	dashboard_charts = [
		# 1. Lead Status - L&D Marketing (Bar Chart)
		{
			"name": "Lead Status - L&D - Marketing - 90 Days",
			"chart_name": "Lead Status - L&D - 90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "status",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": ld_mrkt_filter_90_days,
		},
		# 2. Opportunity by Stage - L&D Marketing (Donut Chart)
		{
			"name": "Opportunity by Stage - L&D - Marketing",
			"chart_name": "Markt - Opportunity by Stage 90 Days",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "sales_stage",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "=", "Learning & Development"],
				["Opportunity", "source", "in", marketing_sources]
			]),
		},
		# 3. Leads Allocated by BD - L&D Marketing (Donut Chart)
		{
			"name": "Leads Allocated by BD - L&D - Marketing",
			"chart_name": "Markt- Leads allocated by BD 90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "lead_owner",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Learning & Development"],
				["Lead", "source", "in", marketing_sources]
			]),
			"number_of_groups": 10,
		},
		# 4. Lead Source - L&D Marketing (Donut Chart)
		{
			"name": "Lead Source - L&D - Marketing - 90 Days",
			"chart_name": "Markt - Lead source - L&D -90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "source",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": ld_mrkt_filter_90_days,
		},
		# 5. Unqualified Reason - L&D Marketing (Bar Chart)
		{
			"name": "Unqualified Reason - L&D - Marketing",
			"chart_name": "Unqualified Reason - L&D -90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "custom_unqualified_reason",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Learning & Development"],
				["Lead", "source", "in", marketing_sources],
				["Lead", "status", "=", "Do Not Contact"],
				["Lead", "creation", ">=", date_90_days_ago]
			]),
		},
		# 6. Rating - L&D Marketing (Donut Chart)
		{
			"name": "Rating - L&D - Marketing - 90 Days",
			"chart_name": "Rating - L&D - 90 Days",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "custom_rating",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "=", "Learning & Development"],
				["Opportunity", "source", "in", marketing_sources],
				["Opportunity", "status", "in", ["Open", "Quotation"]],
				["Opportunity", "creation", ">=", date_90_days_ago]
			]),
		},
		# 7. Industry - L&D Marketing (Donut Chart)
		{
			"name": "Industry - L&D - Marketing - 90 Days",
			"chart_name": "Markt- Industry- L&D -90",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "industry",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Donut",
			"filters_json": ld_mrkt_filter_90_days,
			"number_of_groups": 15,
		},
		# 8. TAT Todays Date - L&D Marketing (Bar Chart)
		{
			"name": "TAT Todays Date - L&D - Marketing - 90 Days",
			"chart_name": "TAT Todays Date - L&D -90 Days",
			"chart_type": "Count",
			"document_type": "Lead",
			"based_on": "creation",
			"timeseries": 0,
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": ld_mrkt_filter_90_days,
		},
		# 9. Type Of Service - L&D Marketing (Bar Chart)
		{
			"name": "Type Of Service - L&D - Marketing - 90 Days",
			"chart_name": "Type Of Service - L&D - 90 Days",
			"chart_type": "Group By",
			"document_type": "Lead",
			"group_by_type": "Count",
			"group_by_based_on": "custom_sub_vertical",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": ld_mrkt_filter_90_days,
		},
		# 10. Opportunities by Owner - L&D Marketing (Bar Chart)
		{
			"name": "Opportunities by Owner - L&D - Marketing",
			"chart_name": "Opportunities by Owner - L&D - Marketing",
			"chart_type": "Group By",
			"document_type": "Opportunity",
			"group_by_type": "Count",
			"group_by_based_on": "opportunity_owner",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": ld_mrkt_opp_filter_90_days,
			"number_of_groups": 10,
		},
		# 11. L&D Marketing Leads Trend - Last 90 Days (Line Chart)
		{
			"name": "L&D Marketing Leads Trend - 90 Days",
			"chart_name": "L&D Marketing Leads Trend - Last 90 Days",
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
				["Lead", "custom_vertical", "=", "Learning & Development"],
				["Lead", "source", "in", marketing_sources]
			]),
		},
		# 12. L&D Marketing Opportunities Trend - Last 90 Days (Line Chart)
		{
			"name": "L&D Marketing Opportunities Trend - 90 Days",
			"chart_name": "L&D Marketing Opportunities Trend - Last 90 Days",
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
				["Opportunity", "custom_vertical", "=", "Learning & Development"],
				["Opportunity", "source", "in", marketing_sources]
			]),
		},
		# 13. Expected Revenue - L&D Marketing (Bar Chart)
		{
			"name": "Expected Revenue - L&D - Marketing",
			"chart_name": "Expected Revenue - L&D - Marketing",
			"chart_type": "Sum",
			"document_type": "Opportunity",
			"based_on": "party_name",
			"value_based_on": "opportunity_amount",
			"is_public": 1,
			"module": "CRM PP",
			"type": "Bar",
			"filters_json": ld_mrkt_opp_filter_90_days,
			"number_of_groups": 10,
		},
	]

	print("\nCreating Dashboard Charts for L&D Marketing Dashboard...")
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
	dashboard_name = "L&D Leads & Opportunities (Marketing)"
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
						{"card": "Total L&D Leads - Marketing (90 Days)"},
						{"card": "Total L&D Opportunities - Marketing (90 Days)"},
						{"card": "Total L&D Opportunity Value - Marketing (90 Days)"},
						{"card": "L&D Closed Won - Marketing (90 Days)"},
					],
					"charts": [
						{"chart": "Lead Status - L&D - 90 Days", "width": "Half"},
						{"chart": "Markt - Opportunity by Stage 90 Days", "width": "Half"},
						{"chart": "TAT Todays Date - L&D -90 Days", "width": "Half"},
						{"chart": "Unqualified Reason - L&D -90 Days", "width": "Half"},
						{"chart": "Rating - L&D - 90 Days", "width": "Half"},
						{"chart": "Type Of Service - L&D - 90 Days", "width": "Half"},
						{"chart": "Markt- Industry- L&D -90", "width": "Half"},
						{"chart": "Markt- Leads allocated by BD 90 Days", "width": "Half"},
						{"chart": "Markt - Lead source - L&D -90 Days", "width": "Half"},
						{"chart": "Opportunities by Owner - L&D - Marketing", "width": "Half"},
						{"chart": "Expected Revenue - L&D - Marketing", "width": "Half"},
						{"chart": "L&D Marketing Leads Trend - Last 90 Days", "width": "Half"},
						{"chart": "L&D Marketing Opportunities Trend - Last 90 Days", "width": "Half"},
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
	print("\n✅ L&D Marketing Dashboard components created successfully!")
	print(f"\nYou can now access the dashboard at: /app/dashboard-view/{dashboard_name}")


def update_ld_marketing_dashboard():
	"""Update existing L&D Marketing Dashboard to add all charts"""
	dashboard_name = "L&D Leads & Opportunities (Marketing)"
	
	if frappe.db.exists("Dashboard", dashboard_name):
		print(f"Updating dashboard: {dashboard_name}")
		dashboard = frappe.get_doc("Dashboard", dashboard_name)
		
		# Clear existing charts and cards
		dashboard.charts = []
		dashboard.cards = []
		
		# Add number cards
		cards_to_add = [
			"Total L&D Leads - Marketing (90 Days)",
			"Total L&D Opportunities - Marketing (90 Days)",
			"Total L&D Opportunity Value - Marketing (90 Days)",
			"L&D Closed Won - Marketing (90 Days)",
		]
		
		for card_name in cards_to_add:
			if frappe.db.exists("Number Card", card_name):
				dashboard.append("cards", {"card": card_name})
		
		# Add charts
		charts_to_add = [
			("Lead Status - L&D - 90 Days", "Half"),
			("Markt - Opportunity by Stage 90 Days", "Half"),
			("TAT Todays Date - L&D -90 Days", "Half"),
			("Unqualified Reason - L&D -90 Days", "Half"),
			("Rating - L&D - 90 Days", "Half"),
			("Type Of Service - L&D - 90 Days", "Half"),
			("Markt- Industry- L&D -90", "Half"),
			("Markt- Leads allocated by BD 90 Days", "Half"),
			("Markt - Lead source - L&D -90 Days", "Half"),
			("Opportunities by Owner - L&D - Marketing", "Half"),
			("Expected Revenue - L&D - Marketing", "Half"),
			("L&D Marketing Leads Trend - Last 90 Days", "Half"),
			("L&D Marketing Opportunities Trend - Last 90 Days", "Half"),
		]
		
		for chart_name, width in charts_to_add:
			if frappe.db.exists("Dashboard Chart", chart_name):
				dashboard.append("charts", {"chart": chart_name, "width": width})
		
		dashboard.save(ignore_permissions=True)
		frappe.db.commit()
		print("✓ Dashboard updated successfully with all charts")
		print(f"\nYou can now access the dashboard at: /app/dashboard-view/{dashboard_name}")
	else:
		print(f"Dashboard '{dashboard_name}' does not exist. Run create_ld_marketing_dashboard() first.")


def delete_ld_marketing_dashboard():
	"""Delete the L&D Marketing Dashboard and all its components"""
	dashboard_name = "L&D Leads & Opportunities (Marketing)"
	
	# Delete dashboard
	if frappe.db.exists("Dashboard", dashboard_name):
		frappe.delete_doc("Dashboard", dashboard_name, ignore_permissions=True)
		print(f"✓ Deleted Dashboard: {dashboard_name}")
	
	# Delete charts
	charts = [
		"Lead Status - L&D - Marketing - 90 Days",
		"Opportunity by Stage - L&D - Marketing",
		"Leads Allocated by BD - L&D - Marketing",
		"Lead Source - L&D - Marketing - 90 Days",
		"Unqualified Reason - L&D - Marketing",
		"Rating - L&D - Marketing - 90 Days",
		"Industry - L&D - Marketing - 90 Days",
		"TAT Todays Date - L&D - Marketing - 90 Days",
		"Type Of Service - L&D - Marketing - 90 Days",
		"Opportunities by Owner - L&D - Marketing",
		"Expected Revenue - L&D - Marketing",
		"L&D Marketing Leads Trend - 90 Days",
		"L&D Marketing Opportunities Trend - 90 Days",
	]
	
	for chart_name in charts:
		if frappe.db.exists("Dashboard Chart", chart_name):
			frappe.delete_doc("Dashboard Chart", chart_name, ignore_permissions=True)
			print(f"✓ Deleted Dashboard Chart: {chart_name}")
	
	# Delete number cards
	cards = [
		"Total L&D Leads - Marketing (90 Days)",
		"Total L&D Opportunities - Marketing (90 Days)",
		"Total L&D Opportunity Value - Marketing (90 Days)",
		"L&D Closed Won - Marketing (90 Days)",
	]
	
	for card_name in cards:
		if frappe.db.exists("Number Card", card_name):
			frappe.delete_doc("Number Card", card_name, ignore_permissions=True)
			print(f"✓ Deleted Number Card: {card_name}")
	
	frappe.db.commit()
	print("\n✅ All L&D Marketing Dashboard components deleted successfully!")


if __name__ == "__main__":
	create_ld_marketing_dashboard()



