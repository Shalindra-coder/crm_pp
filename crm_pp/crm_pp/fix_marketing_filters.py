import frappe
from frappe.utils import add_days, today
import json


def fix_perm_marketing_filters():
	"""Fix filters in Perm Marketing dashboard charts to use proper JSON format"""
	
	# Calculate date 90 days ago
	date_90_days_ago = add_days(today(), -90)
	date_60_days_ago = add_days(today(), -60)
	
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
		"RAI"
	]
	
	print(f"\n{'='*70}")
	print(f"FIXING PERM MARKETING DASHBOARD FILTERS")
	print(f"{'='*70}\n")
	print(f"Using proper JSON format for marketing sources list")
	print(f"Marketing Sources: {marketing_sources}\n")
	
	# Chart updates with corrected filters
	chart_updates = {
		"(Mrkt) - Lead Status - Perm - 90 Days": {
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Permanent Staffing"],
				["Lead", "source", "in", marketing_sources],
				["Lead", "creation", ">=", date_90_days_ago]
			])
		},
		"(Mrkt) - Opportunity by Stage - Perm": {
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "=", "Permanent Staffing"],
				["Opportunity", "source", "in", marketing_sources]
			])
		},
		"(Mrkt) - Leads Allocated by BD - Perm": {
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Permanent Staffing"],
				["Lead", "source", "in", marketing_sources]
			])
		},
		"(Mrkt) - Perm - 90 Days": {
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Permanent Staffing"],
				["Lead", "source", "in", marketing_sources],
				["Lead", "creation", ">=", date_90_days_ago]
			])
		},
		"Unqualified Reason - Perm - (Mrkt)": {
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Permanent Staffing"],
				["Lead", "source", "in", marketing_sources],
				["Lead", "status", "=", "Do Not Contact"],
				["Lead", "creation", ">=", date_90_days_ago]
			])
		},
		"Industry Wise Leads - Perm - Past 60 Days": {
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Permanent Staffing"],
				["Lead", "source", "in", marketing_sources],
				["Lead", "creation", ">=", date_60_days_ago]
			])
		},
		"Lead Source - Industry - (Mrkt) - 90Days": {
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Permanent Staffing"],
				["Lead", "source", "in", marketing_sources],
				["Lead", "creation", ">=", date_90_days_ago]
			])
		},
		"TAT Todays Date - Perm - 90 Days - (Mrkt)": {
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Permanent Staffing"],
				["Lead", "source", "in", marketing_sources],
				["Lead", "creation", ">=", date_90_days_ago]
			])
		},
		"Salary Offerings - Perm - (Mrkt)": {
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Permanent Staffing"],
				["Lead", "source", "in", marketing_sources],
				["Lead", "creation", ">=", date_90_days_ago]
			])
		},
		"(Mrkt) - Perm Salary Offering": {
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "=", "Permanent Staffing"],
				["Opportunity", "source", "in", marketing_sources],
				["Opportunity", "status", "in", ["Open", "Quotation"]],
				["Opportunity", "creation", ">=", date_90_days_ago]
			])
		},
		"Opportunities by Owner - Perm - Marketing": {
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "=", "Permanent Staffing"],
				["Opportunity", "source", "in", marketing_sources],
				["Opportunity", "creation", ">=", date_90_days_ago]
			])
		},
		"Perm Marketing Leads Trend - Last 90 Days": {
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Permanent Staffing"],
				["Lead", "source", "in", marketing_sources]
			])
		},
		"Perm Marketing Opportunities Trend - Last 90 Days": {
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "=", "Permanent Staffing"],
				["Opportunity", "source", "in", marketing_sources]
			])
		},
	}
	
	# Also update number cards
	card_updates = {
		"Total Perm Leads - Marketing (90 Days)": {
			"filters_json": json.dumps([
				["Lead", "custom_vertical", "=", "Permanent Staffing"],
				["Lead", "source", "in", marketing_sources],
				["Lead", "creation", ">=", date_90_days_ago]
			])
		},
		"Total Perm Opportunities - Marketing (90 Days)": {
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "=", "Permanent Staffing"],
				["Opportunity", "source", "in", marketing_sources],
				["Opportunity", "creation", ">=", date_90_days_ago]
			])
		},
		"Total Perm Opportunity Value - Marketing (90 Days)": {
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "=", "Permanent Staffing"],
				["Opportunity", "source", "in", marketing_sources],
				["Opportunity", "creation", ">=", date_90_days_ago]
			])
		},
		"Perm Closed Won - Marketing (90 Days)": {
			"filters_json": json.dumps([
				["Opportunity", "custom_vertical", "=", "Permanent Staffing"],
				["Opportunity", "source", "in", marketing_sources],
				["Opportunity", "status", "=", "Closed"],
				["Opportunity", "creation", ">=", date_90_days_ago]
			])
		},
	}
	
	updated_count = 0
	
	print("Updating Dashboard Charts:\n")
	for chart_name, updates in chart_updates.items():
		if frappe.db.exists("Dashboard Chart", chart_name):
			chart = frappe.get_doc("Dashboard Chart", chart_name)
			chart.filters_json = updates["filters_json"]
			chart.save(ignore_permissions=True)
			print(f"✅ Updated: {chart_name}")
			updated_count += 1
		else:
			print(f"⚠️  Not found: {chart_name}")
	
	print(f"\n{'='*70}\n")
	print("Updating Number Cards:\n")
	
	for card_name, updates in card_updates.items():
		if frappe.db.exists("Number Card", card_name):
			card = frappe.get_doc("Number Card", card_name)
			card.filters_json = updates["filters_json"]
			card.save(ignore_permissions=True)
			print(f"✅ Updated: {card_name}")
			updated_count += 1
		else:
			print(f"⚠️  Not found: {card_name}")
	
	frappe.db.commit()
	
	print(f"\n{'='*70}")
	print(f"✅ Updated {updated_count} components with proper JSON filters")
	print(f"{'='*70}\n")
	
	print("Marketing sources filter now properly formatted!")
	print("Dashboard should load data correctly now.\n")


if __name__ == "__main__":
	fix_perm_marketing_filters()



