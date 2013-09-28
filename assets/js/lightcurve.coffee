$ = jQuery
$ ->
    class LightCurve
        constructor: (@selector, @epoch, @period) ->
            @setGeometry()
            @svg = @getSvg(@selector)
            @isPeriodic = @epoch and @period

        setGeometry: ->
            @margin =
                top: 20
                right: 10
                bottom: 40
                left: 50
            @width = $(@selector).width()
            @height = 0.3 * @width
            @width = @width - @margin.left - @margin.right
            @height = @height - @margin.top - @margin.bottom
            @xScale = d3.scale.linear().range([0, @width]).nice()
            @yScale = d3.scale.linear().range([0, @height]).nice()
            @xAxis = d3.svg.axis().scale(@xScale).orient('bottom').ticks(10).tickSize(-@height, 0, 0)
            @yAxis = d3.svg.axis().scale(@yScale).orient('left').ticks(10).tickSize(-@width, 0, 0)

        getSvg: (selector) ->
            @svg = d3.select(selector).append('svg')
                .attr
                    width: @width + @margin.left + @margin.right
                    height: @height + @margin.top + @margin.bottom
                .append('g')
                .attr
                    transform: "translate(#{@margin.left},#{@margin.top})"
            @svg.append('g')
                .attr
                    class: 'x axis'
                    transform: "translate(0,#{@height})"
            @xTitle = @svg.append('text')
                .attr
                    class: 'axisTitle'
                    transform: "translate(#{@width / 2},#{@height + @margin.bottom})"
            @yTitle = @svg.append('text')
                .attr
                    class: 'axisTitle'
                    transform: "rotate(-90) translate(-#{@height / 2}, -#{@margin.left / 1.3})"
            @svg.append('g')
                .attr
                    class: 'y axis'
            @svg

        getPhase: (jd) =>
            if @isPeriodic
                periods = (jd - @epoch) / @period
                phase = periods % 1
            else
                0.0

        setData: (@data) ->

        drawChart: ->
            @xScale.domain d3.extent @data, (d) -> d.jd
            @yScale.domain d3.extent @data, (d) -> d.magnitude
            @svg.select('.x.axis')
                .call(@xAxis)
            @svg.select('.y.axis')
                .call(@yAxis)
            @svg.selectAll('circle')
                .data(@data)
                .enter()
                .append('circle')
                .attr
                    cx: (d) => @xScale d.jd
                    cy: (d) => @yScale d.magnitude
                    r: '2'
                .on('mouseover', ->
                    d3.select(@).transition().duration(150).attr('r', '10')
                )
                .on('mouseout', ->
                    d3.select(@).transition().duration(150).attr('r', '2')
                )
            @xTitle.text 'Julian Date'
            @yTitle.text 'Magnitude'

        updateChart: (isPhaseChart) ->
            xDomain = if isPhaseChart then [0, 1] else d3.extent @data, (d) -> d.jd
            @xScale.domain xDomain
            @svg.select('.x.axis')
                .call(@xAxis)
            @svg.selectAll('circle')
                .transition()
                .duration(1000)
                .attr
                    cx: (d) => @xScale if isPhaseChart then d.phase else d.jd
            @xTitle.text if isPhaseChart then 'Phase' else 'Julian Date'


    selector = '.lightcurve'
    epoch = +$('.catalog-data .epoch').text()
    period = +$('.catalog-data .period').text()
    lc = new LightCurve(selector, epoch, period)
    csvUrl = $(selector).data 'csvSource'
    if csvUrl
        isPhaseChart = false
        d3.csv(
            csvUrl,
            ((d) ->
                jd: +d.jd
                magnitude: +d.magnitude
                phase: lc.getPhase +d.jd
            ),
            ((error, data) ->
                lc.setData data
                lc.drawChart()
            )
        )
        d3.select('#toggle-chart')
            .on('click', =>
                if lc.isPeriodic
                    isPhaseChart = not isPhaseChart
                    lc.updateChart isPhaseChart
                d3.event.preventDefault()
            )
