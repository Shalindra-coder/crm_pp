import frappe


def find_marketing_cards():
	"""Find all marketing-related number cards"""
	
	print("="*80)
	print("FINDING MARKETING & JULY DASHBOARD CARDS")
	print("="*80)
	
	# Search for marketing cards
	marketing_cards = frappe.db.sql("""
		SELECT name, label, function, aggregate_function_based_on, document_type
		FROM `tabNumber Card`
		WHERE name LIKE '%Marketing%' 
		   OR name LIKE '%Mrkt%' 
		   OR name LIKE '%July%'
		ORDER BY name
	""", as_dict=1)
	
	print(f"\nFound {len(marketing_cards)} cards:\n")
	
	for card in marketing_cards:
		print(f"Name: {card.name}")
		print(f"  Label: {card.label}")
		print(f"  DocType: {card.document_type}")
		print(f"  Function: {card.function}")
		print(f"  Based On: {card.aggregate_function_based_on}")
		print()
	
	# Also find all cards that need fixing
	problematic_cards = frappe.db.sql("""
		SELECT name, label, function, aggregate_function_based_on
		FROM `tabNumber Card`
		WHERE function = 'Sum' 
		  AND aggregate_function_based_on IN ('creation', 'modified')
		ORDER BY name
	""", as_dict=1)
	
	print("="*80)
	print(f"ALL PROBLEMATIC CARDS (Sum on datetime): {len(problematic_cards)}")
	print("="*80)
	
	for card in problematic_cards:
		print(f"- {card.name} (Based on: {card.aggregate_function_based_on})")
	
	print("\n" + "="*80)


if __name__ == "__main__":
	find_marketing_cards()

