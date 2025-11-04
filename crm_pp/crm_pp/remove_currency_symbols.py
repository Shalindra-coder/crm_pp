import frappe


def remove_currency_from_all_dashboards():
	"""Remove currency symbols from all Perm, Temp, and LLC dashboard charts"""
	
	print(f"\n{'='*70}")
	print(f"REMOVING CURRENCY SYMBOLS FROM DASHBOARD CHARTS")
	print(f"{'='*70}\n")
	
	# Get all dashboard charts for all dashboards
	chart_patterns = [
		"%Perm%",
		"%Temp%",
		"%LLC%",
		"%L&D%",
		"%Mrkt%",
		"%Marketing%",
		"%Franchise%",
		"%July%"
	]
	
	updated_count = 0
	skipped_count = 0
	
	for pattern in chart_patterns:
		charts = frappe.db.get_list(
			"Dashboard Chart",
			filters={"name": ["like", pattern]},
			fields=["name"]
		)
		
		print(f"Processing charts matching '{pattern}':\n")
		
		for chart_info in charts:
			chart = frappe.get_doc("Dashboard Chart", chart_info.name)
			
			# Check if chart has currency set
			if chart.currency:
				chart.currency = None
				chart.save(ignore_permissions=True)
				print(f"✅ Removed currency from: {chart.name}")
				updated_count += 1
			else:
				skipped_count += 1
	
	# Also update number cards to remove currency
	print(f"\n{'='*70}\n")
	print(f"Processing Number Cards:\n")
	
	card_patterns = [
		"%Perm%",
		"%Temp%",
		"%LLC%",
		"%L&D%",
		"%Marketing%",
		"%Franchise%",
		"%July%"
	]
	
	for pattern in card_patterns:
		cards = frappe.db.get_list(
			"Number Card",
			filters={"name": ["like", pattern]},
			fields=["name"]
		)
		
		for card_info in cards:
			card = frappe.get_doc("Number Card", card_info.name)
			
			# Remove currency from number cards if they're showing values
			if hasattr(card, 'currency') and card.currency:
				card.currency = None
				card.save(ignore_permissions=True)
				print(f"✅ Removed currency from: {card.name}")
				updated_count += 1
			else:
				skipped_count += 1
	
	frappe.db.commit()
	
	print(f"\n{'='*70}")
	print(f"✅ Updated {updated_count} components")
	print(f"⚠️  Skipped {skipped_count} components (no currency set)")
	print(f"{'='*70}\n")
	
	print("✅ Currency symbols removed from all dashboards!")
	print("\nPlease refresh your dashboards to see the changes.\n")


if __name__ == "__main__":
	remove_currency_from_all_dashboards()

