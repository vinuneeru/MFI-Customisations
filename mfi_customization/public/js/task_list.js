frappe.listview_settings['Task'] = {
    add_fields: ["mr_status"],
    get_indicator: function(doc) {
        if (doc.mr_status == 'Material Rejected') {
            return [__("Material Rejected"), "red", "status,=,Material Rejected"];
        }
    },

    // refresh: setTimeout(function(frm){
    //     if (frappe.user.has_role("Technicians") == true && frappe.user != "Administrator"){
	// 		$('.layout-side-section').remove()
	// 	}
    // }, 200
    // )
};