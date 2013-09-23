$ = jQuery
$ ->
    csvUrl = $('.lightcurve').data 'csvSource'
    console.log csvUrl
    d3.csv csvUrl, (data) ->
        for row in data
            console.log row
