import frappe
from frappe import _
from frappe.utils import getdate, today


def execute(filters=None):
	"""Execute the Lead report -Priyanka"""
	columns = get_columns()
	data = get_data(filters)
	chart = None
	summary = get_summary(data)
	
	return columns, data, None, chart, summary


def get_columns():
	"""Define report columns matching the screenshot"""
	return [
		{
			"fieldname": "source",
			"label": _("Lead Source"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "status",
			"label": _("Lead Status"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "lead_owner",
			"label": _("Lead Owner"),
			"fieldtype": "Link",
			"options": "User",
			"width": 150
		},
		{
			"fieldname": "custom_vertical",
			"label": _("Vertical"),
			"fieldtype": "Link",
			"options": "Vertical",
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
			"fieldname": "industry",
			"label": _("Industry"),
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "company_name",
			"label": _("Company / Account"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "email_id",
			"label": _("Email"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "website",
			"label": _("Website"),
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "phone",
			"label": _("Phone"),
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
			"fieldname": "custom_unqualified_reason",
			"label": _("Unqualified Reason"),
			"fieldtype": "Data",
			"width": 150
		},
		{
			"fieldname": "modified",
			"label": _("Last Modified"),
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "campaign_name",
			"label": _("Campaign Name"),
			"fieldtype": "Link",
			"options": "Campaign",
			"width": 200
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
		{
			"fieldname": "custom_turnover",
			"label": _("Turnover (In INR)"),
			"fieldtype": "Data",
			"width": 130
		},
		{
			"fieldname": "no_of_employees",
			"label": _("No. of Employees"),
			"fieldtype": "Int",
			"width": 130
		},
		{
			"fieldname": "age_today",
			"label": _("Age today"),
			"fieldtype": "Int",
			"width": 100
		},
		{
			"fieldname": "age_last_modify",
			"label": _("Age Last Modify"),
			"fieldtype": "Int",
			"width": 120
		},
	]


def get_data(filters):
	"""Get lead data based on filters"""
	
	conditions = get_conditions(filters)
	
	# SQL query to get all lead data with calculated age fields
	data = frappe.db.sql("""
		SELECT
			source,
			status,
			lead_owner,
			custom_vertical,
			first_name,
			last_name,
			job_title,
			industry,
			company_name,
			email_id,
			website,
			phone,
			DATE(creation) as creation,
			custom_unqualified_reason,
			DATE(modified) as modified,
			campaign_name,
			custom_hr_experience,
			city,
			custom_rating,
			custom_description,
			custom_salary_offering,
			mobile_no,
			custom_turnover,
			no_of_employees,
			DATEDIFF(CURDATE(), DATE(creation)) as age_today,
			DATEDIFF(CURDATE(), DATE(modified)) as age_last_modify
		FROM
			`tabLead`
		WHERE
			docstatus < 2
			{conditions}
		ORDER BY
			source ASC, lead_owner ASC, creation DESC
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
	
	return " ".join(conditions) if conditions else ""


def get_summary(data):
	"""Get summary statistics for the report"""
	if not data:
		return []
	
	total_records = len(data)
	total_employees = sum([row.get("custom_no_of_employees") or 0 for row in data])
	total_age_today = sum([row.get("age_today") or 0 for row in data])
	total_age_last_modify = sum([row.get("age_last_modify") or 0 for row in data])
	
	return [
		{
			"value": total_records,
			"indicator": "Blue",
			"label": _("Total Records"),
			"datatype": "Int"
		},
		{
			"value": total_employees,
			"indicator": "Green",
			"label": _("Total No. of Employees"),
			"datatype": "Int"
		},
		{
			"value": total_age_today,
			"indicator": "Orange",
			"label": _("Total Age today"),
			"datatype": "Int"
		},
		{
			"value": total_age_last_modify,
			"indicator": "Purple",
			"label": _("Total Age Last Modify"),
			"datatype": "Int"
		}
	]

