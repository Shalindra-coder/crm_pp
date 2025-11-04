import frappe
from frappe import _
from frappe.utils import getdate, today, date_diff


def execute(filters=None):
	"""Execute the Daily Leads Report-Shreya"""
	columns = get_columns()
	data = get_data(filters)
	chart = None
	summary = get_summary(data)
	
	return columns, data, None, chart, summary


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
			"fieldname": "lead_owner_alias",
			"label": _("Lead Owner Alias"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "creation",
			"label": _("Create Date"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "modified",
			"label": _("Last Modified"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "created_month",
			"label": _("Created Month"),
			"fieldtype": "Date",
			"width": 110
		},
		{
			"fieldname": "check_lead_modified",
			"label": _("Check for lead last modified date"),
			"fieldtype": "Check",
			"width": 200
		},
		{
			"fieldname": "owner",
			"label": _("Created By"),
			"fieldtype": "Link",
			"options": "User",
			"width": 150
		},
		{
			"fieldname": "job_title",
			"label": _("Designation"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "company_name",
			"label": _("Company / Account"),
			"fieldtype": "Data",
			"width": 250
		},
		{
			"fieldname": "custom_rating",
			"label": _("Rating"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "website",
			"label": _("Website"),
			"fieldtype": "Data",
			"width": 250
		},
		{
			"fieldname": "email_id",
			"label": _("Email"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "custom_vertical",
			"label": _("Vertical"),
			"fieldtype": "Link",
			"options": "Vertical",
			"width": 200
		},
		{
			"fieldname": "custom_sub_vertical",
			"label": _("Sub Vertical"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "custom_employee_referral_name",
			"label": _("Employee Referral Name"),
			"fieldtype": "Data",
			"width": 180
		},
		{
			"fieldname": "lead_owner",
			"label": _("Lead Owner"),
			"fieldtype": "Link",
			"options": "User",
			"width": 150
		},
		{
			"fieldname": "custom_description",
			"label": _("Description"),
			"fieldtype": "Text",
			"width": 300
		},
		{
			"fieldname": "mobile_no",
			"label": _("Mobile"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "phone",
			"label": _("Phone"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "industry",
			"label": _("Industry"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "state",
			"label": _("State/Province"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "country",
			"label": _("Country"),
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "custom_street",
			"label": _("Street"),
			"fieldtype": "Data",
			"width": 300
		},
		{
			"fieldname": "custom_unqualified_reason",
			"label": _("Unqualified Reason"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "custom_salary_offering",
			"label": _("Salary Offerings"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "source",
			"label": _("Lead Source"),
			"fieldtype": "Data",
			"width": 150
		},
	]


def get_data(filters):
	"""Get lead data based on filters"""
	
	conditions = get_conditions(filters)
	
	# SQL query to get all lead data with calculated fields
	data = frappe.db.sql("""
		SELECT
			status,
			first_name,
			last_name,
			SUBSTRING_INDEX(lead_owner, '@', 1) as lead_owner_alias,
		DATE(creation) as creation,
		DATE(modified) as modified,
		DATE_FORMAT(creation, '%%01/%%m/%%Y') as created_month,
		CASE
				WHEN DATEDIFF(CURDATE(), DATE(modified)) > 30 THEN 1
				ELSE 0
			END as check_lead_modified,
			owner,
			job_title,
			company_name,
			custom_rating,
			website,
			email_id,
			custom_vertical,
			custom_sub_vertical,
			custom_employee_referral_name,
			lead_owner,
			custom_description,
			mobile_no,
			phone,
			industry,
			state,
			country,
			custom_street,
			custom_unqualified_reason,
			custom_salary_offering,
			source
		FROM
			`tabLead`
		WHERE
			docstatus < 2
			{conditions}
		ORDER BY
			status ASC, first_name ASC, last_name ASC, creation DESC
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
	
	if filters.get("campaign_name"):
		conditions.append("AND campaign_name = %(campaign_name)s")
	
	if filters.get("owner"):
		conditions.append("AND owner = %(owner)s")
	
	if filters.get("country"):
		conditions.append("AND country = %(country)s")
	
	if filters.get("state"):
		conditions.append("AND state = %(state)s")
	
	return " ".join(conditions) if conditions else ""


def get_summary(data):
	"""Get summary statistics for the report"""
	if not data:
		return []
	
	total_records = len(data)
	total_check_modified = sum([row.get("check_lead_modified") or 0 for row in data])
	
	return [
		{
			"value": total_records,
			"indicator": "Blue",
			"label": _("Total Records"),
			"datatype": "Int"
		},
		{
			"value": total_check_modified,
			"indicator": "Red",
			"label": _("Total Check for lead last modified date"),
			"datatype": "Int"
		}
	]

