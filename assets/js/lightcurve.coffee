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
                right: 20
                bottom: 20
                left: 40
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
                    fill: 'red'
                    r: '2'


    selector = '.lightcurve'
    epoch = +$('.catalog-data .epoch').text()
    period = +$('.catalog-data .period').text()
    lc = new LightCurve(selector, epoch, period)
    csvUrl = $(selector).data 'csvSource'
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
