
function initialize_graph(m, w, h) {

	// Add an SVG element with the desired dimensions and margin.
	var graph = d3.select("#graph").append("svg:svg")
		.attr("width", w + m[1] + m[3])
		.attr("height", h + m[0] + m[2])
		.append("svg:g")
		.attr("transform", "translate(" + m[3] + "," + m[0] + ")");

	// Add the x-axis.
	graph.append("svg:g")
		.attr('id', 'x-axis')
		.attr("class", "x axis")
		.attr("transform", "translate(0," + h + ")");

	// Add the y-axis to the left
	graph.append("svg:g")
		.attr("id", "y-axis")
		.attr("class", "y axis")
		.attr("transform", "translate(-25,0)");

	// Add a legend
	graph.append("svg:g")
		.attr("id", "legend")
		.attr("transform", "translate(0, " + (h + 50) + ")");

	var legend = d3.select("#legend");
	// Michael
	legend.append("line")
		.attr('x1', 0)
		.attr('x2', 50)
		.attr('y1', 0)
		.attr('y2', 0)
		.attr("stroke-width", 4)
	    .attr("stroke", "steelblue");
	legend.append("text")
		.attr('x', 60)
		.attr('y', 4)
		.text('Michael')
		.attr('fill', 'steelblue');

	// Sebastian
	legend.append("line")
		.attr('x1', 130)
		.attr('x2', 180)
		.attr('y1', 0)
		.attr('y2', 0)
		.attr("stroke-width", 4)
	    .attr("stroke", "lightgreen");
	legend.append("text")
		.attr('x', 190)
		.attr('y', 4)
		.text('Sebastian')
		.attr('fill', 'lightgreen');

	// Christian
	legend.append("line")
		.attr('x1', 275)
		.attr('x2', 325)
		.attr('y1', 0)
		.attr('y2', 0)
		.attr("stroke-width", 4)
	    .attr("stroke", "salmon");
	legend.append("text")
		.attr('x', 335)
		.attr('y', 4)
		.text('Christian')
		.attr('fill', 'salmon');

}


function draw_plot(url_data, m, w, h, frequency, period, aggregate) {

	post_data = {frequency: frequency,
				 period: period};

	$.getJSON(url_data, post_data, function(data){
		
		// X scale will fit all values from data[] within pixels 0-w
		var x = d3.scale.linear().domain([0, (Math.floor(period / frequency) - 1)]).range([0, w]);
		// Y scale will fit values from 0-10 within pixels h-0 (Note the inverted domain for the y-scale: bigger is up!)
		// var y = d3.scale.linear().domain([0, 10]).range([h, 0]);
		
		MICHAEL = data['MICHAEL'];
		SEBASTIAN = data['SEBASTIAN'];
		CHRISTIAN = data['CHRISTIAN'];

		Interactions.MICHAEL = MICHAEL;
		Interactions.SEBASTIAN = SEBASTIAN;
		Interactions.CHRISTIAN = CHRISTIAN;


		Interactions.aggregated = aggregate;

		// get max value among all data
		if (aggregate) {
			var AGGREGATED = []
			for (i = 0; i < MICHAEL.length; i++) {
				AGGREGATED.push (MICHAEL[i] + SEBASTIAN[i] + CHRISTIAN[i]);
			}

			var max = d3.max(AGGREGATED);

		} else {
			var max_m = d3.max(MICHAEL);
			var max_s = d3.max(SEBASTIAN);
			var max_c = d3.max(CHRISTIAN);
			var max = d3.max([max_m, max_s, max_c]);
		}

		// automatically determining max range can work something like this
		var y = d3.scale.linear().domain([0, max+1]).range([h, 0]);

		// create a line function that can convert data[] into x and y points
		var line = d3.svg.line()
			// assign the X function to plot our line as we wish
			.x(function(d,i) { 
				// verbose logging to show what's actually being done
				//console.log('Plotting X value for data point: ' + d + ' using index: ' + i + ' to be at: ' + x(i) + ' using our xScale.');
				// return the X coordinate where we want to plot this datapoint
				return x(i); 
			})
			.y(function(d) { 
				// verbose logging to show what's actually being done
				//console.log('Plotting Y value for data point: ' + d + ' to be at: ' + y(d) + " using our yScale.");
				// return the Y coordinate where we want to plot this datapoint
				return y(d); 
			})

		// Add an SVG element with the desired dimensions and margin.
		var graph = d3.select("#graph svg g");
		var x_axis = d3.select("#x-axis");
		var y_axis = d3.select("#y-axis");


		// create yAxis
		var xAxis = d3.svg.axis().scale(x).tickSize(-h).tickSubdivide(true);
		// Add the x-axis.
		x_axis.call(xAxis);

		// create left yAxis
		var yAxisLeft = d3.svg.axis().scale(y).ticks(4).orient("left");
		// Add the y-axis to the left
		y_axis.call(yAxisLeft);
		
		// Remove existing lines
		$('#graph svg g path').remove()

		// Add the line by appending an svg:path element with the data line we created above
		// do this AFTER the axes above so that the line is above the tick-lines
		if (aggregate) {
			graph.append("svg:path").attr("d", line(AGGREGATED)).attr('stroke','steelblue');
		} else {
			graph.append("svg:path").attr("d", line(MICHAEL)).attr('stroke','steelblue');
			graph.append("svg:path").attr("d", line(SEBASTIAN)).attr('stroke', 'lightgreen');
			graph.append("svg:path").attr("d", line(CHRISTIAN)).attr('stroke', 'salmon');
		}

	});

}

