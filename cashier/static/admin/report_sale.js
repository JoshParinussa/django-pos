"use strict";
window.csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
var itemBarcode;
var itemName;
var itemPrice;
var grandTotal = 0;

var row;
var table;

var KTDatatablesDataSourceAjaxServer = function() {

    var initTable1 = function() {
	    table = $('#example1');
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
					'type': 'POST',
					'url': '/v1/report_sale/get_by_invoice?format=datatables',
					'data': {'invoice':currentInvoiceID},
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
						return !$.trim(data) ? '' : data;
					}
				},
				{
					targets: -1,
					title: 'Actions',
					orderable: false,
					render: function(data, type, row) {
						return `<button type='button' onclick='updateItem(this)' id='btn-update' class='btn btn-info btn-update' data-toggle='modal' data-target='#modal-default'>Update</button>&nbsp;
								<button type='button' onclick='deleteItem(this)' class='btn btn-danger' id='btn-delete'>Delete</button>&nbsp;`;
					},
				},
      ],
			columns: [
				{data: 'barcode', orderable: true, searchable:true, name: 'barcode'},
				{data: 'product', orderable: true, searchable:true, name: 'product'},
				{data: 'price', orderable: true, searchable:true, name: 'price'},
				{data: 'qty', orderable: true, searchable:true, name: 'qty'},
				{data: 'total', orderable: true, searchable:true, name: 'total'},
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

var updateItem = function(e){
    row = $(e).closest('tr');
	row_barcode = row.attr('id');
	console.log(row.val());
    // var itemName = row.attr('product');
    // var itemQty = row.attr('qty');
    // var itemBarcode = row.attr('barcode');
    // $('#modal-item-name').val(itemName);
    // $('#modal-qty-item-cart').val(itemQty);
	// $('#modal-barcode').val(itemBarcode);
	// console.log(row);
}

$('#modal-btn-update').click(function(e){
    var newQty = $('#modal-qty-item-cart').val();
    grandTotal -= Number(row.attr('total'));
    var newTotal = Number(newQty) * Number(row.attr('price'));
    grandTotal += newTotal;
    $.ajax({
        type: "POST",
        url: "/v1/report_sale/update_item",
        data:{
            "invoice_number": invoice_number,
            "barcode": $('#modal-barcode').val(),
            "qty": newQty,
            'total': newTotal
        },
        success: function(result){
            row.find(".qty").html(newQty);
            row.find(".purchase_total").html(newTotal)
            $('#modal-default').modal('toggle');
            $('#grand_total').text(grandTotal);
        }
    });
});

var deleteItem = function(e){
    var row = $(e).closest('tr')
    var row_barcode = row.attr('id');
    
    $.ajax({
        type: "POST",
        url: "/v1/report_item/delete_item",
        data:{
            "invoice_number": invoice_number,
            "barcode": row_barcode,
        },
        success: function(result){
            grandTotal -= result.total;
            $('#grand_total').text(grandTotal);
			row.remove();
        }
    });
}

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
