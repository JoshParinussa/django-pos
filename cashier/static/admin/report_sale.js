"use strict";
window.csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
var itemBarcode;
var itemName;
var itemPrice;
var grandTotal = 0;

var row;
var table;

$(document.body).addClass('kt-aside--minimize');

var raw_date = moment(SaleDate, 'LLL').format('YYYY-MM-DD HH:mm:ss')
var sale_date = moment.utc(raw_date).local().format('LLL');
$('#sale-date').val(sale_date);

var KTDatatablesDataSourceAjaxServer = function() {

    var initTable1 = function() {
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
                [0, "asc"]
            ],
            ajax: {
                'type': 'POST',
                'url': '/v1/report_sale/get_by_invoice?format=datatables',
                'data': { 'invoice': currentInvoiceID },
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
                    targets: -1,
                    title: 'Actions',
                    orderable: false,
                    render: function(data, type, row) {
                        return "<span onclick='updateItem(this)' class='btn btn-sm btn-clean btn-icon btn-icon-md' data-toggle='modal' data-target='#modal-default' title='Edit item'>" +
                            "<i class='la la-edit'></i>" +
                            "</span>" +
                            "<span onclick='deleteItem(this)' class='btn btn-sm btn-clean btn-icon btn-icon-md btn-delete' title='Hapus item' id='btn-delete' data-toggle='modal' data-target='#modal-box'>" +
                            "<i class='la la-trash'></i>" +
                            "</span>";
                    },
                },
            ],
            columns: [
                { data: 'barcode', orderable: true, searchable: true, name: 'barcode' },
                { data: 'product', orderable: true, searchable: true, name: 'product' },
                { data: 'price', orderable: true, searchable: true, name: 'price' },
                { data: 'qty', orderable: true, searchable: true, name: 'qty' },
                { data: 'total', orderable: true, searchable: true, name: 'total' },
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

var updateItem = function(e) {
    row = table.api().row($(e).closest('tr')).data();
    $('#modal-item-name').val(row.product);
    $('#modal-qty-item-cart').val(row.qty);
    $('#modal-barcode').val(row.barcode);
}

$('#modal-btn-update').click(function(e) {
    var newQty = $('#modal-qty-item-cart').val();
    var newTotal = Number(newQty) * Number(row.price);
    var oldTotal = Number(row.qty) * Number(row.price);
    var diffTotal = oldTotal - newTotal;
    var oldChange = Number(InvoiceChange);
    var Cash = Number(InvoiceCash);
    var Total = Number(InvoiceGrandTotal) - diffTotal;
    var diffChange, newChange = 0;
    var diffQty = Number(row.qty - newQty);

    if (Total > Cash) {
        Cash = Total;
        newChange = 0;
    } else if ((Cash - Total) != 0) {
        newChange = Cash - Total;
        diffChange = newChange - oldChange;
    }

    InvoiceChange = newChange;
    InvoiceCash = Cash;

    $.ajax({
        type: "POST",
        url: "/v1/report_sale/update_item",
        data: {
            "invoice_number": currentInvoiceID,
            "barcode": $('#modal-barcode').val(),
            "qty": newQty,
            'total': newTotal,
            'grand_total': InvoiceGrandTotal,
            'cash': InvoiceCash,
            'change': InvoiceChange,
            'diffQty': diffQty
        },
        success: function(result) {
            if (Total > Cash) {
                alert("Uang kurang Rp. " + newChange);
            } else if (diffChange < 0) {
                alert("Kembalian tambah Rp. " + diffChange);
            } else if (diffChange > 0) {
                alert("Kembalian kurang Rp. " + Math.abs(diffChange));
            }

            $('#modal-default').modal('toggle');
            InvoiceGrandTotal = Number(result['grand_total']);
            $('#grand_total').text(InvoiceGrandTotal);
            $('#change').val(InvoiceChange);
            $('#cash').val(InvoiceCash);
            table.api().ajax.reload();
        }
    });
});

var deleteItem = function(e) {
    row = table.api().row($(e).closest('tr')).data();
    $('#modal-item-name-delete').html(row.product);
}

$('#modal-btn-delete').click(function(e) {
    var row_barcode = row.barcode;
    var Change = Number(InvoiceChange);
    var oldTotal = Number(row.qty) * Number(row.price);
    InvoiceGrandTotal = Number(InvoiceGrandTotal) - oldTotal;
    InvoiceChange = Number(InvoiceCash) - Number(InvoiceGrandTotal);
    var diffChange = Number(InvoiceChange) - Change;
    $.ajax({
        type: "POST",
        url: "/v1/report_sale/delete_item",
        data: {
            "invoice_number": currentInvoiceID,
            "barcode": row_barcode,
            "total": InvoiceGrandTotal,
            "change": InvoiceChange,
            "qty": row.qty
        },
        success: function(e) {
            alert("Kembalian tambah Rp. " + diffChange);
            $('#grand_total').text(InvoiceGrandTotal);
            $('#change').text(InvoiceChange);
            $('#cash').text(InvoiceCash);
            table.api().ajax.reload();
            $('#modal-box').modal('toggle');
        }
    });
});

$('#process_payment').click(function(e) {
    window.location.replace("/dash/report/transaction");
});

$('#btn-print-payment').click(function() {
    printResult()
});

var printResult = function() {
    var total = $('#grand_total').html()
    var receipt_body = ''
    $("#item_table tbody").find("tr").each(function() {
        var item = $(this).find('.product-name').html()
        var qty = $(this).find('.qty').html()
        var price = Number($(this).find('.price').attr('data-price')).toLocaleString('id-ID')
        var subtotal = Number($(this).find('.purchase_total').attr('data-purchase-total')).toLocaleString('id-ID')
        receipt_body +=
            `<tr>
                <td class="item">${item}</td>
                <td class="quantity">${qty}</td>
                <td class="price">${price}</td>
                <td class="subtotal">${subtotal}</td>
            </tr>`;
    });

    var receipt =
        `<div class="print-receipt">
            <div class="col-12">
                <div class="row center">
                    <h3>Minimarketku</div>
                </div>
                <div class="information">
                    ${date}<br>
                    ${invoice_number}<br>
                    ${currentUser}, siap melayani!<br><br>
                </div>
                <div class="row">
                    <table style="border-top:1px dashed black;">
                        <tbody>
                            
                            <tr>
                            </tr>
                            ${receipt_body}
                            <tr>
                                <td></td>
                                <td style="border-top:1px dashed black;" colspan="3"></td>
                            </tr>
                            <tr>
                                <td>
                                <td colspan="2">HARGA JUAL</td>
                                <td>: ${grandTotal.toLocaleString('id-ID')}</td>
                            </tr>
                            <tr>
                                <td>
                                <td colspan="2">TUNAI </td>
                                <td>: ${Number(cash).toLocaleString('id-ID')}</td>
                            </tr>
                            <tr>
                                <td>
                                <td colspan="2">KEMBALIAN </td>
                                <td>: ${change.toLocaleString('id-ID')}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="row center">
                <br><br><br>
                    <p>===== TERIMA KASIH =====</p>
                    <p>SELAMAT BERBELANJA KEMBALI</p>
                </div>
            </div>
        </div>`;

    var receipt_css =
        `<style type="text/css">
            @page {margin: 10;}
            .print-receipt {
                width: 58mm;
            }
            .center {
                text-align: center;
                font-size: 12px;
              }
            .information {
                text-align: center;
                line-height: normal;
                font-size: 8px;
            }
            table, th, td {
            font-size: 12px;
            }
            table {width:100%;}
            td .item {width:50%;}
            td .quantity {width:10%;}
            td .price {width:20%;}
            td .subtotal {width:20%;}
            
        </style>`;


    var myPrintWindow = window.open('', 'Cetak Receipt', '');
    myPrintWindow.document.write(receipt_css);
    myPrintWindow.document.write(receipt);
    myPrintWindow.document.close();
    myPrintWindow.focus();
    myPrintWindow.print();
    myPrintWindow.close();
    return false;
}

jQuery(document).ready(function() {
    KTDatatablesDataSourceAjaxServer.init();
});