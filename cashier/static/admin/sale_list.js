"use strict";
var KTDatatablesDataSourceAjaxServer = function() {

    var initTable = function() {
        var table = $('.data-table');
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
            order: [
                [0, "asc"]
            ],
            ajax: {
                'type': 'GET',
                'url': '/v1/invoice?format=datatables',
            },
            columnDefs: [{
                    targets: 0,
                    render: function(data, type, row) {
                        // console.log(data.invoice)
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
                        return !$.trim(data) ? '' : data == 1 ? 'SUCCESS' : 'ONPROCESS';
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
                { data: 'invoice', orderable: true, searchable: true, name: 'invoice' },
                { data: 'date', orderable: true, searchable: true, name: 'date' },
                { data: 'cashier', orderable: true, searchable: true, name: 'cashier' },
                { data: 'total', orderable: true, searchable: true, name: 'total' },
                { data: 'status', orderable: true, searchable: true, name: 'status' },
                { data: 'Actions', searchable: false, orderable: false, responsivePriority: -1 }
            ],
        });

    };
    return {
        init: function() {
            initTable();
        },
    };
}();

jQuery(document).ready(function() {
    KTDatatablesDataSourceAjaxServer.init();
});