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
        var date = moment.utc().format('YYYY-MM-DD HH:mm:ss');
        // console.log(date); // 2015-09-13 03:39:27
        var stillUtc = moment.utc(date).toDate();
        var local = moment(stillUtc).local().format('YYYY-MM-DD HH:mm:ss');

        // console.log(local); // 2015-09-13 09:39:27
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
                'url': '/v1/report_purchase/set_datatable?format=datatables',
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
                        return !$.trim(data) ? '' : moment.utc(data).local().format('LLL');
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
                        return !$.trim(data) ? '' : Number(data).toLocaleString('id-ID');
                    }
                },
                {
                    targets: 4,
                    render: function(data) {
                        return !$.trim(data) ? '' : Number(data).toLocaleString('id-ID');
                    }
                },
                {
                    targets: 5,
                    render: function(data) {
                        return !$.trim(data) ? '' : data == 1 ?
                            '<span class="kt-badge kt-badge--success     kt-badge--inline kt-badge--pill">Success</span>' :
                            '<span class="kt-badge kt-badge--warning kt-badge--inline kt-badge--pill">On Process</span>';
                    }
                },
                {
                    targets: -1,
                    title: 'Actions',
                    orderable: false,
                    render: function(data, type, row) {
                        return `<a href="../report/purchase/${row.id}" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Detail">
                          <i class="nav-icon fas fa-edit"></i>
                    </a>`;
                    },
                },
            ],
            columns: [
                { data: 'invoice', orderable: true, searchable: true, name: 'invoice' },
                { data: 'date', orderable: true, searchable: true, name: 'date' },
                { data: 'cashier', orderable: true, searchable: true, name: 'cashier' },
                { data: 'supplier', orderable: true, searchable: true, name: 'supplier' },
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
        $('#btn-print-report').on('click', function(e) {
            var table_body = '';
            var date_range = getDaterange();
            $.ajax({
                type: "POST",
                url: "/v1/purchase/print_report",
                data: {
                    'date_range': date_range
                },
                success: function(result) {
                    table_body +=
                        `<tr>
                            <th>Tgl</th>
                            <th>Invoice</th>
                            <th>Cashier</th>
                            <th>Barcode</th>
                            <th>Produk</th>
                            <th>Harga Satuan</th>
                            <th>Qty</th>
                            <th>Total Harga</th>
                        </tr>`
                    $.each(result, function(key, value) {
                        var date = value['date'];
                        var invoice = value['invoice'];
                        var cashier = value['cashier'];
                        var sales = value['invoice_sale'];
                        var total_harga = value['total']
                        $.each(sales, function(key, value) {
                            var barcode = value['barcode']
                            var product = value['product']
                            var price = value['price']
                            var qty = value['qty']
                            var total = value['total']
                            if (key == 0) {
                                table_body +=
                                    `<tr>
                                        <td>${date}</td>
                                        <td>${invoice}</td>
                                        <td>${cashier}</td>
                                        <td class="barcode">${barcode}</td>
                                        <td class="product">${product}</td>
                                        <td class="price">${price}</td>
                                        <td class="qty">${qty}</td>
                                        <td class="total">${total}</td>
                                    </tr>`;
                            } else {
                                table_body +=
                                    `<tr class="bottom">
                                        <td></td>
                                        <td></td>
                                        <td></td>
                                        <td class="barcode">${barcode}</td>
                                        <td class="product">${product}</td>
                                        <td class="price">${price}</td>
                                        <td class="qty">${qty}</td>
                                        <td class="total">${total}</td>
                                    </tr>`;
                            }
                        });
                        table_body +=
                            `<tr class="bottom">
                                <th>Total</th>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td>${total_harga}</td>
                            </tr>
                            <tr></tr>
                            <tr></tr>`;
                    });
                    var report =
                        `<div class="print-receipt">
                            <div class="col-12">
                                <div class="row center">
                                    <h3>Laporan Penjualan</h3>
                                    <h4>Periode: ${date_range[0]} - ${date_range[1]}</h4>
                                </div>
                                <div class="row">
                                    <table class="table top">
                                        <tbody>
                                            ${table_body}
                                        </tbody>
                                    </table>
                                </div>
                        </div>`;

                    var receipt_css =
                        `<style type="text/css">
                            @page {margin: 20;}
                            
                            table.top{
                                border-top:1px dashed black;
                            }
                            .center {
                                text-align: center;
                                font-size: 12px;
                              }
                            td .bottom{
                                border-bottom:1px solid black;
                            }
                            table, th, td {
                                font-size: 12px;
                                text-align: left;
                            }
                            table {width:100%;}
                            td .barcode {width:20%;}
                            td .product {width:20%;}
                            td .price {width:20%;}
                            td .qty {width:20%;}
                            td .total {width:20%;}
                            
                        </style>`;

                    var myPrintWindow = window.open('', 'Cetak Laporan Penjualan', '');
                    myPrintWindow.document.write(receipt_css);
                    myPrintWindow.document.write(report);
                    myPrintWindow.document.close();
                    myPrintWindow.focus();
                    myPrintWindow.print();
                    myPrintWindow.close();
                }
            });



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
    // $.ajax({
    //     type: "POST",
    //     url: "/v1/report_transaction/set_income_profit",
    //     data: {
    //         'date': condition
    //     },
    //     success: function(result) {
    //         $('#income').html('Rp. ' + result.income);
    //         $('#profit').html('Rp. ' + result.profit);
    //         income = result.income;
    //         profit = result.profit;
    //         currentDate = result.date;
    //         data_2 = result.data_2;
    //         product_all = result.product;
    //     }
    // });
    $.ajax({
        type: "POST",
        url: "/v1/report_purchase/set_datatable?format=datatables",
        data: function(data) {
            data.date = condition;
        },
        success: function(result) {
            table.api().ajax.reload();
        }
    });
});


jQuery(document).ready(function() {
    KTDatatablesDataSourceAjaxServer.init();
});