$ = require('jquery')
bootstrap = require('bootstrap')
datetimepicker = require('eonasdan-bootstrap-datetimepicker')
Elm = require('./Main.elm')

Elm.embed(Elm.JdClock, document.getElementById('jd-clock'))
Elm.embed(Elm.JdConverter, document.getElementById('elm-jd-converter'))

$ ->
    $('.julian-day').tooltip
        container: 'body'
        placement: 'left'
        title: ->
            jd = Number(this.textContent)
            date = new Date((jd  - 2440587.5) * 86400000)
            date.toString()
    setConvertedJD = ->
        dt = new Date(
            +$("#jd-converter .date-year").val(),
            +$("#jd-converter .date-month").val() - 1,
            +$("#jd-converter .date-day").val(),
            +$("#jd-converter .date-hour").val(),
            +$("#jd-converter .date-minute").val(),
            +$("#jd-converter .date-second").val()
        )
        jd = dt.getTime() / 86400000 + 2440587.5
        $("#jd-converter .jd").val(jd.toFixed(4))
        false
    setConvertedDate = (dt, updateJD = true) ->
        dt ?= new Date()
        $("#jd-converter .date-year").val(dt.getFullYear())
        $("#jd-converter .date-month").val(dt.getMonth() + 1)
        $("#jd-converter .date-day").val(dt.getDate())
        $("#jd-converter .date-hour").val(dt.getHours())
        $("#jd-converter .date-minute").val(dt.getMinutes())
        $("#jd-converter .date-second").val(dt.getSeconds())
        setConvertedJD() if updateJD
        false
    setConvertedDate()
    $("#jd-converter .now").on('click', () => setConvertedDate())
    $("#jd-converter input[class^='date-']").on('change', () => setConvertedJD())
    $("#jd-converter input.jd").on('keyup', (e) =>
        jd = +e.target.value
        if not isNaN(jd)
            dt = new Date((jd  - 2440587.5) * 86400000)
            setConvertedDate(dt, false)
        false
    )
