var d3TimeSlider = {
   brushstart: function () {
      svg.classed("selecting", true);
    },
    brushmove:  function () {
    },
    brushend: function () {
        svg.classed("selecting", !d3.event.target.empty());
        newInterval={its:brush.extent()[0].getTime()/1000,ets:brush.extent()[1].getTime()/1000}
        notifyNewInterval(newInterval);
        intervalInit=brush.extent()[0]
        intervalEnd=brush.extent()[1]
        interval_ms_duration=Math.abs(new Date(intervalEnd).getTime() - new Date(intervalInit).getTime())
        axis_init=new Date().setTime(new Date(intervalInit).getTime()-3*interval_ms_duration);
        axis_end=new Date().setTime(new Date(intervalEnd).getTime()+3*interval_ms_duration);
        x.domain([axis_init,axis_end]);
        svg.transition().duration(500)
        .select(".x.axis")
        .call(xAxis);
        brush.extent([intervalInit,intervalEnd]);
        svg.transition().duration(500)
        .select(".brush")
        .call(brush);
    },
    update: function (el, interval, notifyNewInterval) {
        var margin = {top: 15, right: 0, bottom: 25, left: 0}
        width=d3.select(el).node().getBoundingClientRect().width
        height=10
        var customTimeFormat = d3.time.format.multi([
          [".%L", function(d) { return d.getMilliseconds(); }],
          [":%S", function(d) { return d.getSeconds(); }],
          ["%I:%M", function(d) { return d.getMinutes(); }],
          ["%I %p", function(d) { return d.getHours(); }],
          ["%a %d", function(d) { return d.getDay() && d.getDate() != 1; }],
          ["%b %d", function(d) { return d.getDate() != 1; }],
          ["%B", function(d) { return d.getMonth(); }],
          ["%Y", function() { return true; }]
          ]);
        var brushstart = function () {
          svg.classed("selecting", true);
        }
        var brushmove = function () {
        }
        var brushend = function () {
            svg.classed("selecting", !d3.event.target.empty());
            newInterval={its:brush.extent()[0].getTime()/1000,ets:brush.extent()[1].getTime()/1000}
            notifyNewInterval(newInterval);
        }
        var intervalInit=new Date().setTime(interval.its*1000);
        var intervalEnd=new Date().setTime(interval.ets*1000);
        var intervalMsDuration=Math.abs(interval.ets*1000-interval.its*1000);
        var axisInit=new Date().setTime(new Date(intervalInit).getTime()-3*intervalMsDuration);
        var axisEnd=new Date().setTime(new Date(intervalEnd).getTime()+3*intervalMsDuration);
        var x = d3.time.scale()
            .range([0, width])
            .domain([axisInit,axisEnd])
        var xAxis = d3.svg.axis()
                    .scale(x)
                    .orient("bottom")
                    .tickFormat(customTimeFormat)
                    .ticks(4);
        var y = d3.random.normal(height / 2, height / 8);
        var brush = d3.svg.brush()
            .x(x)
            .extent([intervalInit,intervalEnd])
            .on("brushstart", brushstart)
            .on("brush", brushmove)
            .on("brushend", brushend);
        svg = d3.select(el).select("svg")
        svg.transition().duration(500)
        .select(".x.axis")
        .call(xAxis);
        svg.transition().duration(500)
        .select(".brush")
        .call(brush);
    },
    create: function (el, interval, notifyNewInterval) {
        var margin = {top: 15, right: 0, bottom: 25, left: 0}
        width=d3.select(el).node().getBoundingClientRect().width
        height=10
        var customTimeFormat = d3.time.format.multi([
          [".%L", function(d) { return d.getMilliseconds(); }],
          [":%S", function(d) { return d.getSeconds(); }],
          ["%I:%M", function(d) { return d.getMinutes(); }],
          ["%I %p", function(d) { return d.getHours(); }],
          ["%a %d", function(d) { return d.getDay() && d.getDate() != 1; }],
          ["%b %d", function(d) { return d.getDate() != 1; }],
          ["%B", function(d) { return d.getMonth(); }],
          ["%Y", function() { return true; }]
          ]);
        var brushstart = function () {
          svg.classed("selecting", true);
        }
        var brushmove = function () {
        }
        var brushend = function () {
            svg.classed("selecting", !d3.event.target.empty());
            newInterval={its:brush.extent()[0].getTime()/1000,ets:brush.extent()[1].getTime()/1000}
            notifyNewInterval(newInterval);
        }
        var intervalInit=new Date().setTime(interval.its*1000);
        var intervalEnd=new Date().setTime(interval.ets*1000);
        var intervalMsDuration=Math.abs(interval.ets*1000-interval.its*1000);
        var axisInit=new Date().setTime(new Date(intervalInit).getTime()-3*intervalMsDuration);
        var axisEnd=new Date().setTime(new Date(intervalEnd).getTime()+3*intervalMsDuration);
        var x = d3.time.scale()
            .range([0, width])
            .domain([axisInit,axisEnd])
        var xAxis = d3.svg.axis()
                    .scale(x)
                    .orient("bottom")
                    .tickFormat(customTimeFormat)
                    .ticks(4);
        var y = d3.random.normal(height / 2, height / 8);
        var brush = d3.svg.brush()
            .x(x)
            .extent([intervalInit,intervalEnd])
            .on("brushstart", brushstart)
            .on("brush", brushmove)
            .on("brushend", brushend);
        var arc = d3.svg.arc()
            .outerRadius(height / 2)
            .startAngle(0)
            .endAngle(function(d, i) { return i ? -Math.PI : Math.PI; });
        var svg = d3.select(el).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .style('shape-rendering','crispEdges')
            .call(xAxis);
        var brushg = svg.append("g")
            .attr("class", "brush")
            .style('fill','#d0d0d0')
            .style('shape-rendering','crispEdges')
            .call(brush);
        brushg.selectAll(".resize").append("path")
            .attr("transform", "translate(0," +  height / 2 + ")")
            .attr("d", arc);
        brushg.selectAll("rect")
            .attr("height", height);
    },
};

