import $ from 'jquery'
import bootstrap from 'bootstrap'
import ElmJdClock from './JdClock.elm'
import ElmJdConverter from './JdConverter.elm'

ElmJdClock.JdClock.embed(document.getElementById('jd-clock'))
ElmJdConverter.JdConverter.embed(document.getElementById('elm-jd-converter'))

$(() => {
    $('.julian-day').tooltip({
        container: 'body',
        placement: 'left',
        title: () => {
            jd = Number(this.textContent)
            date = new Date((jd  - 2440587.5) * 86400000)
            date.toString()
        }
    })
})
