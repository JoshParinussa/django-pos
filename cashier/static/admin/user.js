"use strict";

var KTDatatablesDataSourceAjaxServer = function() {


	var initTable1 = function() {
		var table = $('#example1');

		if (!table.length) return;

		// begin first table
		table.DataTable({
			serverSide: true,
			pageLength: 50,
			order: [[ 3, "desc" ]],
            ajax: {
					'type': 'GET',
					'url': '/v1/employees?format=datatables',
					// 'dataSrc': 'data.users'
			},
			columnDefs: [
				{
					targets: 0, 
					render: function(data, type, row){
						var output = `
								<span class="kt-user-card-v2__name"><a href="users/${row.id}" title="User Details">${data}</a></span>`;
						return !$.trim(data) ? '' : output;	
				}},
				{targets: 1, render: function(data){
					var d = moment(data).format("ll");
					return d;
				}},
				{targets: 2, render: function(data){
					if (data === true){
						return '<span class="badge badge-primary">Admin</span>';
					}else{
						return '<span class="badge badge-warning">Employee</span>';
					}
				}},
                {targets: 3, render: function(data){
					if (data === true){
						return '<span class="text-primary">.Active</span>';
					}else{
						return '<span class="text-danger">.Inactive</span>';
					}
				}}
            ],
			columns: [
				{data: 'email', orderable: true, searchable:true, name: 'email'},
                {data: 'date_joined', orderable: true, searchable:false},
				{data: 'is_staff', orderable: true, searchable: false},
				{data: 'is_active', orderable: true, searchable: false}
			]
		});
	};
	return {

		//main function to initiate the module
		init: function() {
			initTable1();
		},

	};

}();

// Class definition
// var UserCreate = function () {
//     // Base elements
//     var formEl;
//     var validator;

//     var initValidation = function() {
//         validator = formEl.validate({
//             // Validate only visible fields
//             ignore: ":hidden",

//             // Validation rules
//             rules: {
//             },

//             // Display error
//             invalidHandler: function(event, validator) {
//                 KTUtil.scrollTop();
//             },
//         });
//     }

//     return {
//         // public functions
//         init: function() {
//             formEl = $('#kt_form');
//             initValidation();
//             $('.select2').select2();
//         }
//     };
// }();

jQuery(document).ready(function() {
	// UserCreate.init();
	KTDatatablesDataSourceAjaxServer.init();
});
