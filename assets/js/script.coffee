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
