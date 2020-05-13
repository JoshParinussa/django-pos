"use strict";

var HargaBertingkatTable = function() {

    var initTable = function() {

        var initInlineFormUpdate = function(prefix) {
            if (actions == "update") {
                $('.not_displayed').hide()
                var inlineFormRow = $('tbody').find('.current-form-row')
                inlineFormRow.each(function(index, value) {
                    var isLastElement = index == inlineFormRow.length - 1;
                    if (!isLastElement) {
                        $(this).find('.btn-add-row').removeClass('btn-add-row').addClass('btn-delete-row').prop('title', 'Hapus harga bertingkat')
                            .find('i').removeClass('flaticon2-plus-1').addClass('flaticon-delete');
                    }
                });
            }
        }

        function updateElementIndex(el, prefix, ndx) {
            var id_regex = new RegExp('(' + prefix + '-\\d+)');
            var replacement = prefix + '-' + ndx;
            if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
            if (el.id) el.id = el.id.replace(id_regex, replacement);
            if (el.name) el.name = el.name.replace(id_regex, replacement);
        }

        var addRow = function(selector, prefix) {
            var newElement = $(selector).clone(true)
            var total = $('#id_' + prefix + '-TOTAL_FORMS').val();
            console.log(total)
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
                var rowFormIndex = btn.closest('.current-form-row').find(':input[type=hidden]').attr('name').split('-')[1];
                var inlineFormDeleteId = 'id_' + prefix + '-' + rowFormIndex + '-DELETE';
                $(`#${inlineFormDeleteId}`).prop('checked', true);
                if (actions != "update") {
                    btn.closest('.current-form-row').remove();
                    var forms = $('.current-form-row');
                    $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
                    for (var i = 0, formCount = forms.length; i < formCount; i++) {
                        $(forms.get(i)).find(':input').each(function() {
                            updateElementIndex(this, prefix, i);
                        });
                    }
                }
                btn.closest('.current-form-row').hide();
            }
        }


        $(document).on('click', '.btn-delete-row', function(e) {
            e.preventDefault();
            deleteRow('hargabertingkat', $(this));
        });

        $(document).on('click', '.btn-add-row', function(e) {
            e.preventDefault();
            addRow('.current-form-row:last', 'hargabertingkat');
        });

        initInlineFormUpdate('hargabertingkat');
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