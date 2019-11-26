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
        return [_("Item Code") + ":Data:120",
                _("Description") + ":Data:320",
		_("Sold Qty") + ":Float:120"]

def get_data(conditions,filters):
        invoice = frappe.db.sql("""select
        si_item.item_code,
        si_item.description,
	sum(si_item.stock_qty)
from
        `tabSales Invoice` si, `tabSales Invoice Item` si_item
where
        (si.name = si_item.parent) and (si.docstatus = 1) %s group by si_item.item_code;;"""%conditions, filters, as_list=1)
        return invoice

def get_conditions(filters):
        conditions = ""
        if filters.get("from_date"): conditions += " and si.posting_date >= %(from_date)s"
        if filters.get("to_date"): conditions += " and si.posting_date <= %(to_date)s"

	return conditions, filters
