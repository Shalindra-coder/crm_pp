// Copyright (c) 2025, CRM PP and contributors
// For license information, please see license.txt

frappe.query_reports["Lead MQL SQL - AK"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -3),
			"reqd": 0
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 0
		},
		{
			"fieldname": "lead_owner",
			"label": __("Lead Owner"),
			"fieldtype": "Link",
			"options": "User"
		},
		{
			"fieldname": "status",
			"label": __("Lead Status"),
			"fieldtype": "Select",
			"options": "\nLead\nOpen\nReplied\nOpportunity\nQuotation\nLost Quotation\nInterested\nConverted\nDo Not Contact"
		},
		{
			"fieldname": "custom_vertical",
			"label": __("Vertical"),
			"fieldtype": "Link",
			"options": "Vertical"
		},
		{
			"fieldname": "source",
			"label": __("Lead Source"),
			"fieldtype": "Data"
		},
		{
			"fieldname": "industry",
			"label": __("Industry"),
			"fieldtype": "Data"
		},
		{
			"fieldname": "city",
			"label": __("City"),
			"fieldtype": "Data"
		},
		{
			"fieldname": "custom_rating",
			"label": __("Rating"),
			"fieldtype": "Select",
			"options": "\nHot\nWarm\nCold"
		}
	]
};

