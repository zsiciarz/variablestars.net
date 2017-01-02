$ = require('jquery')
bootstrap = require('bootstrap')
ElmJdClock = require('./JdClock.elm')
ElmJdConverter = require('./JdConverter.elm')

ElmJdClock.JdClock.embed(document.getElementById('jd-clock'))
ElmJdConverter.JdConverter.embed(document.getElementById('elm-jd-converter'))

$ ->
    $('.julian-day').tooltip
        container: 'body'
        placement: 'left'
        title: ->
            jd = Number(this.textContent)
            date = new Date((jd  - 2440587.5) * 86400000)
            date.toString()
