$ = jQuery
$ ->
    updateJulianDate = ->
        jd = new Date().getTime() / 86400000 + 2440587.5
        $("#current-jd").text(jd.toFixed(4))
        setTimeout updateJulianDate, 1000
    updateJulianDate()
