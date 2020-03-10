"use strict";
window.csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

var itemBarcode;
var itemName;
var itemPrice;
var purchaseItemQty;
var purchaseItemTotal;
let lineNo = 1;
var invoice_number = $('#invoice_number').text();

var date = moment().format("DD/MM/YYYY"); 
$('#sale-date').val(date);
$('#cashier').val(currentUser);

var getProductByBarcode = function (){
    var barcode = $('#barcode').val();
    if (barcode.length > 0){
        $.ajax({
            type: "POST",
            url: "/v1/products/get_by_barcode",
            data: {
                'barcode': barcode
            },
            success: function(result){
                if (result.length > 0){
                    var data = result[0]
                    itemBarcode = data.barcode;
                    itemName = data.name;
                    itemPrice = data.selling_price;
                    $('#item-name').val(itemName);
                }else{
                    $('#item-name').val("");
                    alert("Product not found");
                }
            }
        });
    }
}

var drawPurchaseRow = function (){
    purchaseItemQty = $('#qty-item-cart').val();
    purchaseItemTotal = itemPrice * purchaseItemQty;

    $.ajax({
        type: "POST",
        url: "/v1/sales/add_item",
        data:{
            "invoice_number": invoice_number,
            "barcode": itemBarcode,
            "qty": purchaseItemQty,
            "total": purchaseItemTotal
        },
        success: function(result){

        }
    });

    var row = "<tr>"+
            "<td>"+lineNo+"</td>"+
            "<td>"+itemBarcode+"</td>"+
            "<td>"+itemName+"</td>"+
            "<td>"+itemPrice+"</td>"+
            "<td>"+purchaseItemQty+"</td>"+
            "<td>"+purchaseItemTotal+"</td>"+
            "<td>"+
                "<button type='button' class='btn btn-info'>Update</button>&nbsp;"+
                "<button type='button' class='btn btn-danger'>Delete</button>&nbsp;"+
            "</td>"+
          "</tr>";
    var tableBody = $("table tbody"); 
    tableBody.append(row); 
    lineNo++; 
}

var getInvoiceSaleItem = function (){
    
}


$("#search-product").click(function (e){
    getProductByBarcode(); 
})

$('#barcode').on({
    keypress: function(e) {
        if(e.which == 13) {
            getProductByBarcode();
        }
    },
})



$('#add-item-cart').click(function (e){
    drawPurchaseRow();
})

$('#qty-item-cart').on('keypress', function(e){
    if(e.which == 13) {
        drawPurchaseRow();
    }
})