"use strict";
var KTDatatablesDataSourceAjaxServer = function() {

    var initTable1 = function() {
	    var table = $('#example1');
		console.log("A");
		// begin first table
		table.DataTable({
			scrollX: true,
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
					'url': '/v1/products?format=datatables',
			},
			columnDefs: [
				{
					targets: 0,
					render: function(data, type, row) {
						return `<a href="convert/${row.id}" title="Convert">
                          `+(!$.trim(data) ? '' : data)+`
                    </a>`;
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
						return !$.trim(data) ? '' : data;
					}
				},
				{
					targets: 5,
					render: function(data){
						return !$.trim(data) ? '' : data;
					}
				},
				{
					targets: 6,
					render: function(data){
						return !$.trim(data) ? '' : data;
					}
				},
				{
					targets: 7,
					render: function(data){
						return !$.trim(data) ? '' : data;
					}
				},
				{
					targets: 8,
					render: function(data){
						return !$.trim(data) ? '' : data;
					}
				},
				{
					targets: 9,
					render: function(data){
						return !$.trim(data) ? '' : data;
					}
				},
				{
					targets: 10,
					render: function(data){
						return !$.trim(data) ? '' : data;
					}
				},
				{
					targets: 11,
					render: function(data){
						return !$.trim(data) ? '' : data;
					}
				},
				{
					targets: 12,
					render: function(data){
						return !$.trim(data) ? '' : data;
					}
				},
				{
					targets: -1,
					title: 'Actions',
					orderable: false,
					render: function(data, type, row) {
						return `<a href="products/${row.id}" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Variant List">
                          <i class="nav-icon fas fa-edit"></i>
                    </a>`;
					},
				},
      ],
			columns: [
				{data: 'name', orderable: true, searchable:true, name: 'name'},
				{data: 'barcode', orderable: true, searchable:true, name: 'barcode'},
				{data: 'stock', orderable: true, searchable:true, name: 'stock'},
				{data: 'category', orderable: true, searchable:true, name: 'category.name'},
				{data: 'unit', orderable: true, searchable:true, name: 'unit'},
				{data: 'purchase_price', orderable: true, searchable:true, name: 'purchase_price'},
				{data: 'selling_price', orderable: true, searchable:true, name: 'selling_price'},
				{data: 'quantity_grosir_1', orderable: true, searchable:true, name: 'quantity_grosir_1'},
				{data: 'grosir_1_price', orderable: true, searchable:true, name: 'grosir_1_price'},
				{data: 'quantity_grosir_2', orderable: true, searchable:true, name: 'quantity_grosir_2'},
				{data: 'grosir_2_price', orderable: true, searchable:true, name: 'grosir_2_price'},
				{data: 'quantity_grosir_3', orderable: true, searchable:true, name: 'quantity_grosir_3'},
				{data: 'grosir_3_price', orderable: true, searchable:true, name: 'grosir_3_price'},
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
