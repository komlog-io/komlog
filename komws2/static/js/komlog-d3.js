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

d3ResourceGraph_bis = {
    update: function (el, data,onclick) {
        width=d3.select(el).node().getBoundingClientRect().width
        height=300
        var paths = d3.select(el).select(".paths")
        var circles = d3.select(el).select(".circles")
        var texts = d3.select(el).select(".texts")
        var uris = d3.select(el).select(".uris")
        var force = d3.layout.force()
            .size([width, height])
            .nodes(data.nodes)
            .links(data.links)
            .linkDistance(width/5)
            .charge(-300)
            .on('tick',tick)
            .start()
        var path = paths.selectAll("path")
            .data(force.links(), function (d) {return d.source.index+'-'+d.target.index})
        path.exit().remove()
        path.enter().append("path")
            .attr("class", "link uri")
            .attr("marker-end", "url(#uri)")
            .attr("id", function (d) { return d.source.index+'-'+d.target.index})
        var circle = circles.selectAll("circle")
            .data(force.nodes(), function (d) {return d.id})
        circle.exit().remove()
        circle.enter().append("circle")
            .attr("r", 6)
            .on('dblclick',function (d) {
                    d3.event.defaultPrevented
                    onclick(d.uri)
            })
            .call(force.drag);
        var text = texts.selectAll("text")
            .data(force.nodes(), function (d) {return d.id})
        text.exit().remove()
        text.enter().append("text")
            .attr("x", 10)
            .attr("y", ".31em")
            .text(function(d) { return d.uri; });
        var uri = uris.selectAll("text")
            .data(force.links(), function (d) {return d.source.index+'-'+d.target.index})
        uri.exit().remove();
        uri.enter().append("text")
            .attr("x", 8)
            .attr("y", ".31em")
            .append('textPath')
            .attr("xlink:href",function (d) {return '#'+d.source.index+'-'+d.target.index})
            .attr("startOffset","10%")
            .text(function(d) { return d.path; })
        // Use elliptical arc path segments to doubly-encode directionality.
        function tick() {
          path.attr("d", linkArc);
          circle.attr("transform", transform);
          //text.attr("transform", transform);
          //uri.attr("transform", transformLink);
        }
        function linkArc(d) {
          var dx = d.target.x - d.source.x,
              dy = d.target.y - d.source.y,
              dr = 0
          return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
        }
        function transform(d) {
          return "translate(" + d.x + "," + d.y + ")";
        }
        function transformLink(d) {
          var x = d.source.x +(d.target.x - d.source.x)/1.5,
              y = d.source.y +(d.target.y - d.source.y)/2
          return "translate(" + x + "," + y + ")";
        }

    },
    create: function(el, data,onclick) {
        width=d3.select(el).node().getBoundingClientRect().width
        height=300
        var svg = d3.select(el).append("svg")
            .attr("width", width)
            .attr("height", height)
        var paths = svg.append('g').attr("class", "paths")
        var circles = svg.append('g').attr("class", "circles")
        var texts = svg.append('g').attr("class", "texts")
        var uris = svg.append('g').attr("class", "uris")
        var force = d3.layout.force()
            .size([width, height])
            .nodes(data.nodes)
            .links(data.links)
            .linkDistance(width/8)
            .charge(-300)
            .on('tick',tick)
            .start()
        svg.append("defs").selectAll("marker")
            .data(["uri"])
            .enter().append("marker")
            .attr("id", function(d) { return d; })
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 15)
            .attr("refY", -1.5)
            .attr("markerWidth", 7)
            .attr("markerHeight", 7)
            .attr("orient", "auto")
            .append("path")
            .attr("d", "M0,-5L10,0L0,5")
        var path = paths.selectAll("path")
            .data(force.links(), function (d) {return d.source.index+'-'+d.target.index})
            .enter().append("path")
            .attr("class", "link uri")
            .attr("marker-end", "url(#uri)")
            .attr("id", function (d) { return d.source.index+'-'+d.target.index})
        var circle = circles.selectAll("circle")
            .data(force.nodes(), function (d) {return d.id})
            .enter().append("circle")
            .attr("r", 6)
            .on('dblclick',function (d) {
                    d3.event.defaultPrevented
                    onclick(d.uri)
            })
            .call(force.drag);
        var text = texts.selectAll("text")
            .data(force.nodes(),function (d) {return d.id})
          .enter().append("text")
            .attr("x", 8)
            .attr("y", ".31em")
            .text(function(d) { return d.uri; });
        var uri = uris.selectAll("uris")
            .data(force.links(), function (d) {return d.source.index+'-'+d.target.index})
          .enter().append("text")
            .attr("x", 8)
            .attr("y", ".31em")
            .append('textPath')
            .attr("xlink:href",function (d) {return '#'+d.source.index+'-'+d.target.index})
            .text(function(d) { return d.path; })

        // Use elliptical arc path segments to doubly-encode directionality.
        function tick() {
          path.attr("d", linkArc);
          circle.attr("transform", transform);
          //text.attr("transform", transform);
          uri.attr("transform", transformLink);
        }

        function linkArc(d) {
          var dx = d.target.x - d.source.x,
              dy = d.target.y - d.source.y,
              dr = Math.sqrt(dx * dx + dy * dy);
          return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
        }

        function transform(d) {
          return "translate(" + d.x + "," + d.y + ")";
        }

        function transformLink(d) {
          var x = d.target.x +(d.target.x - d.source.x),
              y = d.target.y +(d.target.y - d.source.y)
          return "translate(" + x + "," + y + ")";
        }

    },
}

