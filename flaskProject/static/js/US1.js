
//User current time
function displayCurrentTime() {
  // Create a new Date object
  const now = new Date();
  // Format the time as desired - here it's in a 24-hour format with minutes and seconds
  const formattedTime = now.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
  // Select the element where you want to display the time
  const timeDisplay = document.getElementById('timeDisplay');
  // Set the text content of the selected element to the formatted time
  timeDisplay.textContent = formattedTime;
}
// Call displayCurrentTime every second to update the clock
setInterval(displayCurrentTime, 1000);


document.addEventListener("DOMContentLoaded", function() {
    function getUserCity() {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(function(position) {
                fetch(`https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${position.coords.latitude}&longitude=${position.coords.longitude}&localityLanguage=us`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('userCity').textContent = data.city || 'unknown city';
                })
                .catch(error => {
                    console.error('Positioning error:', error);
                    document.getElementById('userCity').textContent = 'Unable to get current city';
                });
            }, function(error) {
                document.getElementById('userCity').textContent = error.message || 'Unable to obtain location permission';
            });
        } else {
            document.getElementById('userCity').textContent = 'The browser does not support geolocation';
        }
    }

    // Get and display the user's current city
    getUserCity();

    document.getElementById("searchForm").addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent form default submission behavior

        // Get the selected position from the form
        const selectedLocation = document.getElementById("location").value;

        // Build the correct request URL
        const requestURL = `/uv_index?location=${selectedLocation}`;

        // Initiate AJAX request
        fetch(requestURL)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok.'); // If the network response is not ok, throw an error
                }
                return response.json(); // Parse the response in JSON format
            })
            .then(data => {
                //Update the page based on the returned data
                const uvIndexElement = document.getElementById("UVIndex");
                const uvInfoElement = document.getElementById("UVIndexInfo");
                if(data.uv_index !== undefined) {
                    uvIndexElement.textContent = data.uv_index;
                    if(data.uv_index >= 0 && data.uv_index <= 2) {
                        uvInfoElement.textContent = "Minimal risk for harm. Wear sunglasses on bright days.";
                    } else if(data.uv_index > 2 && data.uv_index <= 5) {
                        uvInfoElement.textContent = "Seek shade during midday hours, cover up and wear sunscreen.";
                    } else if(data.uv_index > 5 && data.uv_index <= 7) {
                        uvInfoElement.textContent = "Stay in shade near midday when the sun is strongest.";
                    } else if(data.uv_index > 7 && data.uv_index <= 10) {
                        uvInfoElement.textContent = "Take extra precautions. Unprotected skin will be damaged.";
                    } else if(data.uv_index > 10) {
                        uvInfoElement.textContent = "Avoid the sun between 11AM and 3PM.";
                    } else {
                        uvInfoElement.textContent = "";
                        // If the UV index value is not within the expected range, no information is displayed
                    }
                } else {
                    uvIndexElement.textContent = "No UV index data available for the selected location.";
                    uvInfoElement.textContent = "";
                    //Do not display information when there is no UV index data
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // If the request fails, notify the user
                document.getElementById("UVIndex").textContent = "Error fetching UV index data. Please try again later.";
                document.getElementById("UVIndexInfo").textContent = ""; //Do not display information when an error occurs
            });
    });
});


//fetch  predict data
fetch('/get_uv_forecast')
    .then(response => response.json())
    .then(data => {
        visualizeData(data);
    })
    .catch(error => console.error('Error fetching UV forecast data:', error));

function visualizeData(data) {
   const svg = d3.select("#line-chart"),
        margin = { top: 20, right: 20, bottom: 30, left: 50 }, // Adjust left margin for axis labels if needed
        width = svg.node().getBoundingClientRect().width - margin.left - margin.right,
        height = svg.node().getBoundingClientRect().height - margin.top - margin.bottom,
        g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

    // Define the scale of the x and y axes
    const x = d3.scaleLinear()
    .domain([0, 24]) //Set the data range of the x-axis
    .range([0, width]); //Set the pixel range of the x-axis on the canvas

    const y = d3.scaleLinear()
    .domain([0, 11]) //Set the data range of the y-axis
    .range([height, 0]); //Set the pixel range of the y-axis on the canvas


    //Define color scale
    const color = d3.scaleOrdinal(d3.schemeCategory10);
    // Use the built-in color scheme, a total of 10 colors

    // Process data and organize by city
    const cities = Array.from(new Set(data.map(d => d.city)));
    const data_city = cities.map(city => {
        const filteredData = data.filter(d => d.city === city);
        return {
            city: city,
            values: filteredData.map(d => ({
                hour: +d.hour, // Ensure conversion to number via unary plus sign
                uvIndex: +d.uvIndex
            }))
        };
    });

    console.log(data_city);

    //Add x and y axes
    g.append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(d3.axisBottom(x));
    g.append("g")
        .call(d3.axisLeft(y));

    //Add titles for the x and y axes
g.append("text")
  .attr("text-anchor", "end")
  .attr("x", width + margin.left -4)
  .attr("y", height + margin.bottom ) // Adjust the y-position to align with the bottom of the x-axis
  .text("Hour (h)");


g.append("text")
  .attr("text-anchor", "end")

  .attr("y", margin.left - 20) // Adjust the y-position to align with the left side
  .attr("x", -margin.top + 100) // Adjust the x-position to align with the top of the y-axis
  .text("UV Index");



    //define line generator
    const line = d3.line()
        .x(d => x(d.hour))
        .y(d => y(d.uvIndex));

   //Add tooltip
    const tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    // Draw the UV index curve of each city
    const cityLines = g.selectAll(".city")
        .data(data_city)
        .enter().append("g")
        .attr("class", "city");

    cityLines.append("path")
    .attr("class", "line")
    .attr("d", d => line(d.values))
    .style("stroke", d => color(d.city))
    .attr("fill", "none")
    .attr("stroke-width", 3);

   // Create circles and add tooltip interactions for each data point
    cityLines.selectAll(".point")
    .data(d => d.values)
    .enter().append("circle")
    .attr("class", "point")
    .attr("cx", d => x(d.hour))
    .attr("cy", d => y(d.uvIndex))
    .attr("r", 4)
    .style("fill", d => color(d.city))


    .on("mouseover", function(event, d) {
        tooltip.transition()
        .duration(1000)
        .style("opacity", .9);
        tooltip.html(`Time: ${d.hour}:00<br/>UV Index: ${d.uvIndex}`)
        .style("left", (event.pageX + 10) + "px")
        .style("top", (event.pageY + 10) + "px");
    })
    .on("mouseout", function(event, d) {
        tooltip.transition()
        .duration(500)
        .style("opacity", 0);
});

   // Select all lines and add mouseover events to them
cityLines.selectAll(".line")
    .on("mouseover", function() {
        // Reduce the transparency of all lines except the currently hovered line
        d3.selectAll(".line")
            .style("opacity", 0.2);
        //The currently hovered line remains unchanged
        d3.select(this)
            .style("opacity", 1)
            .style("stroke-width", "6px");
    })
    .on("mouseout", function() {
        //Restore the transparency and width of all lines after the mouse is moved away
        d3.selectAll(".line")
            .style("opacity", 1)
            .style("stroke-width", "3px");
    });


    //Add legend
    const legend = svg.selectAll(".legend")
        .data(cities)
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", (d, i) => `translate(0,${i * 20})`);

    legend.append("rect")
        .attr("x", width - 20)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    legend.append("text")
        .attr("x", width - 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(d => d);
}








