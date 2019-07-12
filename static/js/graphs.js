var noticeDataState;
var noticeDataCounty;
var parallelNoticeDataState;
var parallelNoticeDataCounty;
var county={};
var state={};
var date={};
var category={};
var auctionByState={};
var licenseByState={};
var electionByState={};
var orgByState={};
var proByState={};
var newspaper={};
var usChart;
var pieChart;
var rowChart;
var topicsdata;
var topicChart;

var d3Us;
var dcUs;


queue()
    .defer(d3.json, "/noticesFinal/projects")
    .defer(d3.json,"/noticesFinal/parallel")
    .defer(d3.json,"/noticesFinal/topics")
    .await(init);

function init(error, projectsJson, parallelJson,topicsdataJson) {

	noticeDataState = projectsJson
	noticeDataCounty = projectsJson
	parallelNoticeDataState=parallelJson
    topicsdata=topicsdataJson

	console.log(noticeDataState)

	noticeDataState.forEach(function(d) {
        county[d.id] = d["county"]
        state[d.id] = d["state"]
        date[d.id] = d["month_year"]
		category[d.id]=d["category"]
		newspaper[d.id]=d["newspaper"]
    });


    populateDashBoard();
    populateCountyWiseDashboard();
    document.getElementById("btn_dashboard").click();
    populate_parallel();
    word_analysis()

}

function populateDashBoard(){

	var ndx = crossfilter(noticeDataState);
	//Define Dimensions
	var dateDim = ndx.dimension(function(d) { return d["year"]; });
	var stateTypeDim = ndx.dimension(function(d) { return d["state"]; });
	var countyLevelDim = ndx.dimension(function(d) { return d["county"]; });
	var categoryLevelDim = ndx.dimension(function(d) { return d["category"]; });
	var stateTypeDim2 = ndx.dimension(function(d) { return d["state"]; });
	var newspaperDim = ndx.dimension(function(d){return d['newspaper']});

	var all=ndx.groupAll();
	var totalNoticesByState=stateTypeDim.group();
	var noticesByCategory = categoryLevelDim.group();
	var noticesByDate=dateDim.group();
	var totalNoticesByState2=stateTypeDim2.group();
	var noticesByNewspaper=newspaperDim.group();

	console.log(totalNoticesByState)
	//usChart = dc.geoChoroplethChart("#us-chart");
	//	pieChart = dc.pieChart("#poverty-level-row-chart");
	rowChart = dc.rowChart("#time-chart");
	barChart = dc.barChart("#us-chart");
	timeChart = dc.barChart("#resource-type-row-chart");
	newsChart = dc.pieChart("#poverty-level-row-chart");

	var max_news = noticesByNewspaper.top
	var max_state = totalNoticesByState.top(1)[0].value;
	var max_time = noticesByDate.top(1)[0].value;

	rowChart
		.width(500)
		.height(650)
		.margins({top: 20, right: 65, bottom: 30, left: 30})
		.transitionDuration(1000)
		.x(d3.scale.ordinal().domain(categoryLevelDim))
		.dimension(categoryLevelDim)
		.group(noticesByCategory)
		.elasticX(true);
		/*.xAxisLabel("Year")*/
		//.yAxisLabel("Notices By State")


	barChart
		.width(900)
		.height(300)
		.margins({top: 10, right: 60, bottom: 30, left: 50})
		.transitionDuration(1000)
		.x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .y(d3.scale.linear().domain([0, max_state]))
		.dimension(stateTypeDim)
		.group(totalNoticesByState)
		.elasticX(true)
		.elasticY(true);

	timeChart
		.width(500)
		.height(290)
		.margins({top: 20, right: 90, bottom: 30, left: 55})
		.transitionDuration(1000)
		.x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .y(d3.scale.linear().domain([0, max_state]))
		.dimension(dateDim)
		.group(noticesByDate)
		.elasticX(true)
		.elasticY(true);

	newsChart
        .width(470)
        .height(290)
        .innerRadius(50)
        .dimension(newspaperDim)
        .group(noticesByNewspaper)
        .slicesCap(5)
        .othersGrouper(false)
        .renderLabel(false)
        .legend(dc.legend());

	dc.renderAll();
};

