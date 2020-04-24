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
$('#sale-date').val(date);
$('#cashier').val(currentUser);

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
                    itemPrice = data.selling_price;
                    drawPurchaseRow();
                    $('#barcode').val(null);
                } else {
                    alert("Product not found");
                }
            }
        });
    }
}

var drawDetailTransactionRow = function() {
    $.ajax({

    });
}

var drawPurchaseRow = function() {
    purchaseItemQty = 1
    purchaseItemTotal = itemPrice * purchaseItemQty;

    $.ajax({
        type: "POST",
        url: "/v1/sales/add_item",
        data: {
            "invoice_number": invoice_number,
            "barcode": itemBarcode,
            "qty": purchaseItemQty,
            "total": purchaseItemTotal
        },
        success: function(result) {
            grandTotal += Number(purchaseItemTotal);
            var idRow = itemBarcode;
            if ($('#item_table').find("#" + idRow).length > 0) {
                var currentQty = $('#item_table').find("#" + idRow + " .qty").html();
                var currentPurchaseTotal = $('#item_table').find("#" + idRow + " .purchase_total").html();

                var newQty = Number(currentQty) + Number(purchaseItemQty);
                var newPurchaseTotal = Number(currentPurchaseTotal) + Number(purchaseItemTotal);

                $('#item_table').find("#" + idRow + " .qty").text(newQty);
                $('#item_table').find("#" + idRow + " .purchase_total").text(newPurchaseTotal);



            } else {
                var row = "<tr id='" + idRow + "'" + itemBarcode + "'>" +
                    // "<td>" + lineNo + "</td>" +
                    "<td class='product-barcode' style='display:none;'>" + itemBarcode + "</td>" +
                    "<td class='product-name'>" + itemName + "</td>" +
                    "<td class='price'>" + itemPrice + "</td>" +
                    "<td class='qty'>" + purchaseItemQty + "</td>" +
                    "<td class='purchase_total'>" + purchaseItemTotal + "</td>" +
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
                lineNo++;
            }
            $('#grand_total').text(grandTotal);
            $('#sub-total').text(grandTotal);
        }
    });
}

var getInvoiceSaleItem = function() {
    $.ajax({
        type: "POST",
        url: "/v1/sales/get_by_invoice?format=datatables",
        data: {
            "invoice_number": invoice_number,
        },
        success: function(result) {
            result.data.forEach(function(item) {
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
                    $('#item_table').find("#" + idRow + " .purchase_total").text(newPurchaseTotal);
                } else {
                    var row = "<tr id='" + item.barcode + "'>" +
                        // "<td>" + lineNo + "</td>" +
                        "<td class='product-barcode' style='display:none;'>" + item.barcode + "</td>" +
                        "<td class='product-name'>" + item.product + "</td>" +
                        "<td class='price' data-price='" + item.price + "'>" + item.price + "</td>" +
                        "<td class='qty'>" + item.qty + "</td>" +
                        "<td class='purchase_total'>" + item.total + "</td>" +
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
                    tableBody.append(row)
                    lineNo++;
                }
            })
            $('#grand_total').text("Rp. " + grandTotal);
            $('#sub-total').text("Rp. " + grandTotal);
        }
    });
}

getInvoiceSaleItem();

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
    console.log("HE")
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
    $.ajax({
        type: "POST",
        url: "/v1/sales/process_payment",
        data: {
            "invoice_number": invoice_number,
            "cash": cash,
            "change": change,
            "total": grandTotal,
        }
    });
})

$('#cash').keyup((e) => {
    cash = e.currentTarget.value;
    change = cash - grandTotal;
    $('#change').val(change);
});

$('#btn-cancel-payment').click(function() {
    $('#btn-delete').text();
    console.log($('#btn-delete').text())
})

var deleteItem = function(e) {
    var row = $(e).closest('tr')
    var row_barcode = row.attr('id');

    $.ajax({
        type: "POST",
        url: "/v1/sales/delete_item",
        data: {
            "invoice_number": invoice_number,
            "barcode": row_barcode,
        },
        success: function(result) {
            grandTotal -= result.total;
            $('#grand_total').text(grandTotal);
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
    grandTotal -= Number(row.find(".purchase_total").html());
    var newTotal = Number(newQty) * Number(row.find(".price").html());
    grandTotal += newTotal;
    $.ajax({
        type: "POST",
        url: "/v1/sales/update_item",
        data: {
            "invoice_number": invoice_number,
            "barcode": $('#modal-barcode').val(),
            "qty": newQty,
            'total': newTotal
        },
        success: function(result) {
            row.find(".qty").html(newQty);
            row.find(".purchase_total").html(newTotal)
            $('#modal-default').modal('toggle');
            $('#grand_total').text(grandTotal);
        }
    });
});

var printResult = function() {

    var htmlReceiptHead =

        $("#item_table tbody").find("tr").each(function() {
            console.log($(this).find('.product-name').html());
        });
    var html =
        '<div id="print-receipt">' +
        '<div class="receipt" id="receipt">' +
        '<p class="centered" id="ticket-title">Django Cashier Receipt' +
        '<br>Address line 1' +
        '<br>Address line 2</p>' +
        '<table>' +
        '<thead>' +
        '<tr>' +
        '<th class="quantity">Qty.</th>' +
        '<th class="description">Item</th>' +
        '<th class="price">Total</th>' +
        '</tr>' +
        '</thead>' +
        '<tbody>' +
        '<tr>' +
        '<td class="quantity">1.00</td>' +
        '<td class="description">ARDUINO UNO R3</td>' +
        '<td class="price">$25.00</td>' +
        '</tr>' +
        '<tr>' +
        '<td class="quantity">2.00</td>' +
        '<td class="description">JAVASCRIPT BOOK</td>' +
        '<td class="price">$10.00</td>' +
        '</tr>' +
        '<tr>' +
        '<td class="quantity">1.00</td>' +
        '<td class="description">STICKER PACK</td>' +
        '<td class="price">$10.00</td>' +
        '</tr>' +
        '<tr>' +
        '<td class="quantity"></td>' +
        '<td class="description">TOTAL</td>' +
        '<td class="price">$55.00</td>' +
        '</tr>' +
        '</tbody>' +
        '</table>' +
        '<p class="centered">Thanks for your purchase!' +
        '<br>parzibyte.me/blog</p>' +
        '</div>' +
        '</div>';
    // var myPrintContent = document.getElementById('print-receipt');
    var myPrintWindow = window.open('', 'Print', '');
    myPrintWindow.document.write(html);
    // myPrintWindow.document.getElementById('receipt').style.display='block'
    myPrintWindow.document.close();
    myPrintWindow.focus();
    myPrintWindow.print();
    myPrintWindow.close();
    return false;
}

$('#btn-check').click(function() {
    $("#item_table tbody").find("tr").each(function() {
        console.log($(this).find('.product-name').html());
    });
})