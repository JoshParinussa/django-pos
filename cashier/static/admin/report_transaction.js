"use strict";
window.csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
var table;
var condition;
var row;
var income;

var KTDatatablesDataSourceAjaxServer = function() {
    // condition = $('#date_list_transaction').val();
    // console.log("#"+condition)
    var initTable1 = function() {
        table = $('.data-table');
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
            order: [
                [0, "asc"]
            ],
            ajax: {
                'type': 'POST',
                'url': '/v1/report_transaction/set_datatable?format=datatables',
                'data' : function(data){
                    data.date=condition;
                }
            },
            columnDefs: [{
                    targets: 0,
                    render: function(data, type, row) {
                        return !$.trim(data) ? '' : data;
                    },
                },
                {
                    targets: 1,
                    render: function(data) {
                        return !$.trim(data) ? '' : data;
                    }
                },
                {
                    targets: 2,
                    render: function(data) {
                        return !$.trim(data) ? '' : data;
                    }
                },
                {
                    targets: 3,
                    render: function(data) {
                        return !$.trim(data) ? '' : data;
                    }
                },
                {
                    targets: 4,
                    render: function(data) {
                        return !$.trim(data) ? '' : data == 1 ? 'SUCCESS' : 'PENDING';
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
                { data: 'invoice', orderable: true, searchable: true, name: 'invoice' },
                { data: 'date', orderable: true, searchable: true, name: 'date' },
                { data: 'cashier', orderable: true, searchable: true, name: 'cashier' },
                { data: 'total', orderable: true, searchable: true, name: 'total' },
                { data: 'status', orderable: true, searchable: true, name: 'status' },
                { data: 'Actions', searchable: false, orderable: false, responsivePriority: -1 }
            ],
        });
        $("#sidebar").on('click', function(e) {
            table = $('#example1').dataTable();
            table.columns.adjust().draw();
            // $($.fn.dataTable.tables(true)).DataTable()
            //   .columns.adjust();
            $(".dataTables_scrollHeadInner .dataTables_scrollHead .table").css("width", "100%");
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

$('#date_list_transaction').change(function(){
    condition = this.value;
    console.log(condition)
    $.ajax({
        type: "POST",
        url: "/v1/report_transaction/set_income",
        data: {
            'date': condition
        },
        success: function(result) {
            $('#income').html('Rp. '+result.income);
            income = result.income;
            // console.log(table);
        }
    });
    $.ajax({
        type: "POST",
        url: "/v1/report_transaction/set_datatable?format=datatables",
        data: function(data){
            data.date=condition;
        },
        success: function(result) {
            table.api().ajax.reload();
        }
    });
});
    

var printResult = function() {
    // console.log(table.api().data());
    var receipt_body = '';
    table.api().data().each(function(row_data){
        row = row_data;
        var invoice = row_data.invoice;
        var date = row_data.date;
        var cashier = row_data.cashier;
        var total = 0;
        if (row_data.total != null){
            total = row_data.total;
        }
        var status = "PENDING";
        if (row_data.status != 0){
            status = "SUCCESS";
        }
        receipt_body +=
            `<tr>
                <td class="invoice">${invoice}</td>
                <td class="date">${date}</td>
                <td class="cashier">${cashier}</td>
                <td class="total">${total}</td>
                <td class="status">${status}</td>
            </tr>`;
    })
    
    var receipt =
        `<div class="print-receipt">
            <div class="col-12">
                <div class="row center">
                    <h3>Minimarketku</div>
                </div>
                <div class="row">
                    <table>
                        <tbody>
                            <tr>
                                <td style="border-top:1px dashed black; border-bottom:1px dashed black;" >${currentDate}</td>
                                <td style="border-top:1px dashed black; border-bottom:1px dashed black;" colspan="2"></td>
                                <td style="border-top:1px dashed black; border-bottom:1px dashed black;" ></td>
                            </tr>
                            <tr>
                            </tr>
                            ${receipt_body}
                            <tr>
                                <td></td>
                                <td style="border-top:1px dashed black;" colspan="3"></td>
                            </tr>
                            <tr>
                                <td>
                                <td colspan="2">OMSET</td>
                                <td>: Rp. ${income}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="row center">
                <br><br><br>
                    <p>===== TERIMA KASIH =====</p>
                    <p>SELAMAT BERBELANJA KEMBALI</p>
                </div>
            </div>
        </div>`;
    // '<div id="print-receipt">' +
    // '<div class="receipt" id="receipt">' +
    // '<p class="centered" id="ticket-title">Minimarketku' +
    // '<table>' +
    // '<thead>' +
    // '<tr>' +
    // '<th class="quantity">Qty.</th>' +
    // '<th class="description">Item</th>' +
    // '<th class="price">Total</th>' +
    // '</tr>' +
    // '</thead>' +
    // '<tbody>' +
    // receipt_body +
    // '</tbody>' +
    // '</table>' +
    // '<p class="centered">Terimakasih, datang kembali' +
    // '</div>' +
    // '</div>';

    var receipt_css =
        `<style type="text/css">
            @page {margin: 0;}
            .print-receipt {
                width: 58mm;
            }
            .center {
                text-align: center;
                font-size: 8px;
              }
            table, th, td {
            font-size: 8px;
            }
            table {width:100%;}
            td .item {width:50%;}
            td .quantity {width:10%;}
            td .price {width:20%;}
            td .subtotal {width:20%;}
            
        </style>`;


    var myPrintWindow = window.open('', 'Cetak Receipt', '');
    myPrintWindow.document.write(receipt_css);
    myPrintWindow.document.write(receipt);
    myPrintWindow.document.close();
    myPrintWindow.focus();
    myPrintWindow.print();
    myPrintWindow.close();
    return false;
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

$('#btn-print-report').click(function() {
    printResult()
})


jQuery(document).ready(function() {
    KTDatatablesDataSourceAjaxServer.init();
});