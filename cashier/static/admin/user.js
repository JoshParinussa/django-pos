"use strict";

var KTDatatablesDataSourceAjaxServer = function() {


    var initTable1 = function() {

        var table = $('.data-table');
        if (!table.length) return;

        // begin first table
        table.DataTable({
            responsive: true,
            // scrollX: true,
            autoWidth: false,
            serverSide: true,
            pageLength: 50,
            order: [
                [3, "desc"]
            ],
            ajax: {
                'type': 'GET',
                'url': '/v1/employees?format=datatables',
                // 'dataSrc': 'data.users'
            },
            columnDefs: [{
                    targets: 0,
                    render: function(data, type, row) {
                        return !$.trim(data) ? '' : data;
                    }
                },
                {
                    targets: 1,
                    render: function(data) {
                        var d = moment(data).format("ll");
                        return d;
                    }
                },
                {
                    targets: 2,
                    render: function(data) {
                        if (data === true) {
                            return '<span class="kt-badge kt-badge--info kt-badge--inline kt-badge--pill">Admin</span>';
                        } else {
                            return '<span class="kt-badge kt-badge--warning kt-badge--inline kt-badge--pill">Pegawai</span>';
                        }
                    }
                },
                {
                    targets: 3,
                    render: function(data) {
                        if (data === true) {
                            return '<span class="kt-badge kt-badge--primary kt-badge--dot"></span>&nbsp;<span class="kt-font-bold kt-font-primary">Active</span>';
                        } else {
                            return '<span class="kt-badge kt-badge--danger kt-badge--dot"></span>&nbsp;<span class="kt-font-bold kt-font-danger">Inactive</span>';
                        }
                    }
                },
                {
                    targets: -1,
                    title: 'Actions',
                    orderable: false,
                    render: function(data, type, row) {
                        return `<a href="users/${row.id}" class="btn btn-sm btn-clean btn-icon btn-icon-md" title="Edit User">
                          <i class="nav-icon fas fa-edit"></i>
                    </a>`;
                    },
                },
            ],
            columns: [
                { data: 'email', orderable: true, searchable: true, name: 'email' },
                { data: 'date_joined', orderable: true, searchable: false },
                { data: 'is_superuser', orderable: true, searchable: false },
                { data: 'is_active', orderable: true, searchable: false },
                { data: 'Actions', searchable: false, orderable: false, responsivePriority: -1 }
            ]
        });
    };
    return {

        //main function to initiate the module
        init: function() {
            initTable1();
        },

    };

}();

// Class definition
// var UserCreate = function () {
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
//             initValidation();
//             $('.select2').select2();
//         }
//     };
// }();

jQuery(document).ready(function() {
    // UserCreate.init();
    KTDatatablesDataSourceAjaxServer.init();
});