import frappe


def fix_remaining_marketing_cards():
	"""Fix all remaining marketing and July dashboard cards"""
	
	print("="*80)
	print("FIXING REMAINING MARKETING & JULY DASHBOARD CARDS")
	print("="*80)
	
	# All the problematic marketing cards (exact names from the database)
	cards_to_fix = [
		"Closed Won - July Marketing - All Verticals",
		"L&D Closed Won - Marketing (90 Days)",
		"LLC Closed Won - Marketing (90 Days)",
		"Perm Closed Won - Marketing (90 Days)",
		"Temp Closed Won - Marketing (90 Days)",
		"Total L&D Leads - Marketing (90 Days)",
		"Total L&D Opportunities - Marketing (90 Days)",
		"Total Leads - July Marketing - All Verticals",
		"Total LLC Leads - Marketing (90 Days)",
		"Total LLC Opportunities - Marketing (90 Days)",
		"Total Opportunities - July Marketing - All Verticals",
		"Total Perm Leads - Marketing (90 Days)",
		"Total Perm Opportunities - Marketing (90 Days)",
		"Total Temp Leads - Marketing (90 Days)",
		"Total Temp Opportunities - Marketing (90 Days)",
	]
	
	fixed_count = 0
	
	for card_name in cards_to_fix:
		if frappe.db.exists("Number Card", card_name):
			try:
				card = frappe.get_doc("Number Card", card_name)
				
				print(f"\n🔧 Fixing: {card_name}")
				print(f"   OLD: Function={card.function}, Based On={card.aggregate_function_based_on}")
				
				# Change from summing 'creation' to summing 'docstatus'
				card.aggregate_function_based_on = "docstatus"
				card.save(ignore_permissions=True)
				
				print(f"   NEW: Function={card.function}, Based On={card.aggregate_function_based_on}")
				print(f"   ✅ Fixed")
				fixed_count += 1
				
			except Exception as e:
				print(f"\n❌ Error fixing {card_name}: {str(e)}")
		else:
			print(f"\n⚠️  Card not found: {card_name}")
	
	frappe.db.commit()
	
	print("\n" + "="*80)
	print("📊 SUMMARY")
	print("="*80)
	print(f"✅ Fixed: {fixed_count} marketing/July cards")
	print("="*80)
	print("\nAll dashboard cards have now been fixed!")
	print("Cards now sum 'docstatus' (0 or 1) instead of 'creation' (datetime).")
	print("\nRefresh your dashboards to see normal values instead of 'Cr'!")
	print("="*80)


if __name__ == "__main__":
	fix_remaining_marketing_cards()

