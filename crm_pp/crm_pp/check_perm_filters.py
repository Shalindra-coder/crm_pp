import frappe
from frappe.utils import add_days, today, formatdate
import json


def check_perm_dashboard_filters():
	"""Check the date filters being used in Perm dashboard charts"""
	
	# Calculate date 90 days ago in YYYY-MM-DD format (ISO format for Frappe)
	date_90_days_ago = add_days(today(), -90)  # Returns in YYYY-MM-DD format
	
	print(f"\n{'='*70}")
	print(f"PERM DASHBOARD DATE FILTER CHECK")
	print(f"{'='*70}\n")
	print(f"Today's Date: {today()} (YYYY-MM-DD)")
	print(f"90 Days Ago:  {date_90_days_ago} (YYYY-MM-DD)")
	print(f"\nNote: Frappe filters require YYYY-MM-DD format (ISO 8601)")
	print(f"\n{'='*70}\n")
	
	# Check a few charts to see their filters
	charts_to_check = [
		"Lead Status - Perm - 90 Days",
		"Unqualified Reason - Perm - 90 Days",
		"Rating - Perm - Past 90 Days (Pipeline)",
	]
	
	print("Sample Chart Filters:\n")
	for chart_name in charts_to_check:
		if frappe.db.exists("Dashboard Chart", chart_name):
			chart = frappe.get_doc("Dashboard Chart", chart_name)
			print(f"📊 {chart_name}")
			print(f"   Document Type: {chart.document_type}")
			if chart.filters_json:
				filters = json.loads(chart.filters_json)
				print(f"   Filters:")
				for filter_item in filters:
					print(f"      • {filter_item}")
			print()
	
	# Check number cards
	print(f"\n{'='*70}\n")
	print("Sample Number Card Filters:\n")
	
	cards_to_check = [
		"Total Perm Leads (90 Days)",
		"Perm Closed Won (90 Days)",
	]
	
	for card_name in cards_to_check:
		if frappe.db.exists("Number Card", card_name):
			card = frappe.get_doc("Number Card", card_name)
			print(f"📈 {card_name}")
			print(f"   Document Type: {card.document_type}")
			if card.filters_json:
				filters = json.loads(card.filters_json)
				print(f"   Filters:")
				for filter_item in filters:
					print(f"      • {filter_item}")
			print()
	
	print(f"{'='*70}\n")
	print("✅ All filters should be using YYYY-MM-DD format (ISO 8601)")
	print(f"{'='*70}\n")


if __name__ == "__main__":
	check_perm_dashboard_filters()

