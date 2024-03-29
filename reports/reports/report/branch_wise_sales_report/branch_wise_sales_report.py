# Copyright (c) 2013, Hardik Gadesha and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import msgprint, _

def execute(filters=None):

        conditions, filters = get_conditions(filters)
        columns = get_column()
        data = get_data(conditions,filters)
        return columns,data

def get_column():
        return [_("Date") + ":Date:120",
                _("Location")+ ":Link/Location List:120",
                _("Invoice No") + ":Link/Sales Invoice:120",
                _("Customer Names") + ":Link/Customer:150",
                _("Grand Total") + ":Currency:100",
                _("Outstanding Amount") + ":Currency:140",
                _("Status") + "::100"]

def get_data(conditions,filters):
        invoice = frappe.db.sql("""select posting_date,location_list,name, customer_name, grand_total, outstanding_amount, status 
                                from `tabSales Invoice` where docstatus is not null 
                                and (status = 'Unpaid' or status = 'Paid' or status = 'Overdue' or status = 'Submitted') 
                                %s order by posting_date asc;"""%conditions, filters, as_list=1)
        return invoice

def get_conditions(filters):
        conditions = ""
        if filters.get("from_date"): conditions += " and posting_date >= %(from_date)s"
        if filters.get("to_date"): conditions += " and posting_date <= %(to_date)s"
        if filters.get("type"): conditions += "and invoice_type = %(type)s"
        if filters.get("location"): conditions += "and location = %(location)s"

	return conditions, filters