d3Linegraph = {
    update: function(el, data, interval) {
        y_values_array=[]
        for (var i=0;i<data.length;i++) {
            y_values_array.push(d3.min(data[i].data, function(d) { return d.value; }))
            y_values_array.push(d3.max(data[i].data, function(d) { return d.value; }))
        }
        var formatCount = d3.format(",.0f");
        var formatPercent = d3.format(",.1f");
        var customTimeFormat = d3.time.format.multi([
          [".%L", function(d) { return d.getMilliseconds(); }],
          [":%S", function(d) { return d.getSeconds(); }],
          ["%I:%M", function(d) { return d.getMinutes(); }],
          ["%I %p", function(d) { return d.getHours(); }],
          ["%a %d", function(d) { return d.getDay() && d.getDate() != 1; }],
          ["%b %d", function(d) { return d.getDate() != 1; }],
          ["%B", function(d) { return d.getMonth(); }],
          ["%Y", function() { return true; }]
          ]);
        var margin = {top: 20, right: 0, bottom: 40, left: 10},
            height = 200 - margin.top - margin.bottom;
        width=d3.select(el).node().getBoundingClientRect().width-margin.left
        var x = d3.time.scale()
            .range([0, width])
            .domain([new Date(interval.its*1000),new Date(interval.ets*1000)])
        yDomain=d3.extent(y_values_array)
        yMargin=(yDomain[1]-yDomain[0])*0.1
        if (yMargin==0) {
            yMargin=1
        }
        var y = d3.scale.linear()
            .domain([yDomain[0]-yMargin,yDomain[1]+yMargin])
            .rangeRound([height, 0]);
        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom")
            .ticks(7)
            .tickFormat(customTimeFormat);
        var yAxis = d3.svg.axis() .scale(y)
            .orient("left").ticks(8);
        var svg = d3.select(el).select("svg g")
        var line = d3.svg.line()
                   .x(function (d) {return x(new Date(d.ts*1000))})
                   .y(function (d) {return y(d.value)});
        lines=svg.selectAll('.line')
            .data(data, function(d) {return d.pid})
        lines.enter()
            .append('path')
            .style('fill','none')
            .style('stroke',function (d) {return d.color})
            .attr('class','line')
            .attr('d',function (d) {return line(d.data)});
        lines.exit()
            .remove()
        lines.transition()
            .duration(500)
            .style('fill','none')
            .style('stroke',function (d) {return d.color})
            .attr('class','line')
            .attr('d',function (d) {return line(d.data)});
        svg.select('.x.axis')
            .transition()
            .duration(500)
            .call(xAxis);
        svg.select('.y.axis')
            .transition()
            .duration(500)
            .call(yAxis);
    },
    create: function(el, data, interval) {
        y_values_array=[]
        for (var i=0;i<data.length;i++) {
            y_values_array.push(d3.min(data[i].data, function(d) { return d.value; }))
            y_values_array.push(d3.max(data[i].data, function(d) { return d.value; }))
        }
        var formatCount = d3.format(",.0f");
        var formatPercent = d3.format(",.1f");
        var customTimeFormat = d3.time.format.multi([
          [".%L", function(d) { return d.getMilliseconds(); }],
          [":%S", function(d) { return d.getSeconds(); }],
          ["%I:%M", function(d) { return d.getMinutes(); }],
          ["%I %p", function(d) { return d.getHours(); }],
          ["%a %d", function(d) { return d.getDay() && d.getDate() != 1; }],
          ["%b %d", function(d) { return d.getDate() != 1; }],
          ["%B", function(d) { return d.getMonth(); }],
          ["%Y", function() { return true; }]
          ]);
        var margin = {top: 20, right: 0, bottom: 40, left: 10},
            height = 200 - margin.top - margin.bottom;
        width=d3.select(el).node().getBoundingClientRect().width-margin.left
        var x = d3.time.scale()
            .range([0, width])
            .domain([new Date(interval.its*1000),new Date(interval.ets*1000)])
        yDomain=d3.extent(y_values_array)
        yMargin=(yDomain[1]-yDomain[0])*0.1
        if (yMargin==0) {
            yMargin=1
        }
        var y = d3.scale.linear()
            .domain([yDomain[0]-yMargin,yDomain[1]+yMargin])
            .rangeRound([height, 0]);
        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom")
            .ticks(7)
            .tickFormat(customTimeFormat);
        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left").ticks(8);
        var svg = d3.select(el).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        var line = d3.svg.line()
                   .x(function (d) {return x(new Date(d.ts*1000))})
                   .y(function (d) {return y(d.value)});
        svg.selectAll('.line')
            .data(data)
            .enter()
            .append('path')
            .style('fill','none')
            .style('stroke',function (d) {return d.color})
            .attr('class','line')
            .attr('d',function (d) {return line(d.data)});
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .style('shape-rendering','crispEdges')
            .call(xAxis);
        svg.append("g")
            .attr("class", "y axis")
            .style('shape-rendering','crispEdges')
            .call(yAxis);
    },
}

