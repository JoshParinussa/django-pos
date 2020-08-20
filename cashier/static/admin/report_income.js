"use strict";
var table;
var dates;
window.csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

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

    var initTable = function() {
        table = $('.data-table');
        table.dataTable({
            responsive: true,
            searchDelay: 500,
            processing: true,
            serverSide: true,
            autoWidth: false,
            serverSide: true,
            pageLength: 10,
            ordering: true,
            paging: true,
            order: [
                [0, "asc"]
            ],
            ajax: {
                'type': 'GET',
                'url': '/v1/income?format=datatables',
                'data': function(d) {
                    d.date_range = getDaterange();
                }
            },
            columnDefs: [{
                    targets: 0,
                    render: function(data) {
                        return !$.trim(data) ? '' : data;
                    }
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
                        return !$.trim(data) ? '' : data;
                    }
                },
                {
                    targets: 4,
                    render: function(data) {
                        return !$.trim(data) ? '' : Number(data).toLocaleString('id-ID');
                    }
                },
                {
                    targets: -1,
                    title: 'Actions',
                    orderable: false,
                    render: function(data, type, row) {
                        return `<a href="income/${row.id}" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Variant List">
                          <i class="nav-icon fas fa-edit"></i>
                    </a>`;
                    },
                },
            ],
            columns: [
                { data: 'invoice', orderable: true, searchable: true, name: 'invoice' },
                { data: 'date', orderable: true, searchable: true, name: 'date' },
                { data: 'cashier', orderable: true, searchable: true, name: 'cashier' },
                { data: 'keterangan', orderable: true, searchable: true, name: 'keterangan' },
                { data: 'jumlah_pemasukan', orderable: true, searchable: true, name: 'jumlah_pemasukan' },
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
                url: "/v1/income/print_report",
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
            initTable();
            initEvents();
        },

    };

}();

jQuery(document).ready(function() {
    KTDatatablesDataSourceAjaxServer.init();
});