function populateCountyWiseDashboard() {


	console.log(noticeDataState)
	//Create a Crossfilter instance
	var ndx = crossfilter(noticeDataState);

	//Define Dimensions
	var dateDim = ndx.dimension(function(d) { return d["year"]; });
	var stateTypeDim = ndx.dimension(function(d) { return d["state"]; });
	var countyLevelDim = ndx.dimension(function(d) { return d["county"]; });
	var categoryLevelDim = ndx.dimension(function(d) { return d["category"]; });
	var stateTypeDim2 = ndx.dimension(function(d) { return d["state"]; });
	var newspaperDim = ndx.dimension(function(d){return d['newspaper']});

	//Define groups
	var all=ndx.groupAll();
	var totalNoticesByState=stateTypeDim.group();
	var noticesByCategory = categoryLevelDim.group();
	var noticesByDate=dateDim.group();
	var totalNoticesByState2=stateTypeDim2.group();
	var noticesByNewspaper=newspaperDim.group();
	var noticesByCounty=countyLevelDim.group();


	var selectMenu = dc.selectMenu('#select')
      .dimension(stateTypeDim)
      .group(totalNoticesByState)
      .title(function (d){
        return d.key;
      })
      .filter("Arizona");


	rowChart = dc.rowChart("#time-chart2");
	barChart = dc.barChart("#us-chart2");
	timeChart = dc.lineChart("#resource-type-row-chart2");
	newsChart = dc.pieChart("#poverty-level-row-chart2");

 	var max_news = noticesByNewspaper.top
	var max_state = totalNoticesByState.top(1)[0].value;
	var max_time = noticesByDate.top(1)[0].value;
	var max_cat = noticesByCategory.top(1)[0].value;

	rowChart
		.width(500)
		.height(650)
		.margins({top: 20, right: 65, bottom: 30, left: 30})
		.transitionDuration(1000)
		.x(d3.scale.ordinal().domain(countyLevelDim))
		.dimension(countyLevelDim)
		.group(noticesByCounty)
		.elasticX(true)
		.cap(10)
		.othersGrouper(false);
		/*.xAxisLabel("Year")*/
		//.yAxisLabel("Notices By State")


	barChart
		.width(900)
		.height(300)
		.margins({top: 10, right: 60, bottom: 70, left: 50})
		.transitionDuration(1000)
		.x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .y(d3.scale.linear().domain([0, max_cat]))
		.dimension(categoryLevelDim)
		.group(noticesByCategory,"notices")
		.elasticX(true)
		.elasticY(true)
		.renderlet(function (chart) {
                chart.selectAll("g.x text")
                .attr('transform', "rotate(-45)");
            });


	timeChart
		.width(500)
		.height(290)
		.margins({top: 20, right: 90, bottom: 30, left: 55})
		.transitionDuration(1000)
		.x(d3.scale.ordinal())
        .xUnits(dc.units.ordinal)
        .y(d3.scale.linear().domain([0, max_state]))
		.dimension(dateDim)
		.group(noticesByDate)
		.elasticX(true)
		.elasticY(true);

	newsChart
        .width(470)
        .height(290)
        .innerRadius(50)
        .dimension(newspaperDim)
        .group(noticesByNewspaper)
        .slicesCap(5)
        .othersGrouper(false)
        .renderLabel(false)
        .legend(dc.legend());

 	dc.renderAll();
};


