from __future__ import unicode_literals
import frappe
#mfi_customization.mfi.patch.compatible_items.execute

def execute():
    add_item_acc()
    add_item_ton()

def add_item_acc():
	compatible_items = frappe.get_all("Compatible Items")
	for c_item in compatible_items:
		c_item = frappe.get_doc("Compatible Items", c_item)
		if frappe.db.exists('Item',c_item.asset_item):
			item = frappe.get_doc('Item',c_item.asset_item)
			print('checking item to add compatible item')
			company = "MFI DOCUMENT SOLUTIONS KENYA"
			added_items = [row.item_code for row in item.compatible_spares]
			added_compatible_toners = [row.item_code for row in item.compatible_toners]
			item_modified = 0
			if c_item.item not in added_items and c_item.type == "Accessories":
				print('*************adding Accessories***************')
				add_on_entry_child = item.append('compatible_spares',{})
				add_on_entry_child.item_code = c_item.item
				add_on_entry_child.company = company
				add_on_entry_child.item_name = item.item_name
				add_on_entry_child.item_group = item.item_group
				add_on_entry_child.yeild = item.yeild
				item_modified = 1


			# elif c_item.item not in added_compatible_toners and c_item.type == "Toner":
			# 	print('*************adding Toner***************')
			# 	add_on_entry_child = item.append('compatible_toners',{})
			# 	add_on_entry_child.item_code = c_item.item
			# 	add_on_entry_child.company = company
			# 	add_on_entry_child.item_name = item.item_name
			# 	add_on_entry_child.item_group = item.item_group
			# 	add_on_entry_child.yeild = item.yeild
			# 	item_modified = 1
			if item_modified:
				print('*************saving item***************')
				item.save()
	frappe.db.commit()


def add_item_ton():
	compatible_items = frappe.get_all("Compatible Items")
	for c_item in compatible_items:
		c_item = frappe.get_doc("Compatible Items", c_item)
		if frappe.db.exists('Item',c_item.asset_item):
			item = frappe.get_doc('Item',c_item.asset_item)
			print('checking item to add compatible item')
			company = "MFI DOCUMENT SOLUTIONS KENYA"
			added_items = [row.item_code for row in item.compatible_spares]
			added_compatible_toners = [row.item_code for row in item.compatible_toners]
			item_modified = 0
			# if c_item.item not in added_items and c_item.type == "Accessories":
			# 	print('*************adding Accessories***************')
			# 	add_on_entry_child = item.append('compatible_spares',{})
			# 	add_on_entry_child.item_code = c_item.item
			# 	add_on_entry_child.company = company
			# 	add_on_entry_child.item_name = item.item_name
			# 	add_on_entry_child.item_group = item.item_group
			# 	add_on_entry_child.yeild = item.yeild
			# 	item_modified = 1


			if c_item.item not in added_compatible_toners and c_item.type == "Toner":
				print('*************adding Toner***************')
				add_on_entry_child = item.append('compatible_toners',{})
				add_on_entry_child.item_code = c_item.item
				add_on_entry_child.company = company
				add_on_entry_child.item_name = item.item_name
				add_on_entry_child.item_group = item.item_group
				add_on_entry_child.yeild = item.yeild
				item_modified = 1
			if item_modified:
				print('*************saving item***************')
				item.save()
	frappe.db.commit()