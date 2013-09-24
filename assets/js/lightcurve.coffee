$ = jQuery
$ ->
    class LightCurve
        constructor: (@selector) ->
            @margin =
                top: 20
                right: 20
                bottom: 20
                left: 40
            @width = $(@selector).width()
            @height = 0.3 * @width
            @width = @width - @margin.left - @margin.right
            @height = @height - @margin.top - @margin.bottom

        getSvg: ->
            d3.select(@selector).append('svg')
                .attr
                    width: @width + @margin.left + @margin.right
                    height: @height + @margin.top + @margin.bottom
                .append('g')
                .attr
                    transform: "translate(#{@margin.left},#{@margin.top})"

        getScales: ->
            [
                d3.scale.linear().range([0, @width]).nice()
                d3.scale.linear().range([0, @height]).nice()
            ]

        drawData: (svg, data) ->
            [xScale, yScale] = @getScales()
            xScale.domain d3.extent data, (d) -> d.jd
            yScale.domain d3.extent data, (d) -> d.magnitude
            xAxis = d3.svg.axis().scale(xScale).orient('bottom').ticks(10)
            yAxis = d3.svg.axis().scale(yScale).orient('left').ticks(10)
            svg.append('g')
                .attr
                    class: 'x axis'
                    transform: "translate(0,#{@height})"
                .call(xAxis.tickSize(-@height, 0, 0))
            svg.append('g')
                .attr
                    class: 'y axis'
                .call(yAxis.tickSize(-@width, 0, 0))
            svg.selectAll('circle')
                .data(data)
                .enter()
                .append('circle')
                .attr
                    cx: (d) -> xScale d.jd
                    cy: (d) -> yScale d.magnitude
                    fill: 'red'
                    r: '2'


    selector = '.lightcurve'
    lc = new LightCurve(selector)
    svg = lc.getSvg()
    csvUrl = $(selector).data 'csvSource'
    d3.csv(
        csvUrl,
        ((d) ->
            jd: +d.jd
            magnitude: +d.magnitude
        ),
        ((error, data) ->
            lc.drawData svg, data
        )
    )
