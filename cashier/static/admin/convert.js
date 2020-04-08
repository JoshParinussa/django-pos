"use strict";
window.csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
var KTDatatablesDataSourceAjaxServer = function() {

    var initTable1 = function() {
	    var table = $('.data-table');
		// begin first table
		table.DataTable({
			responsive: true,
            searchDelay: 500,
            processing: true,
            serverSide: true,
            autoWidth: false,
			serverSide: true,
			pageLength: 10,
			ordering: true,
			paging: true,
			order: [[ 0, "asc" ]],
            ajax: {
					'type': 'POST',
					'url': '/v1/converts/get_by_product?format=datatables',
					'data': {'product':currentProduct},
			},
			columnDefs: [
				{
					targets: 0,
					render: function(data){
						console.log(data);
						return !$.trim(data) ? '' : data;
					}	
					// render: function(data, type, row){
					// 	return `<a href="products/${row.id}" title="Product Details">${data}</a>`;
					// }
				},{
					targets: 1,
					render: function(data){
						console.log(data);
						return !$.trim(data) ? '' : data;
					}	
                },
                {
					targets: 2,
					render: function(data){
						console.log(data);
						return !$.trim(data) ? '' : data;
					}	
                },
                {
					targets: 3,
					render: function(data){
						console.log(data);
						return !$.trim(data) ? '' : data;
					}	
                },
                {
					targets: 4,
					render: function(data){
						console.log(data);
						return !$.trim(data) ? '' : data;
					}	
                },
                {
					targets: 5,
					render: function(data){
						console.log(data);
						return !$.trim(data) ? '' : data;
					}	
                },
                {
					targets: 6,
					render: function(data){
						console.log(data);
						return !$.trim(data) ? '' : data;
					}	
                },
				{
					targets: -1,
					title: 'Actions',
					orderable: false,
					render: function(data, type, row) {
						return `<a href="${row.id}" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Variant List">
                          <i class="nav-icon fas fa-edit"></i>
                    </a>`;
					},
				},
      ],
			columns: [
				{data: 'quantity', orderable: true, searchable:true, name: 'quantity'},
				{data: 'unit', orderable: true, searchable:true, name: 'unit'},
                {data: 'purchase_price', orderable: true, searchable:true, name: 'purchase_price'},
                {data: 'selling_price', orderable: true, searchable:true, name: 'selling_price'},
                {data: 'grosir_1_price', orderable: true, searchable:true, name: 'grosir_1_price'},
                {data: 'grosir_2_price', orderable: true, searchable:true, name: 'grosir_2_price'},
                {data: 'grosir_3_price', orderable: true, searchable:true, name: 'grosir_3_price'},
				{data: 'Actions', searchable: false, orderable: false, responsivePriority: -1}
			],
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
    // ProductsForm.init();
});
