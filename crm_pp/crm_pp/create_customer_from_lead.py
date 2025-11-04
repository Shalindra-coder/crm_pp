import frappe
from erpnext.crm.doctype.lead.lead import _make_customer

@frappe.whitelist()
def create_customer_from_lead(doc, method=None):
    if doc.status in ["Converted", "Convert"]:
        try:
            existing_customer = frappe.db.exists("Customer", {"lead_name": doc.name})
            if existing_customer:
                return

            customer_doc = _make_customer(source_name=doc.name)

            if hasattr(customer_doc, "customer_type"):
                if customer_doc.customer_type.strip() == "Company":
                    customer_doc.customer_type = "Business Owner "

            # Insert without running validations
            customer_doc.flags.ignore_validate = True
            customer_doc.flags.ignore_mandatory = True
            customer_doc.insert(ignore_permissions=True)

            frappe.db.commit()
            frappe.logger().info(f" Customer auto-created for Lead: {doc.name}")

        except Exception as e:
            frappe.log_error(
                f"Error auto-creating Customer from Lead {doc.name}: {str(e)}",
                "Lead to Customer Auto Creation Error"
            )
