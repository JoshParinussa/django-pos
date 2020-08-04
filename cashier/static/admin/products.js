"use strict";
var KTDatatablesDataSourceAjaxServer = function() {

    var initTable1 = function() {
        var table = $('.data-table');
        table.DataTable({
            // autoWidth: false,
            // processing: true,
            serverSide: true,
            pageLength: 10,
            // ordering: true,
            // paging: true,
            // scrollX: true,
            order: [
                [0, "asc"]
            ],
            ajax: {
                'type': 'GET',
                'url': '/v1/products?format=datatables',
                // 'url': '/v1/products',
                // 'dataSrc': 'data.results'
            },
            columnDefs: [{
                    targets: 0,
                    render: function(data, type, row) {
                        return `<a href="products/${row.id}/converts/get_by_product" title="Convert">
                          ` + (!$.trim(data) ? '' : data) + `
                    </a>`;
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
                        return !$.trim(data) ? '' : data;
                    }
                },
                {
                    targets: 5,
                    render: function(data) {
                        return !$.trim(data) ? '' : data;
                    }
                },
                {
                    targets: 6,
                    render: function(data) {
                        return !$.trim(data) ? '' : data;
                    }
                },
                {
                    targets: -1,
                    title: 'Actions',
                    orderable: false,
                    render: function(data, type, row) {
                        return `<a href="products/${row.id}" class="product btn btn-sm btn-clean btn-icon btn-icon-md" id="product" title="Variant List">
                          <i class="nav-icon fas fa-edit"></i>
                        </a>`;
                    },
                },
            ],
            columns: [
                { data: 'name', orderable: true, searchable: true, name: 'name' },
                { data: 'barcode', orderable: true, searchable: true, name: 'barcode' },
                { data: 'stock', orderable: true, searchable: false, name: 'stock' },
                { data: 'category', orderable: true, searchable: false, name: 'category.name' },
                { data: 'unit', orderable: true, searchable: false, name: 'unit' },
                { data: 'purchase_price', orderable: true, searchable: false, name: 'purchase_price' },
                { data: 'selling_price', orderable: true, searchable: false, name: 'selling_price' },
                { data: 'Actions', searchable: false, orderable: false, responsivePriority: -1 }
            ],
        });
        $("#sidebar").on('click', function(e) {
            var table = $('#example1').DataTable();
            table.columns.adjust().draw();
            $(".dataTables_scrollHeadInner .dataTables_scrollHead .table").css("width", "100%");
        });

    };
    return {
        init: function() {
            initTable1();
        },

    };

}();

jQuery(document).ready(function() {
    KTDatatablesDataSourceAjaxServer.init();
});