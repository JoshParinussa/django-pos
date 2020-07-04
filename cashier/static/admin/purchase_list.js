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
        console.log(dates);
        return dates
    }

    var initTable = function() {
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
                [1, "dsc"]
            ],
            ajax: {
                'type': 'GET',
                'url': '/v1/purchase?format=datatables',
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
                    targets: -1,
                    title: 'Actions',
                    orderable: false,
                    render: function(data, type, row) {
                        return `<a href="purchase/update/${row.id}" target="_blank" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Variant List">
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
                { data: 'Actions', searchable: false, orderable: false, responsivePriority: -1 }
            ],
        });

    };

    var initEvents = function() {
        $('#btn-filter-date').on('click', function(e) {
            console.log(getDaterange());
            table.api().ajax.reload();
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