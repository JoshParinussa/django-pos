"use strict";

var HargaBertingkatTable = function() {

    var initTable = function() {

        function updateElementIndex(el, prefix, ndx) {
            var id_regex = new RegExp('(' + prefix + '-\\d+)');
            var replacement = prefix + '-' + ndx;
            console.log(replacement);
            if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
            if (el.id) el.id = el.id.replace(id_regex, replacement);
            if (el.name) el.name = el.name.replace(id_regex, replacement);
        }

        var addRow = function(selector, prefix) {
            var newElement = $(selector).clone(true)
            var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
            newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
                var name = $(this).attr('name')
                if (name) {
                    name = name.replace('-' + (total - 1) + '-', '-' + total + '-');
                    var id = 'id_' + name;
                    $(this).attr({ 'name': name, 'id': id }).val('').removeAttr('checked');
                }
            });
            total++;
            $('#id_' + prefix + '-TOTAL_FORMS').val(total);
            $(selector).after(newElement);
            var conditionRow = $('.current-form-row:not(:last)');
            conditionRow.find('.btn-add-row')
                .removeClass('btn-add-row').addClass('btn-delete-row').prop('title', 'Hapus harga bertingkat')
                .find('i').removeClass('flaticon2-plus-1').addClass('flaticon-delete')
            return false;
        }

        var deleteRow = function(prefix, btn) {
            var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
            if (total > 1) {
                btn.closest('.current-form-row').remove();
                var forms = $('.current-form-row');
                $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
                for (var i = 0, formCount = forms.length; i < formCount; i++) {
                    $(forms.get(i)).find(':input').each(function() {
                        updateElementIndex(this, prefix, i);
                    });
                }
            }

        }


        $(document).on('click', '.btn-delete-row', function(e) {
            e.preventDefault();
            deleteRow('form', $(this));
        });

        $(document).on('click', '.btn-add-row', function(e) {
            e.preventDefault();
            addRow('.current-form-row:last', 'form');
        });


    };
    return {

        //main function to initiate the module
        init: function() {
            initTable();
        },

    };


}();


jQuery(document).ready(function() {
    HargaBertingkatTable.init();
});