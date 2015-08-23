bootstrap = require('bootstrap')

$ = jQuery
$ ->
    updateJulianDate = ->
        jd = new Date().getTime() / 86400000 + 2440587.5
        $("#current-jd").text(jd.toFixed(4))
        setTimeout updateJulianDate, 1000
    updateJulianDate()
    $('.julian-day').tooltip
        container: 'body'
        placement: 'left'
        title: ->
            jd = Number(this.textContent)
            date = new Date((jd  - 2440587.5) * 86400000)
            date.toString()
