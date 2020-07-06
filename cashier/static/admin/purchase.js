"use strict";
window.csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

$(document.body).addClass('kt-aside--minimize');

var itemBarcode;
var itemName;
var itemPrice;
var purchaseItemQty;
var purchaseItemTotal;
let lineNo = 1;
var invoice_number = $('#invoice_number').text();
var grandTotal = 0;
var cash = 0;
var change = 0;

//Modal
var row;


var date = moment().format('LLL');
$('#purchase-date').val(date);
$('#cashier').val(currentUser);

var emptyingCashChange = function() {
    $('#cash').val('');
}

var getProductByBarcode = function() {
    var barcode = $('#barcode').val();

    if (barcode.length > 0) {
        $.ajax({
            type: "POST",
            url: "/v1/products/get_by_barcode",
            data: {
                'barcode': barcode
            },
            success: function(result) {
                if (result.length > 0) {
                    var data = result[0]
                    itemBarcode = data.barcode;
                    itemName = data.name;
                    itemPrice = data.purchase_price;
                    drawPurchaseRow();
                    $('#barcode').val(null);
                } else {
                    alert("Product not found");
                }
            }
        });
    }
}

var drawPurchaseRow = function() {
    purchaseItemQty = 1
    var supplier = $('#supplier').val()
        // purchaseItemTotal = itemPrice * purchaseItemQty;

    $.ajax({
        type: "POST",
        url: "/v1/purchase_detail/add_item",
        data: {
            "invoice_purchase": invoice_number,
            "barcode": itemBarcode,
            "qty": purchaseItemQty,
            "supplier": supplier
        },
        success: function(result) {
            var idRow = itemBarcode;
            var purchaseItemTotal = Number(result.purchase.total);
            var purchaseItemPrice = Number(result.price);
            if ($('#item_table').find("#" + idRow).length > 0) {
                var currentQty = $('#item_table').find("#" + idRow + " .qty").html();
                var currentTotal = $('#item_table').find("#" + idRow + " .purchase_total").attr('data-purchase-total');
                grandTotal -= Number(currentTotal);
                grandTotal += purchaseItemTotal;
                var newQty = Number(currentQty) + Number(purchaseItemQty);

                $('#item_table').find("#" + idRow + " .qty").text(newQty);
                $('#item_table').find("#" + idRow + " .purchase_total").attr('data-purchase-total', purchaseItemTotal);
                $('#item_table').find("#" + idRow + " .purchase_total").text(purchaseItemTotal.toLocaleString('id-ID'));
                $('#item_table').find("#" + idRow + " .price").text(purchaseItemPrice.toLocaleString('id-ID'));



            } else {
                var row = "<tr id='" + idRow + "'" + itemBarcode + "'>" +
                    "<td class='product-barcode' style='display:none;'>" + itemBarcode + "</td>" +
                    "<td class='product-name'>" + itemName + "</td>" +
                    "<td class='price' data-price='" + purchaseItemPrice + "'>" + purchaseItemPrice.toLocaleString('id-ID') + "</td>" +
                    "<td class='qty'>" + purchaseItemQty + "</td>" +
                    "<td class='purchase_total' data-purchase-total='" + purchaseItemTotal + "'>" + purchaseItemTotal.toLocaleString('id-ID') + "</td>" +
                    "<td>" +
                    "<span onclick='updateItem(this)' class='btn btn-sm btn-clean btn-icon btn-icon-md' data-toggle='modal' data-target='#modal-default' title='Edit item'>" +
                    "<i class='la la-edit'></i>" +
                    "</span>" +
                    "<span onclick='deleteItem(this)' class='btn btn-sm btn-clean btn-icon btn-icon-md' title='Hapus item'>" +
                    "<i class='la la-trash'></i>" +
                    "</span>" +
                    "</td>" +
                    "</tr>";
                var tableBody = $("#item_table tbody");
                tableBody.append(row);
                grandTotal += Number(purchaseItemTotal);
                lineNo++;
            }
            $('#grand_total').text(grandTotal.toLocaleString('id-ID'));
            $('#sub-total').text(grandTotal.toLocaleString('id-ID'));
        }
    });
}

