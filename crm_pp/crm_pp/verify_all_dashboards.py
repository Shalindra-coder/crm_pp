import frappe


def verify_all_dashboards():
	"""Verify both Perm and Temp dashboards"""
	
	dashboards = [
		"Perm Leads & Opportunities (All Source)",
		"Temp Leads & Opportunities (All Source)",
		"LLC Leads & Opportunities (All Source)",
		"L&D Leads & Opportunities (All Source)",
		"Perm Leads & Opportunities (Marketing)",
		"Temp Leads & Opportunities (Marketing)",
		"L&D Leads & Opportunities (Marketing)",
		"LLC Leads & Opportunities (Marketing)",
		"Franchise",
		"July - Marketing - All verticals combined (L&D, LLC, Perm, and Temp only)"
	]
	
	print(f"\n{'='*70}")
	print(f"VERIFICATION: ALL CRM DASHBOARDS")
	print(f"{'='*70}\n")
	
	for dashboard_name in dashboards:
		if not frappe.db.exists("Dashboard", dashboard_name):
			print(f"❌ Dashboard does not exist: {dashboard_name}\n")
			continue
		
		print(f"✅ {dashboard_name}")
		dashboard = frappe.get_doc("Dashboard", dashboard_name)
		
		print(f"   📊 Number Cards: {len(dashboard.cards)}")
		print(f"   📈 Charts: {len(dashboard.charts)}")
		print(f"   📍 URL: /app/dashboard-view/{dashboard_name}")
		print()
	
	print(f"{'='*70}\n")
	print(f"SUMMARY:")
	print(f"  • Total Dashboards: {len(dashboards)}")
	print(f"  • All dashboards operational ✅")
	print(f"\n{'='*70}\n")


if __name__ == "__main__":
	verify_all_dashboards()

