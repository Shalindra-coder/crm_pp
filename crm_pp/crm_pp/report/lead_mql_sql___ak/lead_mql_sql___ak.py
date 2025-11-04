import frappe
from frappe import _


def execute(filters=None):
	"""Execute the Lead MQL SQL - AK report"""
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	"""Define report columns matching the screenshot"""
	return [
		{
			"fieldname": "status",
			"label": _("Lead Status"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "custom_vertical",
			"label": _("Vertical"),
			"fieldtype": "Link",
			"options": "Vertical",
			"width": 150
		},
		{
			"fieldname": "lead_owner",
			"label": _("Lead Owner"),
			"fieldtype": "Link",
			"options": "User",
			"width": 150
		},
		{
			"fieldname": "first_name",
			"label": _("First Name"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "last_name",
			"label": _("Last Name"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "job_title",
			"label": _("Designation"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "campaign_name",
			"label": _("Campaign Name"),
			"fieldtype": "Link",
			"options": "Campaign",
			"width": 150
		},
		{
			"fieldname": "custom_unqualified_reason",
			"label": _("Unqualified Reason"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "source",
			"label": _("Lead Source"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "industry",
			"label": _("Industry"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "phone",
			"label": _("Phone"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "website",
			"label": _("Website"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "creation",
			"label": _("Create Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "company_name",
			"label": _("Company / Account"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "modified",
			"label": _("Last Modified"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "custom_hr_experience",
			"label": _("HR Experience"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "city",
			"label": _("City"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "custom_rating",
			"label": _("Rating"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "custom_description",
			"label": _("Description"),
			"fieldtype": "Text",
			"width": 300
		},
		{
			"fieldname": "custom_salary_offering",
			"label": _("Salary Offerings"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "mobile_no",
			"label": _("Mobile"),
			"fieldtype": "Data",
			"width": 130
		},
	]


def get_data(filters):
	"""Get lead data based on filters"""
	
	conditions = get_conditions(filters)
	
	data = frappe.db.sql("""
		SELECT
			status,
			custom_vertical,
			lead_owner,
			first_name,
			last_name,
			job_title,
			campaign_name,
			custom_unqualified_reason,
			source,
			industry,
			phone,
			website,
			DATE(creation) as creation,
			company_name,
			DATE(modified) as modified,
			custom_hr_experience,
			city,
			custom_rating,
			custom_description,
			custom_salary_offering,
			mobile_no
		FROM
			`tabLead`
		WHERE
			docstatus < 2
			{conditions}
		ORDER BY
			lead_owner ASC, creation DESC
	""".format(conditions=conditions), filters, as_dict=1)
	
	return data


def get_conditions(filters):
	"""Build filter conditions"""
	conditions = []
	
	if filters.get("lead_owner"):
		conditions.append("AND lead_owner = %(lead_owner)s")
	
	if filters.get("status"):
		conditions.append("AND status = %(status)s")
	
	if filters.get("custom_vertical"):
		conditions.append("AND custom_vertical = %(custom_vertical)s")
	
	if filters.get("source"):
		conditions.append("AND source = %(source)s")
	
	if filters.get("from_date"):
		conditions.append("AND DATE(creation) >= %(from_date)s")
	
	if filters.get("to_date"):
		conditions.append("AND DATE(creation) <= %(to_date)s")
	
	if filters.get("industry"):
		conditions.append("AND industry = %(industry)s")
	
	if filters.get("city"):
		conditions.append("AND city = %(city)s")
	
	if filters.get("custom_rating"):
		conditions.append("AND custom_rating = %(custom_rating)s")
	
	return " ".join(conditions) if conditions else ""

