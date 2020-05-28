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
                [1, "dsc"]
            ],
            ajax: {
                'type': 'GET',
                'url': '/v1/invoice?format=datatables',
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
                        return `<a href="sale/update/${row.id}" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Variant List">
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