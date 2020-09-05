'use strict';
window.csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
var dates;
// Class definition
var KTDatatableChildDataLocalDemo = function() {
    // Private functions
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

    var subTableInit = function(e) {
        $('<div/>').attr('id', 'child_data_local_' + e.data.id).appendTo(e.detailCell).KTDatatable({
            data: {
                type: 'local',
                source: e.data.purchase_invoice,
                pageSize: 5,
            },

            // layout definition
            layout: {
                scroll: true,
                height: 400,
                footer: false,
            },

            sortable: true,

            // columns definition
            columns: [{
                field: 'barcode',
                title: 'Bacode',

            }, {
                field: 'product',
                title: 'Produk',
            }, {
                field: 'purchase_price',
                title: 'Harga Beli',
                template: function(row) {
                    return '<span>' + Number(row.purchase_price).toLocaleString('id-ID') + '</span>';
                },
            }, {
                field: 'qty',
                title: 'Qty',
            }, {
                field: 'total',
                title: 'Total',
                type: 'number',
                template: function(row) {
                    return '<span>' + Number(row.total).toLocaleString('id-ID') + '</span>';
                },
            }],
        });
    };

    // demo initializer
    var mainTableInit = function() {

        var date = moment.utc().format('YYYY-MM-DD HH:mm:ss');
        var stillUtc = moment.utc(date).toDate();
        var local = moment(stillUtc).local().format('YYYY-MM-DD HH:mm:ss');

        var datatable = $('#kt_datatable').KTDatatable({
            data: {
                type: 'remote',
                source: {
                    read: {
                        url: '/v1/report_supplier/set_datatable?format=datatables',
                        data: {
                            'date_range': ctx_dates.length === 0 ? getDaterange() : ctx_dates,
                            'pk': pk
                        }
                    },
                },
                pageSize: 10, // display 20 records per page
                serverPaging: true,
                serverFiltering: false,
                serverSorting: true,
            },

            // layout definition
            layout: {
                scroll: false,
                height: null,
                footer: false,
            },

            sortable: true,

            filterable: false,

            pagination: true,

            detail: {
                title: 'Load sub table',
                content: subTableInit,
            },

            search: {
                input: $('#kt_datatable_search_query'),
                key: 'generalSearch'
            },

            // columns definition
            columns: [{
                field: 'id',
                title: '',
                sortable: false,
                width: 30,
                textAlign: 'center',
            }, {
                field: 'invoice',
                title: 'Invoice',
            }, {
                field: 'cashier',
                title: 'Kasir',
            }, {
                field: 'date',
                title: 'Tanggal',
                template: function(row) {
                    return '<span>' + moment.utc(row.date).local().format('LLL') + '</span>';
                }
            }, {
                field: 'total',
                title: 'Total',
                type: 'number',
                template: function(row) {
                    return '<span>' + Number(row.total).toLocaleString('id-ID') + '</span>';
                },
            }, {
                field: 'report_status',
                title: 'Status',
                // callback function support for column rendering
                template: function(row) {
                    var status = {
                        1: { 'title': 'Pending', 'class': 'kt-badge kt-badge--warning kt-badge--inline kt-badge--pill' },
                        2: { 'title': 'Selesai', 'class': 'kt-badge kt-badge--success kt-badge--inline kt-badge--pill' },
                        3: { 'title': 'Batal', 'class': 'kt-badge kt-badge--danger kt-badge--inline kt-badge--pill' },
                    };
                    return '<span class="' + status[row.report_status].class + '">' + status[row.report_status].title + '</span>';
                },
            }, {
                field: 'report_payment_status',
                title: 'Pembayaran',
                autoHide: false,
                // callback function support for column rendering
                template: function(row) {
                    var status = {
                        1: { 'title': 'Hutang', 'class': 'kt-badge kt-badge--warning kt-badge--inline kt-badge--pill' },
                        2: { 'title': 'Cash', 'class': 'kt-badge kt-badge--primary kt-badge--inline kt-badge--pill' },
                    };
                    return '<span class="' + status[row.report_payment_status].class + '">' + status[row.report_payment_status].title + '</span>';
                },
            }, {
                field: 'Actions',
                width: 130,
                title: 'Actions',
                sortable: false,
                overflow: 'visible',
                template: function(row) {
                    return `<a href="../../transaction/purchase/update/${row.id}" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Lihat pembelian">
                          <i class="nav-icon fas fa-edit"></i>
                    </a>`;
                },
            }],
        });

        $('#kt_datatable_search_status').on('change', function() {
            datatable.search($(this).val(), 'report_status');
        });

        $('#kt_datatable_search_type').on('change', function() {
            datatable.search($(this).val(), 'report_payment_status');
        });

        $('#kt_datatable_search_status, #kt_datatable_search_type').selectpicker();

        $('#btn-filter-date').on('click', function(e) {
            $.redirect('/dash/report/supplier/' + pk, { 'dates': getDaterange() }, "GET");
        });
    };

    // var initEvents = function() {

    // };

    return {
        // Public functions
        init: function() {
            initDateRangePicker();
            mainTableInit();
            // initEvents();
        },
    };
}();

jQuery(document).ready(function() {
    KTDatatableChildDataLocalDemo.init();
});