import frappe


def verify_perm_dashboard():
	"""Verify the Perm Dashboard and its components"""
	dashboard_name = "Perm Leads & Opportunities (All Source)"
	
	print(f"\n{'='*70}")
	print(f"VERIFICATION: {dashboard_name}")
	print(f"{'='*70}\n")
	
	# Check if dashboard exists
	if not frappe.db.exists("Dashboard", dashboard_name):
		print("❌ Dashboard does not exist!")
		return
	
	print("✅ Dashboard exists")
	
	# Get dashboard details
	dashboard = frappe.get_doc("Dashboard", dashboard_name)
	
	# Check number cards
	print(f"\n📊 Number Cards ({len(dashboard.cards)}):")
	for card in dashboard.cards:
		card_exists = frappe.db.exists("Number Card", card.card)
		status = "✅" if card_exists else "❌"
		print(f"  {status} {card.card}")
	
	# Check charts
	print(f"\n📈 Charts ({len(dashboard.charts)}):")
	for chart in dashboard.charts:
		chart_exists = frappe.db.exists("Dashboard Chart", chart.chart)
		status = "✅" if chart_exists else "❌"
		print(f"  {status} {chart.chart} ({chart.width})")
	
	# List all available Perm dashboard charts
	print(f"\n📋 All Available Perm Dashboard Charts:")
	all_charts = frappe.db.get_list(
		"Dashboard Chart",
		filters={
			"name": ["like", "%Perm%"]
		},
		fields=["name", "chart_type", "document_type"]
	)
	
	for chart in all_charts:
		in_dashboard = any(c.chart == chart.name for c in dashboard.charts)
		status = "✅" if in_dashboard else "⚠️ "
		print(f"  {status} {chart.name} ({chart.chart_type} - {chart.document_type})")
	
	# List all available Perm number cards
	print(f"\n📋 All Available Perm Number Cards:")
	all_cards = frappe.db.get_list(
		"Number Card",
		filters={
			"name": ["like", "%Perm%"]
		},
		fields=["name", "label"]
	)
	
	for card in all_cards:
		in_dashboard = any(c.card == card.name for c in dashboard.cards)
		status = "✅" if in_dashboard else "⚠️ "
		print(f"  {status} {card.name}")
	
	print(f"\n{'='*70}")
	print(f"Dashboard URL: /app/dashboard-view/{dashboard_name}")
	print(f"{'='*70}\n")


if __name__ == "__main__":
	verify_perm_dashboard()



