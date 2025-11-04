import frappe
from frappe.utils import add_days, today, formatdate
import json


def fix_perm_dashboard_date_filters():
	"""Fix all Perm dashboard charts and cards to use proper dd-mm-yyyy date format"""
	
	# Calculate date 90 days ago in YYYY-MM-DD format (ISO format for Frappe)
	date_90_days_ago = add_days(today(), -90)  # Returns in YYYY-MM-DD format
	
	print(f"\n{'='*70}")
	print(f"FIXING PERM DASHBOARD DATE FILTERS")
	print(f"{'='*70}\n")
	print(f"Using date: {date_90_days_ago} (90 days ago from {today()})\n")
	print(f"Note: Using YYYY-MM-DD format as required by Frappe filters\n")
	
	# Get all Perm dashboard charts
	charts = frappe.db.get_list(
		"Dashboard Chart",
		filters={"name": ["like", "%Perm%"]},
		fields=["name"]
	)
	
	updated_count = 0
	skipped_count = 0
	
	print("Updating Dashboard Charts:\n")
	
	for chart_info in charts:
		chart = frappe.get_doc("Dashboard Chart", chart_info.name)
		
		if chart.filters_json:
			# Parse the filters
			filters = json.loads(chart.filters_json)
			
			# Update any date filters (check for both "90 days ago" and dd-mm-yyyy format)
			updated = False
			for filter_item in filters:
				if len(filter_item) >= 4:
					old_value = filter_item[3]
					# Check if it's a date-related filter that needs updating
					if old_value == "90 days ago" or (isinstance(old_value, str) and "-" in old_value and len(old_value) == 10):
						# Check if it's not already in YYYY-MM-DD format
						if old_value != date_90_days_ago:
							filter_item[3] = date_90_days_ago
							updated = True
			
			if updated:
				# Save the updated filters
				chart.filters_json = json.dumps(filters)
				chart.save(ignore_permissions=True)
				print(f"✅ Updated: {chart.name}")
				updated_count += 1
			else:
				skipped_count += 1
		else:
			skipped_count += 1
	
	# Get all Perm number cards
	print(f"\n{'='*70}\n")
	print("Updating Number Cards:\n")
	
	cards = frappe.db.get_list(
		"Number Card",
		filters={"name": ["like", "%Perm%"]},
		fields=["name"]
	)
	
	for card_info in cards:
		card = frappe.get_doc("Number Card", card_info.name)
		
		if card.filters_json:
			# Parse the filters
			filters = json.loads(card.filters_json)
			
			# Update any date filters (check for both "90 days ago" and dd-mm-yyyy format)
			updated = False
			for filter_item in filters:
				if len(filter_item) >= 4:
					old_value = filter_item[3]
					# Check if it's a date-related filter that needs updating
					if old_value == "90 days ago" or (isinstance(old_value, str) and "-" in old_value and len(old_value) == 10):
						# Check if it's not already in YYYY-MM-DD format
						if old_value != date_90_days_ago:
							filter_item[3] = date_90_days_ago
							updated = True
			
			if updated:
				# Save the updated filters
				card.filters_json = json.dumps(filters)
				card.save(ignore_permissions=True)
				print(f"✅ Updated: {card.name}")
				updated_count += 1
			else:
				skipped_count += 1
		else:
			skipped_count += 1
	
	frappe.db.commit()
	
	print(f"\n{'='*70}")
	print(f"✅ Updated {updated_count} components")
	print(f"⚠️  Skipped {skipped_count} components (already using correct format)")
	print(f"{'='*70}\n")


if __name__ == "__main__":
	fix_perm_dashboard_date_filters()