d3Histogram = {
    update: function(el, data) {
        var formatCount = d3.format(",.0f");
        var formatPercent = d3.format(",.1f");
        var margin = {top: 20, right: 0, bottom: 40, left: 0},
            height = 200 - margin.top - margin.bottom;
        width=d3.select(el).node().getBoundingClientRect().width
        x_values=[]
        for (i in data) {
                data[i].values=data[i].data.map( function (d) {return d.value})
        }
        x_domain=[]
        for (i in data) {
            extent=d3.extent(data[i].values)
            x_domain.push(extent[0])
            x_domain.push(extent[1])
        }
        x_domain=d3.extent(x_domain)
        xMargin=(x_domain[1]-x_domain[0])*0.1
        if (xMargin==0) {
            xMargin=1
        }
        num_ticks=parseInt((x_domain[1]-x_domain[0])/100)
        if (num_ticks<10) {
            num_ticks=10
        } else if (num_ticks>30) {
            num_ticks=30
        }
        var x = d3.scale.linear()
            .range([0, width])
            .domain([x_domain[0]-xMargin,x_domain[1]+xMargin])
        for (i in data) {
            data[i].histogram=d3.layout.histogram().bins(x.ticks(num_ticks))(data[i].values);
        }
        var y = d3.scale.linear()
            .domain([0, d3.max(data.map(function(d) { return d3.max(d.histogram, function (d) {return d.y}) }))])
            .rangeRound([0, height]);
        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom")
        var svg = d3.select(el).select("svg").select('g')
        var histograms = svg.selectAll(".histogram")
            .data(data, function (d) { return d.pid})
        histograms.enter()
            .append('g')
            .attr('class','histogram')
            .each(function (d) {
                total_values=0
                for (j in d.histogram) {
                    total_values+=d.histogram[j].y
                }
                rects=d3.select(this).selectAll('rect')
                    .data(d.histogram, function(d) {return d.x})
                    .enter()
                    .append('rect')
                    .attr("x", function (d) {return x(d.x)})
                    .attr("y", function (d) {return height - y(d.y)})
                    .style('fill',d.color)
                    .attr("width", function(d) {return x(d.x+d.dx)-x(d.x)-1})
                    .attr("height", function (d) {return y(d.y)});
                texts=d3.select(this).selectAll('text')
                    .data(d.histogram, function(d) {return d.x})
                    .enter()
                    .append('text')
                    .attr("class", "percentage")
                    .attr("dy", "1em")
                    .attr("y", function (d) {return height-y(d.y)})
                    .attr("x", function (d) {return x(d.x+d.dx/2)})
                    .attr("text-anchor", "middle")
                    .style('fill','white')
                    .text(function(d) { return formatPercent(d.y/total_values*100)+'%'});
                });
        histograms.exit().remove();
        histograms.each( function (d) {
            total_values=0
            for (j in d.histogram) {
                total_values+=d.histogram[j].y
            }
            rects=d3.select(this).selectAll('rect')
                .data(d.histogram, function(d) {return d.x})
            rects.enter()
                .append('rect')
                .attr("x", function (d) {return x(d.x)})
                .attr("y", function (d) {return height - y(d.y)})
                .style('fill',d.color)
                .attr("width", function(d) {return x(d.x+d.dx)-x(d.x)-1})
                .attr("height", function (d) {return y(d.y)});
            texts=d3.select(this).selectAll('text')
                .data(d.histogram, function(d) {return d.x})
            texts.enter()
                .append('text')
                .attr("class", "percentage")
                .attr("dy", "1em")
                .attr("y", function (d) {return height-y(d.y)})
                .attr("x", function (d) {return x(d.x+d.dx/2)})
                .attr("text-anchor", "middle")
                .style('fill','white')
                .text(function(d) { return formatPercent(d.y/total_values*100)+'%'});
            rects.exit().remove()
            texts.exit().remove()
            rects.transition()
                .duration(500)
                .attr("x", function (d) {return x(d.x)})
                .attr("y", function (d) {return height - y(d.y)})
                .style('fill',d.color)
                .attr("width", function(d) {return x(d.x+d.dx)-x(d.x)-1})
                .attr("height", function (d) {return y(d.y)});
            texts.transition()
                .duration(500)
                .attr("dy", "1em")
                .attr("y", function (d) {return height-y(d.y)})
                .attr("x", function (d) {return x(d.x+d.dx/2)})
                .attr("text-anchor", "middle")
                .style('fill','white')
                .text(function(d) { return formatPercent(d.y/total_values*100)+'%'});
            });
        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom")
        svg.select('.x.axis')
            .transition()
            .duration(500)
            .call(xAxis)
    },
    create: function(el, data) {
        var formatCount = d3.format(",.0f");
        var formatPercent = d3.format(",.1f");
        var margin = {top: 20, right: 0, bottom: 40, left: 0},
            height = 200 - margin.top - margin.bottom;
        width=d3.select(el).node().getBoundingClientRect().width
        for (i in data) {
                data[i].values=data[i].data.map( function (d) {return d.value})
        }
        x_domain=[]
        for (i in data) {
            extent=d3.extent(data[i].values)
            x_domain.push(extent[0])
            x_domain.push(extent[1])
        }
        x_domain=d3.extent(x_domain)
        xMargin=(x_domain[1]-x_domain[0])*0.1
        if (xMargin==0) {
            xMargin=1
        }
        num_ticks=parseInt((x_domain[1]-x_domain[0])/100)
        if (num_ticks<10) {
            num_ticks=10
        } else if (num_ticks>30) {
            num_ticks=30
        }
        var x = d3.scale.linear()
            .range([0, width])
            .domain([x_domain[0]-xMargin,x_domain[1]+xMargin])
        for (i in data) {
            data[i].histogram=d3.layout.histogram().bins(x.ticks(num_ticks))(data[i].values);
        }
        var y = d3.scale.linear()
            .domain([0, d3.max(data.map(function(d) { return d3.max(d.histogram, function (d) {return d.y}) }))])
            .rangeRound([0, height]);
        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom")
        var svg = d3.select(el).append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
        var histogram = svg.selectAll(".histogram")
            .data(data, function (d) { return d.pid})
            .enter()
            .append('g')
            .attr('class','histogram')
            .each(function (d) {
                total_values=0
                for (j in d.histogram) {
                    total_values+=d.histogram[j].y
                }
                rects=d3.select(this).selectAll('rect')
                    .data(d.histogram, function(d) {return d.x})
                    .enter()
                    .append('rect')
                    .attr("x", function (d) {return x(d.x)})
                    .attr("y", function (d) {return height - y(d.y)})
                    .style('fill',d.color)
                    .attr("width", function(d) {return x(d.x+d.dx)-x(d.x)-1})
                    .attr("height", function (d) {return y(d.y)});
                texts=d3.select(this).selectAll('text')
                    .data(d.histogram, function(d) {return d.x})
                    .enter()
                    .append('text')
                    .attr("class", "percentage")
                    .attr("dy", "1em")
                    .attr("y", function (d) {return height-y(d.y)})
                    .attr("x", function (d) {return x(d.x+d.dx/2)})
                    .attr("text-anchor", "middle")
                    .style('fill','white')
                    .text(function(d) { return formatPercent(d.y/total_values*100)+'%'});
                });
                        
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
            .selectAll("text")
            .style("text-anchor", "end")
            .attr("dy", ".9em")
    },
}