function update_frequency_status(to_remove) {

	$('button[data-frequency=' + to_remove + ']').removeClass('active');
	$('button[data-frequency=' + Interactions.frequency + ']').addClass('active');

}

function update_period_status(to_remove) {

	$('button[data-period=' + to_remove + ']').removeClass('active');
	$('button[data-period=' + Interactions.period + ']').addClass('active');

}


function initialize_aggregate_button(url_data, m, w, h) {

	var aggregate_btn = $('#aggregate-button');

	aggregate_btn.click(function() { 

		var new_state = !Interactions.aggregated;

		var btn = $(this);
		if (Interactions.aggregated) {
			btn.text('Aggregate');
			btn.removeClass('active');

			draw_plot(url_data, m, w, h, Interactions.frequency, Interactions.period, new_state);

		} else {
			btn.text('Aggregated');
			btn.addClass('active');

			draw_plot(url_data, m, w, h, Interactions.frequency, Interactions.period, new_state);
		}

		Interactions.aggregated = new_state;

	});
}

function initialize_refresh_button() {
	var refresh_button = $('#refresh-button');
	var icon = refresh_button.find('i')

	refresh_button.click(function() {

		icon.addClass('fa-spin');

		$.getJSON('/refresh', function(data) {
			icon.removeClass('fa-spin');
			if (data.refreshed) {

				var alert = '<div class="alert alert-success alert-dismissible" role="alert">\
							  <button type="button" class="close" data-dismiss="alert"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>\
							  Interactions data refreshed.\
							</div>'

				$('#main-content').prepend(alert);
			} else {
				console.log("Couldn't refresh data.")
			}
		});
	});

}


function initialize_buttons (url_data, m, w, h) {
	
	update_frequency_status();
	update_period_status();

	var frequency_buttons = $('button[data-frequency]');
	var period_buttons = $('button[data-period]');

	frequency_buttons.click(function () {

		var btn = $(this);

		var frequency = btn.attr('data-frequency');

		var previous_frequency = Interactions.frequency;
		Interactions.frequency = frequency;

		draw_plot(url_data, m, w, h, frequency, Interactions.period, Interactions.aggregated);

		update_frequency_status(previous_frequency);

	});

	period_buttons.click(function () {

		var btn = $(this);

		var period = btn.attr('data-period');

		var previous_period = Interactions.period;
		Interactions.period = period;

		draw_plot(url_data, m, w, h, Interactions.frequency, period, Interactions.aggregated);
		
		update_period_status(previous_period);

	});

}








