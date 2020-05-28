"use strict";
var KTDatatablesDataSourceAjaxServer = function() {

    var initTable1 = function() {
        var table = $('.data-table');
        // begin first table
        table.DataTable({
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
                'url': '/v1/supplier?format=datatables',
            },
            columnDefs: [{
                    targets: 0,
                    render: function(data) {
                            console.log(data);
                            return !$.trim(data) ? '' : data;
                        }
                        // render: function(data, type, row){
                        // 	return `<a href="products/${row.id}" title="Product Details">${data}</a>`;
                        // }
                },
                {
                    targets: 1,
                    render: function(data) {
                        console.log(data);
                        return !$.trim(data) ? '' : data;
                    }
                },
                {
                    targets: 2,
                    render: function(data) {
                        console.log(data);
                        return !$.trim(data) ? '' : data;
                    }
                },
                {
                    targets: 3,
                    render: function(data) {
                        console.log(data);
                        return !$.trim(data) ? '' : data;
                    }
                },
                {
                    targets: 4,
                    render: function(data) {
                        console.log(data);
                        return !$.trim(data) ? '' : data;
                    }
                },
                {
                    targets: -1,
                    title: 'Actions',
                    orderable: false,
                    render: function(data, type, row) {
                        return `<a href="supplier/${row.id}" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Variant List">
                          <i class="nav-icon fas fa-edit"></i>
                    </a>`;
                    },
                },
            ],
            columns: [
                { data: 'company_name', orderable: true, searchable: true, name: 'company_name' },
                { data: 'address', orderable: true, searchable: true, name: 'address' },
                { data: 'contact_person', orderable: true, searchable: true, name: 'contact_person' },
                { data: 'office_phone', orderable: true, searchable: true, name: 'office_phone' },
                { data: 'phone', orderable: true, searchable: true, name: 'phone' },
                { data: 'Actions', searchable: false, orderable: false, responsivePriority: -1 }
            ],
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