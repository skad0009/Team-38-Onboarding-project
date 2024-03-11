document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("UV_Index").addEventListener("submit", function(event) {
        event.preventDefault(); // 阻止表单默认提交行为
        const input1 = document.getElementById("location").value;
        const requestURL = `/uv_index?location=${input1}`;

        // 发起AJAX请求
        fetch(requestURL)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok.'); // 抛出错误，被后面的catch捕获
                }
                return response.json();
            })
            .then(data => {
                // 更新页面上的结果
                if(data.uv_index !== undefined) {
                    document.getElementById("UVIndex").textContent = data.uv_index;
                } else {
                    // 处理数据返回成功，但结构不符合预期
                    document.getElementById("UVIndex").textContent = "Please enter a correct location in English.";
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // 处理请求失败的情况
                document.getElementById("UVIndex").textContent = "There was an error processing your request. Please try again.";
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
        margin = { top: 20, right: 20, bottom: 30, left: 50 },
        width = +svg.attr("width") - margin.left - margin.right,
        height = +svg.attr("height") - margin.top - margin.bottom,
        g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);

    // 定义x和y轴的比例尺
    const x = d3.scaleLinear()
    .domain([0, 24]) // 设置x轴的数据范围
    .range([0, width]); // 设置x轴在画布上的像素范围

    const y = d3.scaleLinear()
    .domain([0, 11]) // 设置y轴的数据范围
    .range([height, 0]); // 设置y轴在画布上的像素范围


    // 定义颜色比例尺
    const color = d3.scaleOrdinal(d3.schemeCategory10); // 使用内置的颜色方案，共10种颜色

    // 处理数据，分城市组织
    const cities = Array.from(new Set(data.map(d => d.city)));
    const data_city = cities.map(city => {
        return {
            city: city,
            values: data.filter(d => d.city === city).map(d => ({ hour: +d.hour, uvIndex: +d.uvIndex }))
        };
    });

    // 添加x和y轴
    g.append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(d3.axisBottom(x));
    g.append("g")
        .call(d3.axisLeft(y));



    // 定义线的生成器
    const line = d3.line()
        .x(d => x(d.hour))
        .y(d => y(d.uvIndex));

    // 添加工具提示
    const tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

    // 绘制每个城市的UV指数曲线
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

    // 为每个数据点创建圆圈并添加工具提示的交互
cityLines.selectAll(".point")
    .data(d => d.values)
    .enter().append("circle")
    .attr("class", "point")
    .attr("cx", d => x(d.hour))
    .attr("cy", d => y(d.uvIndex))
    .attr("r", 5) // 点的大小
    .style("fill", d => color(d.city))

 .on("mouseover", function(event, d) {
    tooltip.transition()
        .duration(200)
        .style("opacity", .9);
    tooltip.html(`Time: ${d.hour}:00<br/>UV Index: ${d.uvIndex}`)
        .style("left", (event.pageX + 10) + "px")  // 加10个像素，防止遮挡
        .style("top", (event.pageY + 10) + "px");  // 同上
})
.on("mouseout", function(event, d) {
    tooltip.transition()
        .duration(500)
        .style("opacity", 0);
});

    // 选中所有的线条，并为它们添加鼠标悬停事件
cityLines.selectAll(".line")
    .on("mouseover", function() {
        // 除了当前悬停的线条，其他所有线条透明度降低
        d3.selectAll(".line")
            .style("opacity", 0.2);
        // 当前悬停的线条保持不变
        d3.select(this)
            .style("opacity", 1)
            .style("stroke-width", "6px"); // 可选，增加线条宽度以增强视觉效果
    })
    .on("mouseout", function() {
        // 鼠标移开后恢复所有线条的透明度和宽度
        d3.selectAll(".line")
            .style("opacity", 1)
            .style("stroke-width", "3px");
    });


    // 添加图例
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








