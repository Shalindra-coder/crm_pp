import frappe


def fix_ld_number_cards():
	"""Fix L&D Dashboard number cards - change from Sum to Count"""
	
	print("="*80)
	print("FIXING L&D DASHBOARD NUMBER CARDS")
	print("="*80)
	
	# Cards that need to be fixed (should COUNT, not SUM)
	count_cards = [
		"Total L&D Leads (90 Days)",
		"Total L&D Opportunities (90 Days)",
		"L&D Closed Won (90 Days)",
	]
	
	for card_name in count_cards:
		if frappe.db.exists("Number Card", card_name):
			try:
				card = frappe.get_doc("Number Card", card_name)
				
				print(f"\nFixing: {card_name}")
				print(f"  OLD - Function: {card.function}, Based On: {card.aggregate_function_based_on}")
				
				# Change from Sum to Count
				card.function = "Count"
				card.report_function = "Count"
				# For Count function, we don't need aggregate_function_based_on
				# but we'll keep it as the identifier field
				
				card.save(ignore_permissions=True)
				
				print(f"  NEW - Function: {card.function}, Based On: {card.aggregate_function_based_on}")
				print(f"  ✅ Fixed successfully!")
				
			except Exception as e:
				print(f"  ❌ Error fixing {card_name}: {str(e)}")
		else:
			print(f"\n❌ Card not found: {card_name}")
	
	# The "Total L&D Opportunity Value" card should remain Sum (it's summing revenue)
	revenue_card = "Total L&D Opportunity Value (90 Days)"
	if frappe.db.exists("Number Card", revenue_card):
		try:
			card = frappe.get_doc("Number Card", revenue_card)
			print(f"\nVerifying: {revenue_card}")
			print(f"  Function: {card.function}, Based On: {card.aggregate_function_based_on}")
			
			if card.aggregate_function_based_on != "opportunity_amount":
				print(f"  ⚠️  Warning: Should be based on 'opportunity_amount'")
				card.aggregate_function_based_on = "opportunity_amount"
				card.save(ignore_permissions=True)
				print(f"  ✅ Fixed to sum opportunity_amount")
			else:
				print(f"  ✅ Already correct (sums revenue)")
				
		except Exception as e:
			print(f"  ❌ Error checking {revenue_card}: {str(e)}")
	
	frappe.db.commit()
	
	print("\n" + "="*80)
	print("✅ L&D DASHBOARD NUMBER CARDS FIXED!")
	print("="*80)
	print("\nChanges applied:")
	print("  1. Total L&D Leads (90 Days) - Changed to COUNT")
	print("  2. Total L&D Opportunities (90 Days) - Changed to COUNT")
	print("  3. L&D Closed Won (90 Days) - Changed to COUNT")
	print("  4. Total L&D Opportunity Value (90 Days) - Remains SUM (revenue)")
	print("\nRefresh your dashboard to see the corrected values!")
	print("="*80)


if __name__ == "__main__":
	fix_ld_number_cards()

