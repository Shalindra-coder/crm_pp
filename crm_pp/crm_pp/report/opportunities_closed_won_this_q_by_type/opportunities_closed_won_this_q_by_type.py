# Copyright (c) 2025, Prompt Personnel and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import formatdate, get_first_day, get_last_day, add_months, getdate


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	
	# Calculate summary statistics
	summary = get_summary(data)
	
	# Add grouping by Opportunity Record Type
	chart = get_chart_data(data)
	
	return columns, data, None, chart, summary


def get_columns():
	"""Define report columns"""
	return [
		{
			"fieldname": "opportunity_name",
			"label": _("Opportunity Name"),
			"fieldtype": "Link",
			"options": "Opportunity",
			"width": 220
		},
		{
			"fieldname": "custom_vertical",
			"label": _("Opportunity Record Type"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "opportunity_owner",
			"label": _("Opportunity Owner"),
			"fieldtype": "Link",
			"options": "User",
			"width": 150
		},
		{
			"fieldname": "primary_contact",
			"label": _("Primary Contact"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "contact_email",
			"label": _("Contact: Email"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "actual_revenue_yearly",
			"label": _("Actual Revenue (Yearly)"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "expected_revenue_yearly",
			"label": _("Expected Revenue (Yearly)"),
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"fieldname": "actual_revenue",
			"label": _("Actual Revenue"),
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"fieldname": "expected_revenue",
			"label": _("Expected Revenue"),
			"fieldtype": "Currency",
			"width": 130
		},
		{
			"fieldname": "source",
			"label": _("Lead Source"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "created_date",
			"label": _("Created Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "close_date",
			"label": _("Close Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "stage",
			"label": _("Stage"),
			"fieldtype": "Data",
			"width": 110
		},
		{
			"fieldname": "vertical",
			"label": _("Vertical"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "custom_requirement_details",
			"label": _("Requirements Details"),
			"fieldtype": "Text",
			"width": 300
		},
		{
			"fieldname": "owner_mobile",
			"label": _("Opportunity Owner: Mobile Phone"),
			"fieldtype": "Data",
			"width": 140
		},
		{
			"fieldname": "contact_phone",
			"label": _("Contact: Phone"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "contact_active",
			"label": _("Active"),
			"fieldtype": "Check",
			"width": 80
		},
		{
			"fieldname": "contact_number",
			"label": _("Contact Number"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "industry",
			"label": _("Industry"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "account_created_date",
			"label": _("Account: Created Date"),
			"fieldtype": "Date",
			"width": 120
		},
		{
			"fieldname": "delivery_manager",
			"label": _("Delivery Manager"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "salary_band",
			"label": _("Salary Band"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "salary_range",
			"label": _("Salary Range"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "owner_active",
			"label": _("Opportunity Owner: Active"),
			"fieldtype": "Check",
			"width": 90
		},
		{
			"fieldname": "account_name",
			"label": _("Account Name"),
			"fieldtype": "Link",
			"options": "Lead",
			"width": 220
		},
		{
			"fieldname": "opportunity_type",
			"label": _("Type"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "services",
			"label": _("Services"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "lost_reason",
			"label": _("Lost Reason"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "inactive_reason",
			"label": _("Inactive Reason"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "phone",
			"label": _("Phone"),
			"fieldtype": "Data",
			"width": 120
		}
	]


def get_data(filters):
	"""Get opportunity data based on filters"""
	
	conditions = get_conditions(filters)
	
	# Calculate date range for yearly projection
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	
	# Calculate number of days in the filter range
	days_in_range = 365  # Default to 365 if no date filter
	if from_date and to_date:
		from frappe.utils import date_diff, getdate
		days_in_range = date_diff(to_date, from_date) + 1  # +1 to include both dates
		if days_in_range <= 0:
			days_in_range = 365
	
	# Calculate projection multiplier (365 days / filter days)
	yearly_multiplier = 365.0 / days_in_range
	
	# SQL query to get all opportunity data
	data = frappe.db.sql("""
		SELECT
			o.name as opportunity_name,
			o.custom_vertical as custom_vertical,
			o.opportunity_owner,
			o.contact_person as primary_contact,
			o.contact_email,
			COALESCE(o.custom_actual_revenue, 0) as actual_revenue,
			COALESCE(o.opportunity_amount, 0) as expected_revenue,
			o.custom_lead_source as source,
			DATE(o.creation) as created_date,
			o.custom_close_date as close_date,
			o.status as stage,
			o.custom_vertical as vertical,
			o.custom_requirement_details as custom_requirement_details,
			(SELECT mobile_no FROM `tabUser` WHERE name = o.opportunity_owner LIMIT 1) as owner_mobile,
			o.contact_mobile as contact_phone,
			COALESCE(o.custom_client_status, 0) as contact_active,
			o.contact_mobile as contact_number,
			o.industry,
			(SELECT DATE(creation) FROM `tabLead` WHERE name = o.party_name LIMIT 1) as account_created_date,
			o.custom_delivery_manager as delivery_manager,
			o.custom_salary_band as salary_band,
			o.custom_salary_range as salary_range,
			(SELECT enabled FROM `tabUser` WHERE name = o.opportunity_owner LIMIT 1) as owner_active,
			o.party_name as account_name,
			o.opportunity_type,
			o.custom_services as services,
			o.custom_lost_reason as lost_reason,
			o.custom_inactive_reason as inactive_reason,
			o.phone
		FROM
			`tabOpportunity` o
	WHERE
		o.docstatus < 2
		{conditions}
	ORDER BY
		o.custom_vertical ASC, o.opportunity_owner ASC, o.creation DESC
	""".format(conditions=conditions), filters, as_dict=1)
	
	# Calculate yearly projected values for each row
	for row in data:
		# Get the main revenue values (for the filtered period)
		actual_revenue = row.get("actual_revenue") or 0
		expected_revenue = row.get("expected_revenue") or 0
		
		# Calculate yearly projected values
		row["actual_revenue_yearly"] = actual_revenue * yearly_multiplier
		row["expected_revenue_yearly"] = expected_revenue * yearly_multiplier
	
	return data


def get_conditions(filters):
	"""Build SQL conditions from filters"""
	conditions = []
	
	# Default filter: Closed Won stage
	if filters.get("stage"):
		conditions.append("AND o.status = %(stage)s")
	else:
		conditions.append("AND o.status = 'Closed Won'")
	
	# Date range filter
	if filters.get("from_date"):
		conditions.append("AND DATE(o.creation) >= %(from_date)s")
	if filters.get("to_date"):
		conditions.append("AND DATE(o.creation) <= %(to_date)s")
	
	# Opportunity Record Type filter
	if filters.get("opportunity_record_type"):
		conditions.append("AND o.custom_vertical = %(opportunity_record_type)s")
	
	# Vertical filter
	if filters.get("vertical"):
		conditions.append("AND o.custom_vertical = %(vertical)s")
	
	# Opportunity Owner filter
	if filters.get("opportunity_owner"):
		conditions.append("AND o.opportunity_owner = %(opportunity_owner)s")
	
	# Lead Source filter
	if filters.get("lead_source"):
		conditions.append("AND o.source = %(lead_source)s")
	
	# Industry filter
	if filters.get("industry"):
		conditions.append("AND o.industry = %(industry)s")
	
	# Opportunity Type filter
	if filters.get("opportunity_type"):
		conditions.append("AND o.opportunity_type = %(opportunity_type)s")
	
	return " ".join(conditions)


def get_summary(data):
	"""Calculate summary statistics"""
	if not data:
		return []
	
	total_records = len(data)
	total_actual_revenue_yearly = sum(row.get("actual_revenue_yearly", 0) or 0 for row in data)
	total_expected_revenue_yearly = sum(row.get("expected_revenue_yearly", 0) or 0 for row in data)
	total_actual_revenue = sum(row.get("actual_revenue", 0) or 0 for row in data)
	total_expected_revenue = sum(row.get("expected_revenue", 0) or 0 for row in data)
	total_active = sum(1 for row in data if row.get("contact_active"))
	total_owner_active = sum(1 for row in data if row.get("owner_active"))
	
	return [
		{
			"value": total_records,
			"indicator": "Blue",
			"label": _("Total Records"),
			"datatype": "Int"
		},
		{
			"value": total_actual_revenue_yearly,
			"indicator": "Green" if total_actual_revenue_yearly > 0 else "Red",
			"label": _("Total Actual Revenue (Yearly)"),
			"datatype": "Currency"
		},
		{
			"value": total_expected_revenue_yearly,
			"indicator": "Blue",
			"label": _("Total Expected Revenue (Yearly)"),
			"datatype": "Currency"
		},
		{
			"value": total_actual_revenue,
			"indicator": "Green" if total_actual_revenue > 0 else "Red",
			"label": _("Total Actual Revenue"),
			"datatype": "Currency"
		},
		{
			"value": total_expected_revenue,
			"indicator": "Blue",
			"label": _("Total Expected Revenue"),
			"datatype": "Currency"
		},
		{
			"value": total_active,
			"indicator": "Green",
			"label": _("Total Active"),
			"datatype": "Int"
		},
		{
			"value": total_owner_active,
			"indicator": "Green",
			"label": _("Total Opportunity Owner: Active"),
			"datatype": "Int"
		}
	]


def get_chart_data(data):
	"""Generate chart data grouped by Opportunity Record Type"""
	if not data:
		return None
	
	# Group by Opportunity Record Type
	type_data = {}
	for row in data:
		record_type = row.get("custom_vertical") or "Not Specified"
		if record_type not in type_data:
			type_data[record_type] = {
				"count": 0,
				"expected_revenue": 0
			}
		type_data[record_type]["count"] += 1
		type_data[record_type]["expected_revenue"] += (row.get("expected_revenue", 0) or 0)
	
	return {
		"data": {
			"labels": list(type_data.keys()),
			"datasets": [
				{
					"name": "Count",
					"values": [type_data[k]["count"] for k in type_data.keys()]
				},
				{
					"name": "Expected Revenue",
					"values": [type_data[k]["expected_revenue"] for k in type_data.keys()]
				}
			]
		},
		"type": "bar",
		"colors": ["#7CD6FD", "#743ee2"]
	}

