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

var emptyingCashChange = function() {
    $('#change').val('');
    $('#cash').val('');
}

var getProductByNameAPI = function(id) {
    $.ajax({
        type: "POST",
        url: "/v1/products/get_by_name",
        data: {
            'id': id
        },
        success: function(result) {
            if (result.length > 0) {
                var data = result[0]
                itemBarcode = data.barcode;
                itemName = data.name;
                itemPrice = data.selling_price;
                drawPurchaseRow();
                // $("#product_name").val(null).trigger('change');
                $('#barcode').val(null);
            } else {
                alert("Product not found");
            }
        }
    });
}

var getProductByName = function() {
    var product_arr = [];
    var res;
    // $.ajax({
    //     type: "GET",
    //     url: "/v1/products?query={id, text}",
    //     success: function(data) {
    //         product_arr = data.results,
    //             res = data.results.map(function(item) {
    //                 return { id: item.id, text: item.text };
    //             });
    //         $('#product_name').select2({
    //             theme: "bootstrap",
    //             data: res,
    //             multiple: true,
    //             maximumSelectionLength: 1,
    //             placeholder: "Cari berdasarkan nama produk",

    //         });
    //     }
    // });

    // SELECT2 from AJAX
    // $('.barcode').select2({
    //     ajax: {
    //         type: "GET",
    //         url: "/v1/products?query={id, text}",
    //         dataType: 'json',
    //         data: function(params) {
    //             var query = {
    //                 barcode: params.term,
    //                 type: 'public'
    //             }

    //             // Query parameters will be ?search=[term]&type=public
    //             return query;
    //         }

    //     },
    //     theme: "bootstrap",
    //     // selectOnClose: true,
    //     placeholder: "Cari berdasarkan barcode produk",
    // });

    $('.product_name').select2({
        ajax: {
            type: "GET",
            url: "/v1/products?query={id, text}",
            dataType: 'json',

        },
        theme: "bootstrap",
        // selectOnClose: true,
        placeholder: "Cari berdasarkan nama produk",
    });

    $('.product_name').on("select2:select", function(evt) {
        var id = $(this).val();
        $('#product_name').val('').trigger("change");
        getProductByNameAPI(id);
        $('#barcode').focus();
    });

    // $('.barcode').on("select2:select", function(evt) {
    //     var id = $(this).val();
    //     $('#barcode').val('').trigger("change");
    //     getProductByNameAPI(id);
    //     $('#barcode').focus();
    // });
    // $(document).on('keyup keydown', 'input.select2-search__field', function(e) {
    //     if (e.keyCode == 13) {
    //         var id = $('#product_name').select2('data')[0].id;
    //         $('#product_name').val('').trigger("change");
    //         getProductByNameAPI(id);
    //         $('#barcode').focus();
    //     }
    // });

    $(document).on('focus', '.select2-selection.select2-selection--single', function(e) {
        $(this).closest(".select2-container").siblings('select:enabled').select2('open');
    });
}

getProductByName();

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

