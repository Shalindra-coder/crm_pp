// Copyright (c) 2025, CRM PP and contributors
// For license information, please see license.txt

frappe.query_reports["Daily Leads Report-Shreya"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
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
			"options": "\nLead\nOpen\nReplied\nOpportunity\nQuotation\nLost Quotation\nInterested\nConverted\nDo Not Contact\nNew\nWorking\nNurturing\nQualified\nUnqualified\nConvert"
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
			"fieldname": "state",
			"label": __("State/Province"),
			"fieldtype": "Data"
		},
		{
			"fieldname": "country",
			"label": __("Country"),
			"fieldtype": "Link",
			"options": "Country"
		},
		{
			"fieldname": "custom_rating",
			"label": __("Rating"),
			"fieldtype": "Select",
			"options": "\nHot\nWarm\nCold"
		},
		{
			"fieldname": "owner",
			"label": __("Created By"),
			"fieldtype": "Link",
			"options": "User"
		},
		{
			"fieldname": "campaign_name",
			"label": __("Campaign Name"),
			"fieldtype": "Link",
			"options": "Campaign"
		}
	]
};

