"use strict";
window.csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
var table;
var condition;
var row;
var income;
var profit;
var currentDate;
var data;
var data_2;
var product_all;
var dates;


var KTDatatablesDataSourceAjaxServer = function() {
    var initDateRangePicker = function() {
        var start = moment().subtract(29, 'days');
        var end = moment();
        $('#kt_daterangepicker_6 .form-control').val(moment().format('YYYY-MM-DD') + ' to ' + moment().format('YYYY-MM-DD'));
        $('#kt_daterangepicker_6').daterangepicker({
            buttonClasses: ' btn',
            applyClass: 'btn-primary',
            cancelClass: 'btn-secondary',

            startDate: start,
            endDate: end,
            ranges: {
                'Today': [moment(), moment()],
                'Yesterday': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
                'Last 7 Days': [moment().subtract(6, 'days'), moment()],
                'Last 30 Days': [moment().subtract(29, 'days'), moment()],
                'This Month': [moment().startOf('month'), moment().endOf('month')],
                'Last Month': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
            }
        }, function(start, end, label) {
            $('#kt_daterangepicker_6 .form-control').val(start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
        });
    };
    var getDaterange = function() {
        var date_range = $('#date-picker-range').val();
        dates = date_range.split(' to ');
        return dates
    }
    var initTable1 = function() {
        table = $('.data-table');
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
                'data': function(d) {
                    d.date_range = getDaterange();
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
    };

    var initEvents = function() {
        $('#btn-filter-date').on('click', function(e) {
            table.api().ajax.reload();
        });

    };

    return {
        init: function() {
            initDateRangePicker();
            initTable1();
            initEvents();
        },
    };
}();

$('#date_list_transaction').change(function() {
    condition = this.value;
    console.log(condition)
    $.ajax({
        type: "POST",
        url: "/v1/report_transaction/set_income_profit",
        data: {
            'date': condition
        },
        success: function(result) {
            $('#income').html('Rp. ' + result.income);
            $('#profit').html('Rp. ' + result.profit);
            income = result.income;
            profit = result.profit;
            currentDate = result.date;
            data_2 = result.data_2;
            console.log(data_2);
            product_all = result.product;
        }
    });
    $.ajax({
        type: "POST",
        url: "/v1/report_transaction/set_datatable?format=datatables",
        data: function(data) {
            data.date = condition;
        },
        success: function(result) {
            table.api().ajax.reload();
        }
    });
});


var printResult = function() {
    // console.log(table.api().data());
    var receipt_header = '';
    var receipt_body = '';
    var receipt_all = '';
    var invoice_sale;
    var product_name;
    var barcode;
    var selling_price;
    var qty;
    var total;
    table.api().data().each(function(row_data) {
        row = row_data;
        var invoice = row_data.invoice;
        var cashier = row_data.cashier;

        receipt_header = `<tr>
                                <td class="invoice">${invoice}</td>
                                <td class="cashier">${cashier}</td>
                            </tr>`;
        // console.log(data_2)
        $.each(data_2, function(key, value) {
                console.log(key + " " + value)
                    // invoice_sale = a.invoice;
                    // product_name = a.product_id;
                    // // console.log(product_name);
                    // qty = a.qty; 
                    // total = 0;
                    // if (a.total != null){
                    // total = a.total;
                    // }
                    // //console.log("========="+product_name);
                    // for (var b in product_all){
                    //     if(b.name == product_name){
                    //         barcode == b.barcode
                    //         selling_price == b.selling_price
                    //     }
                    // }
                    // // if (invoice_sale == invoice){
                    //     receipt_body +=
                    //         `<tr>
                    //             <td class="barcode">${barcode}</td>
                    //             <td class="product_name">${product_name}</td>
                    //             <td class="selling_price">${selling_price}</td>
                    //             <td class="qty">${qty}</td>
                    //             <td class="total">${total}</td>
                    //         </tr>`;
            })
            // for (var a in data_2){
            //     //console.log(a);
            //     invoice_sale = a.invoice;
            //     product_name = a.product_id;
            //     // console.log(product_name);
            //     qty = a.qty; 
            //     total = 0;
            //     if (a.total != null){
            //     total = a.total;
            //     }
            //     //console.log("========="+product_name);
            //     for (var b in product_all){
            //         if(b.name == product_name){
            //             barcode == b.barcode
            //             selling_price == b.selling_price
            //         }
            //     }
            //     // if (invoice_sale == invoice){
            //         receipt_body +=
            //             `<tr>
            //                 <td class="barcode">${barcode}</td>
            //                 <td class="product_name">${product_name}</td>
            //                 <td class="selling_price">${selling_price}</td>
            //                 <td class="qty">${qty}</td>
            //                 <td class="total">${total}</td>
            //             </tr>`;
            //     // }
            // }
            //receipt_all += receipt_header + receipt_body 

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
                            ${receipt_all}
                            <tr>
                                <td></td>
                                <td style="border-top:1px dashed black;" colspan="3"></td>
                            </tr>
                            <tr>
                                <td>
                                <td>OMSET</td>
                                <td>: Rp. ${income}</td>
                            </tr>
                            <tr>
                                <td>
                                <td>KEUNTUNGAN</td>
                                <td>: Rp. ${profit}</td>
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


    // var myPrintWindow = window.open('', 'Cetak Receipt', '');
    // myPrintWindow.document.write(receipt_css);
    // myPrintWindow.document.write(receipt);
    // myPrintWindow.document.close();
    // myPrintWindow.focus();
    // myPrintWindow.print();
    // myPrintWindow.close();
    // return false;
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
    console.log($('#date-picker-range').val());
})


jQuery(document).ready(function() {
    KTDatatablesDataSourceAjaxServer.init();
});