function populate_parallel()
{
    var ndx = crossfilter(noticeDataState);
	//Define Dimensions
	var dateDim = ndx.dimension(function(d) { return d["year"]; });
	var stateTypeDim = ndx.dimension(function(d) { return d["state"]; });
	var countyLevelDim = ndx.dimension(function(d) { return d["county"]; });
	var categoryLevelDim = ndx.dimension(function(d) { return d["category"]; });
	var newspaperDim = ndx.dimension(function(d){return d['newspaper']});

	var all=ndx.groupAll();
	console.log('inside populate_parallel');
	console.log(parallelNoticeDataState);
	/*var selectMenu2 = dc.selectMenu('#select2')
      .dimension(categoryLevelDim)
      .group(categoryLevelDim.group())
      .title(function (d){
        return d.key;
      })
      .filter("Auctions and Bids");
	var selected=selectMenu2.filter()

	console.log(selectMenu2.filter())*/

    var margin = {top: 30, right: 40, bottom: 20, left: 200};
    var width = 1260 - margin.left - margin.right;
    var height = 500 - margin.top - margin.bottom;
    var dimensions = [
    {
        name: "state",
        scale: d3.scale.ordinal().rangePoints([0, height]),
        type: String
    },
        {
        name: "notices_count",
        scale: d3.scale.linear().range([height, 0]),
        type: Number
    },
        {
        name: "population_2017",
        scale: d3.scale.linear().range([height, 0]),
        type: Number
    },

        {
        name: "unemployment",
        scale: d3.scale.linear().range([height, 0]),
        type: Number
    },{
        name: "Tax Notice",
        scale: d3.scale.linear().range([height, 0]),
        type: Number
    },
        {
        name: "uneducated",
        scale: d3.scale.linear().range([height, 0]),
        type: Number
    },
        {
        name: "pov",
        scale: d3.scale.linear().range([height, 0]),
        type: Number
    },
        {
        name: "Auctions and Bids",
        scale: d3.scale.linear().range([height, 0]),
        type: Number
    },

        {
        name: "Foreclosures",
        scale: d3.scale.linear().range([height, 0]),
        type: Number
    }

        ];

    var dragging = {};
    var foreground;
    var background;
    var y = {};

    var x = d3.scale.ordinal()
        .domain(dimensions.map(function(d) { return d.name; }))
        .rangePoints([0, width]);

    var line = d3.svg.line()
        .defined(function(d) { return !isNaN(d[1]); });

    var yAxis = d3.svg.axis()
        .orient("left");

    var svg = d3.select("#parallel")
                .append("g")
                .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var dimension = svg.selectAll(".dimension")
        .data(dimensions)
        .enter().append("g")
        .attr("class", "dimension")
        .attr("transform", function(d) { return "translate(" + x(d.name) + ")"; });

    //trying to set y
    d3.keys(parallelNoticeDataState[0]).filter(function(d) {
        y[d]=d3.scale.linear().domain(d3.extent(parallelNoticeDataState, function(p) { return +p[d]; })).range([height, 0]);
        return d != "name" && y[d];
    });

    dimensions.forEach(function(dimension) {
        dimension.scale.domain(dimension.type === Number
            ? d3.extent(parallelNoticeDataState, function(d) { return +d[dimension.name]; })
            : parallelNoticeDataState.map(function(d) { return d[dimension.name]; }));
      });

    var background = svg.append("g")
        .attr("class", "background")
        .selectAll("path")
        .data(parallelNoticeDataState)
        .enter().append("path")
        .attr("d", draw);

    var foreground = svg.append("g")
        .attr("class", "foreground")
        .selectAll("path")
        .data(parallelNoticeDataState)
        .enter().append("path")
        .attr("d", draw);

    function draw(d) {
      return line(dimensions.map(function(dimension) {
        return [x(dimension.name), dimension.scale(d[dimension.name])];
      }));
    }

    dimension.append("g")
        .attr("class", "vaxis")
        .each(function(d) { d3.select(this).call(yAxis.scale(d.scale)); })
        .append("text")
        .attr("class", "title")
        .attr("text-anchor", "middle")
        .attr("y", -9)
        .text(function(d) { return d.name; });

    // Rebind the axis data to simplify mouseover.
    svg.select(".vaxis").selectAll("text:not(.title)")
        .attr("class", "label")
        .data(parallelNoticeDataState, function(d) { return d.name || d; });

    //for brushing
    // Add a group element for each dimension.
    var g = dimension.call(d3.behavior.drag()
        .origin(function(d) { console.log({x: x(d.name)});return {x: x(d.name)}; })
        .on("dragstart", function(d) {
            dragging[d.name] = x(d.name);
            background.attr("visibility", "hidden");
        })
        .on("drag", function(d) {
            dragging[d.name] = Math.min(width, Math.max(0, d3.event.x));
            foreground.attr("d", path); //ch path to draw
            dimensions.sort(function(a, b) { return position(a.name) - position(b.name); });
            x.domain(dimensions);
            g.attr("transform", function(d) { return "translate(" + position(d.name) + ")"; })
        })
        .on("dragend", function(d) {
            delete dragging[d.name];

            transition(d3.select(this)).attr("transform", "translate(" + x(d.name) + ")");
            transition(foreground).attr("d", path);//ch

            background
                .attr("d", path)//ch
                .transition()
                .delay(500)
                .duration(0)
                .attr("visibility", null);
        }
    ));

    // Add and store a brush for each axis.
    g.append("g")
    .attr("class", "brush")
    .each(function(d) {
        d3.select(this).call(y[d.name].brush = d3.svg.brush().y(y[d.name]).on("brushstart", brushstart).on("brush", brush));
    })
    .selectAll("rect")
    .attr("x", -8)
    .attr("width", 16);

    // setting up brushing
    // Add a group element for each dimension.
    function position(d) {
        var v = dragging[d];
        return v == null ? x(d) : v;
    }

    function transition(g) {
      return g.transition().duration(500);
    }

    // Returns the path for a given data point.
    function path(d) {
      return line(dimensions.map(function(p) {
        return [position(p.name), y[p.name](d[p.name])];
      }));
    }

    function brushstart() {
      d3.event.sourceEvent.stopPropagation();
    }

    // Handles a brush event, toggling the display of foreground lines.
    function brush() {
        var actives = dimensions.filter(function(p) { return !y[p.name].brush.empty(); }),
        extents = actives.map(function(p) { return y[p.name].brush.extent(); });
        foreground.style("display", function(d) {
        return actives.every(function(p, i) {
        return extents[i][0] <= d[p.name] && d[p.name] <= extents[i][1];
        }) ? null : "none";
        });
    }
    dc.renderAll();

    };