var drawPurchaseRow = function() {
    purchaseItemQty = 1
    var member = $('#member').val()
    var idRow = itemBarcode;
    // purchaseItemTotal = itemPrice * purchaseItemQty;

    $.ajax({
        type: "POST",
        url: "/v1/sales/add_item",
        data: {
            "invoice_number": invoice_number,
            "barcode": itemBarcode,
            "qty": purchaseItemQty,
            "member": member,
        },
        success: function(result) {
            if (result.is_out_of_stock) {
                toastr.error('Stok ' + result.product.name + ' KOSONG atau HABIS.');
            } else {
                var purchaseItemTotal = Number(result.sale.total);
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
                        "<i class='la la-edit icon-10x'></i>" +
                        "</span>" +
                        "<span onclick='deleteItem(this)' class='btn btn-sm btn-clean btn-icon btn-icon-md' title='Hapus item'>" +
                        "<i class='la la-trash icon-10x'></i>" +
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
            try {
                var invoice_data = result.data['invoice'][0];
                $('#member').val(invoice_data['member'])
                date = moment.utc(invoice_data['date']).local().format('LLL');
                $('#sale-date').val(date);
                var sale_items = result.data['sale_items'];

                $('#change').val(Number(invoice_data['change']).toLocaleString('id-ID'));
                $('#cash').val(Number(invoice_data['cash']));

                sale_items.forEach(function(item) {
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
                            "<span onclick='updateItem(this)' class='btn btn-xl btn-clean btn-icon btn-icon-xl' data-toggle='modal' data-target='#modal-default' title='Edit item'>" +
                            "<i class='la la-edit icon-10x'></i>" +
                            "</span>" +
                            "<span onclick='deleteItem(this)' class='btn btn-xl btn-clean btn-icon btn-icon-xl btn-delete' title='Hapus item'>" +
                            "<i class='la la-trash icon-10x'></i>" +
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
                    $('#product_name').attr("disabled", true);
                    $('#barcode').attr("disabled", true);
                    $('#member').attr("disabled", true);
                    $('#cash').attr("disabled", true);
                    var item_table = $('#item_table');
                    $("#btn-print-payment").prop('disabled', false);
                    $("#item_table tr").each(function() {
                        $(this).find("th.col-actions").remove();
                        $(this).find("td.col-actions").remove();
                    });
                } else if (invoice_data['status'] == 2) {
                    var alert_status = $('.alert-status').attr("hidden", false);
                    alert_status.find('.alert').removeClass('alert-success').addClass('alert-danger');
                    alert_status.find('.alert-text').text('Transaksi telah dibatalkan !');
                    if ($('#cash').val() > 0) {
                        $("#btn-print-process-payment").prop('disabled', false);
                    }
                } else {
                    var alert_status = $('.alert-status').attr("hidden", false);
                    alert_status.find('.alert').removeClass('alert-success').addClass('alert-warning');
                    alert_status.find('.alert-text').text('Transaksi belum diproses, segera selesaikan transaksi !');
                    if ($('#cash').val() > 0) {
                        $("#btn-print-process-payment").prop('disabled', false);
                    }

                }

            } catch (err) {}
        }
    });
}

getInvoiceSaleItem();

$("#search-product").click(function(e) {
    getProductByBarcode();

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

var processPayment = function() {
    var member = $('#member').val()
    $.ajax({
        type: "POST",
        url: "/v1/sales/process_payment",
        data: {
            "invoice_number": invoice_number,
            "cash": cash,
            "change": change,
            "total": grandTotal,
            "member": member
        },
        success: function(result) {
            // window.location.href = '/dash/transaction/sale';
            window.location.href = '/dash/transaction/sale/new';
        }
    });
}

$('#process_payment').click(function(e) {
    processPayment();
})

$('input.number').keyup(function(event) {

    // skip for arrow keys
    if (event.which >= 37 && event.which <= 40) return;

    // format number
    $(this).val(function(index, value) {
        return value
            .replace(/\D/g, "")
            .replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    });
});

$('#cash').on('keyup', function(e) {
    // skip for arrow keys
    if (event.which >= 37 && event.which <= 40) return;
    cash = e.currentTarget.value;
    cash = cash.replace(/,/g, '');

    change = cash - grandTotal;

    $('#change').val(change.toLocaleString('id-ID'));
    if (e.currentTarget.value == 0) {
        $("#btn-print-payment").prop('disabled', true);
        $("#btn-print-process-payment").prop('disabled', true);
    } else {
        $("#btn-print-payment").prop('disabled', false);
        $("#btn-print-process-payment").prop('disabled', false);
    }
});

$('#btn-print-payment').click(function() {
    printResult();
})

$('#btn-print-process-payment').click(function() {
    processPayment();
    printResult();
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
            $('#grand_total').text(Number(grandTotal).toLocaleString('id-ID'));
            row.remove();
        }
    });
}

var curItemQty;
var updateItem = function(e) {
    row = $(e).closest('tr')
    var itemName = row.find(".product-name").html();
    var itemQty = row.find(".qty").html();
    curItemQty = itemQty;
    var itemBarcode = row.find(".product-barcode").html();
    $('#modal-item-name').val(itemName);
    $('#modal-qty-item-cart').val(itemQty);
    $('#modal-barcode').val(itemBarcode);
}

$('#modal-btn-update').click(function(e) {
    var newQty = $('#modal-qty-item-cart').val();
    // grandTotal -= Number(row.find(".purchase_total").attr('data-purchase-total'));
    // var newTotal = Number(newQty) * Number(row.find(".price").html());
    if (curItemQty != newQty) {
        $.ajax({
            type: "POST",
            url: "/v1/sales/update_item",
            data: {
                "invoice_number": invoice_number,
                "barcode": $('#modal-barcode').val(),
                "qty": newQty,
                // 'total': newTotal
            },
            success: function(result) {
                if (result.is_out_of_stock) {
                    toastr.error('Stok ' + result.product.name + ' KOSONG atau HABIS.');
                } else {
                    // var newQty = $('#modal-qty-item-cart').val();
                    grandTotal -= Number(row.find(".purchase_total").attr('data-purchase-total'));
                    // var newTotal = Number(newQty) * Number(row.find(".price").html());

                    row.find(".qty").html(newQty);
                    row.find(".price").html(result.sale.price);
                    row.find(".purchase_total").html(Number(result.sale.total).toLocaleString('id-ID'));
                    row.find(".purchase_total").attr('data-purchase-total', result.sale.total);
                    $('#modal-default').modal('toggle');

                    grandTotal += result.sale.total;
                    $('#grand_total').text(Number(grandTotal).toLocaleString('id-ID'));
                    emptyingCashChange();
                }
            }
        });
    } else {
        $('.modal').modal('toggle');
    }
});

$('#cancel-transaction').click(function(e) {
    $.ajax({
        type: "POST",
        url: "/v1/sales/update_cancel_transaction",
        data: {
            "invoice_number": invoice_number,
        },
        success: function(result) {
            // location.reload()
            window.location.href = '/dash/transaction/sale';
        }
    });
});

var printResult = function() {
    var total = $('#grand_total').html()
    change = $('#change').val();
    cash = $('#cash').val();
    cash = cash.replace(/,/g, '');
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
                    <h3>Assalam Paiton</h3>
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
                    <p>Barang yang sudah dibeli tidak dapat dikembalikan</p>
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