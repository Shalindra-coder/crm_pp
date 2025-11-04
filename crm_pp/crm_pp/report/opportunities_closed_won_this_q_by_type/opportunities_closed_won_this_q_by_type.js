// Copyright (c) 2025, Prompt Personnel and contributors
// For license information, please see license.txt

frappe.query_reports["Opportunities Closed Won This Q by Type"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
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
			"fieldname": "stage",
			"label": __("Stage"),
			"fieldtype": "Select",
			"options": "\nQualification\nNeeds Analysis\nValue Proposition\nIdentify Decision Makers\nPerception Analysis\nProposal/Price Quote\nNegotiation/Review\nClosed Won\nClosed Lost",
			"default": "Closed Won"
		},
		{
			"fieldname": "opportunity_record_type",
			"label": __("Opportunity Record Type"),
			"fieldtype": "Link",
			"options": "Opportunity Type",
			"reqd": 0
		},
		{
			"fieldname": "vertical",
			"label": __("Vertical"),
			"fieldtype": "Select",
			"options": "\nPermanent Staffing\nTemporary Staffing\nLearning & Development\nLabour Law Advisory & Compliance\nFranchise",
			"reqd": 0
		},
		{
			"fieldname": "opportunity_owner",
			"label": __("Opportunity Owner"),
			"fieldtype": "Link",
			"options": "User",
			"reqd": 0
		},
		{
			"fieldname": "lead_source",
			"label": __("Lead Source"),
			"fieldtype": "Select",
			"options": "\nSelf\nWebsite_form_SEO\nSEO\nEmployee Referral\nDirect Calls\nDirect_Emails_SEO\nRAI\nSmatbot_SEO\nLinkedIn\nGoogle Ads\nFacebook",
			"reqd": 0
		},
		{
			"fieldname": "industry",
			"label": __("Industry"),
			"fieldtype": "Link",
			"options": "Industry Type",
			"reqd": 0
		},
		{
			"fieldname": "opportunity_type",
			"label": __("Type"),
			"fieldtype": "Link",
			"options": "Opportunity Type",
			"reqd": 0
		}
	],
	
	"onload": function(report) {
		// Set default date range to current quarter
		var today = new Date();
		var currentMonth = today.getMonth(); // 0-11
		var currentYear = today.getFullYear();
		
		// Calculate quarter start month (0, 3, 6, 9)
		var quarterStartMonth = Math.floor(currentMonth / 3) * 3;
		
		// Quarter start date
		var quarter_start = new Date(currentYear, quarterStartMonth, 1);
		
		// Quarter end date (last day of the quarter)
		var quarter_end = new Date(currentYear, quarterStartMonth + 3, 0);
		
		// Format dates as YYYY-MM-DD
		var from_date = frappe.datetime.obj_to_str(quarter_start);
		var to_date = frappe.datetime.obj_to_str(quarter_end);
		
		report.set_filter_value('from_date', from_date);
		report.set_filter_value('to_date', to_date);
	}
};