function openTabClick(evt, container, index) {
	//    console.log("Tarun", index);
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(container).style.display = "block";
    evt.currentTarget.className += " active";
};

function contains(array, obj) {
    var i = array.length;
    while (i--) {
        if (array[i] === obj) {
            return true;
        }
    }
    return false;
};


function word_analysis()
{
    var ndx = crossfilter(topicsdata);
    console.log('inside topic model')
    console.log(topicsdata)
	//Define Dimensions
	var docDim = ndx.dimension(function(d) { return d["Dominant_Topic"]; });
	//var keyDim = ndx.dimension(function(d) { return d["Keywords"]; });


	var all=ndx.groupAll();
	var totalDocsByState=docDim.group();

topicChart=dc.pieChart("#poverty-level-row-chart3");

	//usChart = dc.geoChoroplethChart("#us-chart");
	//	pieChart = dc.pieChart("#poverty-level-row-chart");
	//rowChart = dc.rowChart("#time-chart3");
	//barChart = dc.barChart("#us-chart");
	//timeChart = dc.barChart("#resource-type-row-chart");
	//newsChart = dc.pieChart("#poverty-level-row-chart");



	topicChart
		.width(470)
        .height(290)
        .innerRadius(50)
        .dimension(docDim)
        .group(totalDocsByState)
        .slicesCap(4)
        .othersGrouper(false)
        .renderLabel(false)
        .legend(dc.legend());



	dc.renderAll();
};