d3ResourceGraph = {
    update: function(el, data,onclick) {
        width=d3.select(el).node().getBoundingClientRect().width
        height=width
        diagonal=Math.sqrt(width*width+height*height)
        margin = 25
        pack = d3.layout.pack()
            .padding(50)
            .size([(width-margin),(height-margin)])
            .value(function(d) { return (d.children.length+1) })
            .sort(function (a,b) { return a.name - b.name});
        root=data
        parentUri=root.name.split('.').splice(0,root.name.split('.').length-1).join('.')
        focus = root,
        nodes = pack.nodes(root);
        $.each(nodes, function (i,d) {
          if (d.hasOwnProperty('children')){
              $.each(d.children, function (index,child) {
                  child.r*=(1-child.depth/100)
                  child.x*=(1+child.depth/100)
                  child.y*=(1+child.depth/100)
              });
          }
        });
        svg = d3.select(el).selectAll("svg")
            .attr("width",width)
            .attr("height",height)

        old_nodes = svg.selectAll('.node')
        old_nodes.remove()
        node = svg.selectAll('.node')
            .data(nodes, function (d) { return d.id})
        node_groups = node.enter().append('g')
            .attr('class','node')
            .attr("transform", function(d) { return "translate(" + (d.x-d.r) + "," + (d.y-d.r) + ")" })
        node_groups.append("text")
            .attr("class", "slide-title")
            .attr("transform", function(d) { return "translate(-" + d.name.length + ",-" + 5 + ")";})
            .text(function(d) {return d.name})
        node_groups
            .append("rect")
            .attr('class','slide')
            .attr("width", function(d) { return 2*d.r; })
            .attr("height", function(d) { return 2*d.r; })
            .attr("rx", 5)
            .attr("ry", 5)
            .style("filter", "url(#drop-shadow)")
            .on("click", function(d) { onclick(d.name), d3.event.stopPropagation(); })
        node_groups
            .filter(function (d) { return d.type==='d'||d.type==='p'||d.type==='w'})
            .append("image")
            .attr("width", 20)
            .attr("height", 20)
            .attr("xlink:href",function (d) { 
                if (d.type ==='d'){ 
                    image='ds.png'
                } else if (d.type=='p') {
                    image='dp.png'
                } else if (d.type=='w') {
                    image='wg.png'
                }
                return 'static/img/'+image
            })
            .attr('class','slide-menu')
            .attr("transform", function(d) { return "translate(-" + 20 + "," + 0 + ")";})
            .on("click", function(d) { PubSub.publish('uriActionReq',{id:d.id}), d3.event.stopPropagation(); })
        node_groups.append("text")
            .attr("class", "slide-label")
            .style("fill-opacity", function(d) { 
                if (focus === d) {
                    return 1
                } else if (d.name.split('.')[d.name.split('.').length-1].length< d.r/2) {
                    return 1
                } else {
                    return 0
                }
            })
            .attr("transform", function(d) { return "translate(" + 5 + "," + 15 + ")";})
            .text(function(d) { return focus === d ? d.name : d.name.split('.')[d.name.split('.').length-1]})
    },
    create: function (el,data,onclick) {
        width=d3.select(el).node().getBoundingClientRect().width
        height=width
        var svg = d3.select(el).select("svg")
            .attr("width",width)
            .attr("height",height)
            .append("g")
            .attr("transform", "translate(0,0)");
        var defs = svg.append("defs");
        var filter = defs.append("filter")
            .attr("id", "drop-shadow")
            .attr("height", "115%");
        filter.append("feGaussianBlur")
            .attr("in", "SourceAlpha")
            .attr("stdDeviation", 1.7)
            .attr("result", "blur");
        filter.append("feOffset")
            .attr("in", "blur")
            .attr("dx", 1)
            .attr("dy", 1)
            .attr("result", "offsetBlur");
        var feMerge = filter.append("feMerge");
        feMerge.append("feMergeNode")
            .attr("in", "offsetBlur")
        feMerge.append("feMergeNode")
            .attr("in", "SourceGraphic");
    }   
}

