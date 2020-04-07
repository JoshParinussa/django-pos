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
		table.dataTable({
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
			table = $('#example1').dataTable();
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
    row = table.api().row($(e).closest('tr')).data();
    $('#modal-item-name').val(row.product);
    $('#modal-qty-item-cart').val(row.qty);
	$('#modal-barcode').val(row.barcode);
}

$('#modal-btn-update').click(function(e){
    var newQty = $('#modal-qty-item-cart').val();
	var newTotal = Number(newQty) * Number(row.price);
	var oldTotal = Number(row.qty) * Number(row.price);
	var diffTotal = oldTotal - newTotal;
	var oldChange = Number(InvoiceChange);
	InvoiceGrandTotal = Number(InvoiceGrandTotal)- diffTotal;
	InvoiceChange = Number(InvoiceCash)- Number(InvoiceGrandTotal);
	var diffChange = Number(InvoiceChange) - oldChange;
	if(diffChange<0){
		InvoiceCash = Number(InvoiceCash) + Number(Math.abs(diffChange));
		InvoiceChange = 0;
	}
    $.ajax({
        type: "POST",
        url: "/v1/report_sale/update_item",
        data:{
            "invoice_number": currentInvoiceID,
            "barcode": $('#modal-barcode').val(),
            "qty": newQty,
			'total': newTotal,
			'grand_total':InvoiceGrandTotal,
			'cash':InvoiceCash,
			'change':InvoiceChange
        },
        success: function(result){
            if(diffChange>0){
				alert("Kembalian tambah Rp. "+diffChange);
			}else if(diffChange<0){
				alert("Uang kurang Rp. "+Math.abs(diffChange));
			}
            $('#modal-default').modal('toggle');
			$('#grand_total').text(InvoiceGrandTotal);
			$('#change').text(InvoiceChange);
			$('#cash').text(InvoiceCash);
			table.api().ajax.reload();
			// location.reload();
        }
	});
	grandTotal = 0;
});

var deleteItem = function(e){
    var row = table.api().row($(e).closest('tr')).data()
    var row_barcode = row.barcode;
    
    $.ajax({
        type: "POST",
        url: "/v1/report_item/delete_item",
        data:{
            "invoice_number": currentInvoiceID,
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
