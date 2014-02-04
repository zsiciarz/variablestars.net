$ = jQuery
$ ->
    current_jd = +$("#current-jd").text()
    $("#id_jd").val(current_jd)

    detail_fields = $("#div_id_comp1, #div_id_comp2, #div_id_comment_code, #div_id_chart, #div_id_notes")
    detail_fields.hide()