var getInvoicePurchaseItem = function() {
    $.ajax({
        type: "POST",
        url: "/v1/purchase_detail/get_by_invoice?format=datatables",
        data: {
            "invoice_purchase": invoice_number,
        },
        success: function(result) {
            try {
                var invoice_data = result.data['purchase'][0];
                console.log(invoice_data['supplier'])
                $('#supplier').val(invoice_data['supplier'])
                date = moment.utc(invoice_data['date']).local().format('LLL');
                $('#purchase-date').val(date);
                var purchase_items = result.data['purchase_items'];

                purchase_items.forEach(function(item) {
                    grandTotal += Number(item.total);
                    var idRow = item.barcode;
                    var currentQty = $('#item_table').find("#" + idRow + " .qty").html();
                    var currentPurchaseTotal = $('#item_table').find("#" + idRow + " .purchase_total").html();

                    if ($('#item_table').find("#" + idRow).length > 0) {
                        var currentQty = $('#item_table').find("#" + idRow + " .qty").html();
                        var currentPurchaseTotal = $('#item_table').find("#" + idRow + " .purchase_total").html();

                        var newQty = Number(currentQty) + Number(item.qty);
                        var newPurchaseTotal = Number(currentPurchaseTotal) + Number(item.total);

                        $('#item_table').find("#" + idRow + " .qty").text(newQty);
                        $('#item_table').find("#" + idRow + " .purchase_total").text(newPurchaseTotal.toLocaleString('id-ID'));
                    } else {
                        var row = "<tr id='" + item.barcode + "'>" +
                            // "<td>" + lineNo + "</td>" +
                            "<td class='product-barcode' style='display:none;'>" + item.barcode + "</td>" +
                            "<td class='product-name'>" + item.product + "</td>" +
                            "<td class='price' data-price='" + item.price + "'>" + Number(item.price).toLocaleString('id-ID') + "</td>" +
                            "<td class='qty'>" + item.qty + "</td>" +
                            "<td class='purchase_total' data-purchase-total='" + item.total + "'>" + Number(item.total).toLocaleString('id-ID') + "</td>" +
                            "<td class='col-actions'>" +
                            "<span onclick='updateItem(this)' class='btn btn-sm btn-clean btn-icon btn-icon-md' data-toggle='modal' data-target='#modal-default' title='Edit item'>" +
                            "<i class='la la-edit'></i>" +
                            "</span>" +
                            "<span onclick='deleteItem(this)' class='btn btn-sm btn-clean btn-icon btn-icon-md btn-delete' title='Hapus item'>" +
                            "<i class='la la-trash'></i>" +
                            "</span>" +
                            "</td>" +
                            "</tr>";
                        var tableBody = $("#item_table tbody");
                        tableBody.append(row)
                        lineNo++;
                    }
                })
                $('#grand_total').text(Number(grandTotal).toLocaleString('id-ID'));
                $('#sub-total').text(Number(grandTotal).toLocaleString('id-ID'));

                if (invoice_data['status'] == 1) {
                    $('.alert-status').attr("hidden", false);
                    $('#process_payment').attr("disabled", true);
                    $('#supplier').attr("disabled", true);
                    $('#cash').attr("disabled", true);
                    var item_table = $('#item_table');
                    $("#btn-print-payment").prop('disabled', false);
                    $("#item_table tr").each(function() {
                        $(this).find("th.col-actions").remove();
                        $(this).find("td.col-actions").remove();
                    });
                } else {
                    var alert_status = $('.alert-status').attr("hidden", false);
                    alert_status.find('.alert').removeClass('alert-success').addClass('alert-warning');
                    alert_status.find('.alert-text').text('Transaksi belum diproses, segera selesaikan transaksi !');
                }

            } catch (err) {}
        }
    });
}

getInvoicePurchaseItem();

$("#search-product").click(function(e) {
    getProductByBarcode();
    // drawPurchaseRow();
})

$('#barcode').on({
    keypress: function(e) {
        if (e.which == 13) {
            getProductByBarcode();
        }
    },
})



$('#add-item-cart').click(function(e) {
    drawPurchaseRow();
    $('#barcode').val(null);
    $('#qty-item-cart').val(1);
})

$('#qty-item-cart').on('keypress', function(e) {
    if (e.which == 13) {
        drawPurchaseRow();
        $('#barcode').val(null);
        $('#qty-item-cart').val(1);
    }
})

$('#process_payment').click(function(e) {
    var supplier = $('#supplier').val()
    $.ajax({
        type: "POST",
        url: "/v1/purchase_detail/process_payment",
        data: {
            "invoice_purchase": invoice_number,
            "total": grandTotal,
            "supplier": supplier
        },
        success: function(result) {
            window.location.href = '/dash/transaction/purchase';
        }
    });
})

$('#cash').on('keyup', function(e) {
    cash = e.currentTarget.value;
    change = cash - grandTotal;
    $('#change').val(change.toLocaleString('id-ID'));
    if (e.currentTarget.value == 0)
        $("#btn-print-payment").prop('disabled', true);
    else
        $("#btn-print-payment").prop('disabled', false);
});

$('#btn-print-payment').click(function() {
    printResult()
})

var deleteItem = function(e) {
    var row = $(e).closest('tr')
    var row_barcode = row.attr('id');

    $.ajax({
        type: "POST",
        url: "/v1/purchase_detail/delete_item",
        data: {
            "invoice_purchase": invoice_number,
            "barcode": row_barcode,
        },
        success: function(result) {
            grandTotal -= result.total;
            $('#grand_total').text(Number(grandTotal).toLocaleString('id-ID'));
            row.remove();
        }
    });
}

var updateItem = function(e) {
    row = $(e).closest('tr')
    var itemName = row.find(".product-name").html();
    var itemQty = row.find(".qty").html();
    var itemBarcode = row.find(".product-barcode").html();
    $('#modal-item-name').val(itemName);
    $('#modal-qty-item-cart').val(itemQty);
    $('#modal-barcode').val(itemBarcode);
}

$('#modal-btn-update').click(function(e) {
    var newQty = $('#modal-qty-item-cart').val();
    grandTotal -= Number(row.find(".purchase_total").attr('data-purchase-total'));
    var newTotal = Number(newQty) * Number(row.find(".price").html());
    $.ajax({
        type: "POST",
        url: "/v1/purchase_detail/update_item",
        data: {
            "invoice_purchase": invoice_number,
            "barcode": $('#modal-barcode').val(),
            "qty": newQty,
            'total': newTotal
        },
        success: function(result) {
            row.find(".qty").html(newQty);
            row.find(".price").html(result.price);
            row.find(".purchase_total").html(Number(result.total).toLocaleString('id-ID'));
            row.find(".purchase_total").attr('data-purchase-total', result.total);
            $('#modal-default').modal('toggle');

            grandTotal += result.total;
            $('#grand_total').text(Number(grandTotal).toLocaleString('id-ID'));
            emptyingCashChange();
        }
    });
});

var printResult = function() {
    var total = $('#grand_total').html()
    change = $('#change').val();
    cash = $('#cash').val();
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