"use strict";
var KTDatatablesDataSourceAjaxServer = function() {

    var initTable1 = function() {
        var table = $('.data-table');
        // begin first table
        table.DataTable({
            serverSide: true,
            pageLength: 10,
            order: [
                [0, "asc"]
            ],
            ajax: {
                'type': 'GET',
                'url': '/v1/report_out_of_stock?format=datatables',
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
                        return !$.trim(data) ? '' : data;
                    }
                },
            ],
            columns: [
                { data: 'name', orderable: true, searchable: true, name: 'name' },
                { data: 'stock', orderable: true, searchable: true, name: 'stock' },
            ],
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

jQuery(document).ready(function() {
    KTDatatablesDataSourceAjaxServer.init();
});