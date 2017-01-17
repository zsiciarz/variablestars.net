import d3 from 'd3'

class LightCurve {
    constructor(selector, epoch, period) {
        this.selector = selector
        this.epoch = epoch
        this.period = period
        this.setGeometry()
        this.svg = this.getSvg(this.selector)
        this.isPeriodic = this.epoch && this.period
    }

    setGeometry() {
        this.margin = {
            top: 20,
            right: 10,
            bottom: 40,
            left: 50
        }
        this.width = d3.select(this.selector).node().offsetWidth - 40
        this.height = 0.3 * this.width
        this.width = this.width - this.margin.left - this.margin.right
        this.height = this.height - this.margin.top - this.margin.bottom
        this.xScale = d3.scale.linear().range([0, this.width]).nice()
        this.yScale = d3.scale.linear().range([0, this.height]).nice()
        this.xAxis = d3.svg.axis().scale(this.xScale).orient('bottom').ticks(10).tickSize(-this.height, 0, 0)
        this.yAxis = d3.svg.axis().scale(this.yScale).orient('left').ticks(10).tickSize(-this.width, 0, 0)
    }

    getSvg(selector) {
        this.svg = d3.select(selector).append('svg')
            .attr({
                width: this.width + this.margin.left + this.margin.right,
                height: this.height + this.margin.top + this.margin.bottom
            })
            .append('g')
            .attr({
                transform: `translate(${this.margin.left},${this.margin.top})`
            })
        this.svg.append('g')
            .attr({
                class: 'x axis',
                transform: `translate(0,${this.height})`
            })
        this.xTitle = this.svg.append('text')
            .attr({
                class: 'axisTitle',
                transform: `translate(${this.width / 2},${this.height + this.margin.bottom})`
            })
        this.yTitle = this.svg.append('text')
            .attr({
                class: 'axisTitle',
                transform: `rotate(-90) translate(-${this.height / 2}, -${this.margin.left / 1.3})`
            })
        this.svg.append('g').attr({class: 'y axis'})
        return this.svg
    }

    getPhase(jd) {
        if (this.isPeriodic) {
            const periods = (jd - this.epoch) / this.period
            return periods % 1
        }
        else {
            return 0.0
        }
    }

    setData(data) {
        this.data = data
    }

    drawChart() {
        this.xScale.domain(d3.extent(this.data, d => d.jd))
        this.yScale.domain(d3.extent(this.data, d => d.magnitude))
        this.svg.select('.x.axis').call(this.xAxis)
        this.svg.select('.y.axis').call(this.yAxis)
        this.svg.selectAll('circle')
            .data(this.data)
            .enter()
            .append('circle')
            .attr({
                cx: d => this.xScale(d.jd),
                cy: d => this.yScale(d.magnitude),
                r: '2'
            })
            .on('mouseover', function () {
                d3.select(this).transition().duration(150).attr('r', '10')
            })
            .on('mouseout', function () {
                d3.select(this).transition().duration(150).attr('r', '2')
            })
            .append('title')
            .text(d => `JD ${d.jd}:  ${d.magnitude} mag.`)
        this.xTitle.text('Julian Date')
        this.yTitle.text('Magnitude')
    }

    updateChart(isPhaseChart) {
        let xDomain = d3.extent(this.data, d => d.jd)
        if (isPhaseChart) {
            xDomain = [0, 1]
        }
        this.xScale.domain(xDomain)
        this.svg.select('.x.axis').call(this.xAxis)
        this.svg.selectAll('circle')
            .transition()
            .duration(1000)
            .attr({
                cx: d => this.xScale(isPhaseChart ? d.phase : d.jd)
            })
        this.xTitle.text(isPhaseChart ? 'Phase' : 'Julian Date')
    }
}

const selector = '.lightcurve'
const epoch = +d3.select('.catalog-data .epoch').text()
const period = +d3.select('.catalog-data .period').text()
const lc = new LightCurve(selector, epoch, period)
const csvUrl = d3.select(selector).node().dataset.csvSource
if (csvUrl) {
    let isPhaseChart = false
    d3.csv(
        csvUrl,
        d => ({
            jd: +d.jd,
            magnitude: +d.magnitude,
            phase: lc.getPhase(+d.jd)
        }),
        (error, data) => {
            lc.setData(data)
            lc.drawChart()
        }
    )
    d3.select('#toggle-chart').on('click', () => {
        if (lc.isPeriodic) {
            isPhaseChart = !isPhaseChart
            lc.updateChart(isPhaseChart)
        }
        d3.event.preventDefault()
    })
}