d3Table = {
    update: function(el, data) {
        columns=data.map(function(e) {return e.pid})
        columns.sort()
        columns.unshift('date')
        literals={'date':'Date'}
        $.each(data, function (index,e) {
            literals[e.pid]=e.datapointname
        });
        tableData=[]
        for (var i=0;i<data.length;i++) {
            for (j=0;j<data[i].data.length;j++) {
                tsDataArray=$.grep(tableData, function (e) {return e.ts == data[i].data[j].ts})
                if (tsDataArray.length == 0) {
                    tsObj={}
                    tsObj.ts=data[i].data[j].ts
                    tsObj.date=new Date(tsObj.ts*1000)
                    tsObj[data[i].pid]=data[i].data[j].value
                    tableData.push(tsObj)
                } else {
                    tsDataArray[0][data[i].pid]=data[i].data[j].value
                }
            }
        }
        tableData.sort(function(a,b) {
            return b.ts-a.ts;
        });
        var table = d3.select(el).select("table")
            tbody = table.select("tbody");
        // append the header row
        thead = table.select('thead').select("tr")
            .selectAll("th")
            .data(columns)
        thead.enter()
            .append("th")
                .text(function(column) { return literals[column]; });
        // create a row for each object in the data
        var rows = tbody.selectAll("tr")
            .data(tableData)
        rows.enter()
            .append("tr");
        // create a cell in each row for each column
        var cells = rows.selectAll("td")
            .data(function(row) {
                return columns.map(function(column) {
                    return {column: column, value: row[column]};
                });
            })
        cells.enter()
            .append("td")
            .text(function(d) { return d.value; });
        cells.transition()
            .duration(500)
            .text(function(d) { return d.value; });
        cells.exit().remove()
        rows.exit().remove()
        thead.exit().remove()
    },
    create: function(el, data) {
        columns=data.map(function(e) {return e.pid})
        columns.sort()
        columns.unshift('date')
        literals={'date':'Date'}
        $.each(data, function (e) {
            literals[e.pid]=e.datapointname
        });
        tableData=[]
        for (var i=0;i<data.length;i++) {
            for (j=0;j<data[i].data.length;j++) {
                tsDataArray=$.grep(tableData, function (e) {return e.ts == data[i].data[j].ts})
                if (tsDataArray.length == 0) {
                    tsObj={}
                    tsObj.ts=data[i].data[j].ts
                    tsObj.date=new Date(tsObj.ts*1000)
                    tsObj[data[i].pid]=data[i].data[j].value
                    tableData.push(tsObj)
                } else {
                    tsDataArray[0][data[i].pid]=data[i].data[j].value
                }
            }
        }
        tableData.sort(function(a,b) {
            return b.ts-a.ts;
        });
        var table = d3.select(el).append("table")
                .attr("class", "table table-condensed wtb")
            thead = table.append("thead"),
            tbody = table.append("tbody");
        // append the header row
        thead.append("tr")
            .selectAll("th")
            .data(columns)
            .enter()
            .append("th")
                .text(function(column) { return literals[column]; });
        // create a row for each object in the data
        var rows = tbody.selectAll("tr")
            .data(tableData)
            .enter()
            .append("tr");
        // create a cell in each row for each column
        var cells = rows.selectAll("td")
            .data(function(row) {
                return columns.map(function(column) {
                    return {column: column, value: row[column]};
                });
            })
            .enter()
            .append("td")
            .text(function(d) { return d.value; });
    },
}

