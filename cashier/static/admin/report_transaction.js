"use strict";
var KTDatatablesDataSourceAjaxServer = function() {

    var initTable1 = function() {
	    var table = $('.data-table');
		console.log("A");
		// begin first table
		table.DataTable({
			autoWidth: false,
			processing: true,
            serverSide: true,
            serverSide: false,
			pageLength: 10,
			ordering: true,
			paging: true,
			scrollX: true,
			order: [[ 0, "asc" ]],
            ajax: {
					'type': 'GET',
					'url': '/v1/report_transaction?format=datatables',
			},
			columnDefs: [
				{
					targets: 0,
					render: function(data, type, row) {
						return !$.trim(data) ? '' : data;
					},
				},
				{
					targets: 1,
					render: function(data){
						return !$.trim(data) ? '' : data;
					}
				},
				{
					targets: 2,
					render: function(data){
						return !$.trim(data) ? '' : data;
					}
				},
				{
					targets: 3,
					render: function(data){
						return !$.trim(data) ? '' : data;
					}
				},
				{
					targets: 4,
					render: function(data){
						return !$.trim(data) ? '' : data == 1 ? 'SUCCESS' : 'FAIL';
					}
				},
				{
					targets: -1,
					title: 'Actions',
					orderable: false,
					render: function(data, type, row) {
						return `<a href="../report/sale/${row.id}" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Detail">
                          <i class="nav-icon fas fa-edit"></i>
                    </a>`;
					},
				},
      ],
			columns: [
				{data: 'invoice', orderable: true, searchable:true, name: 'invoice'},
				{data: 'date', orderable: true, searchable:true, name: 'date'},
				{data: 'cashier', orderable: true, searchable:true, name: 'cashier'},
				{data: 'total', orderable: true, searchable:true, name: 'total'},
				{data: 'status', orderable: true, searchable:true, name: 'status'},
				{data: 'Actions', searchable: false, orderable: false, responsivePriority: -1}
			],
		});
		$("#sidebar").on('click', function(e){
			var table = $('#example1').DataTable();
			table.columns.adjust().draw();
			// $($.fn.dataTable.tables(true)).DataTable()
			//   .columns.adjust();
			$(".dataTables_scrollHeadInner .dataTables_scrollHead .table").css("width","100%");
			console.log("APA")
		  });
		
	};
	return {

		//main function to initiate the module
		init: function() {
			initTable1();
			// if ($.fn.dataTable){
			// 	initTable1();
			// }
		},

	};

}();


// Class definition
// var ProductsForm = function () {
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
// 			initValidation();
// 			$('.select2').select2();
//         }
//     };
// }();



jQuery(document).ready(function() {
	KTDatatablesDataSourceAjaxServer.init();
});
