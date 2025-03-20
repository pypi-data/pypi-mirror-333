

document.addEventListener("DOMContentLoaded", function () {
    console.log("loaded");
});

charts = {}

eel.expose(updateHeader);
function updateHeader(header_text, node_id, columns, options) {
    const {node: node, is_template: is_template} = findTemplateOrCreate("headerTemplate", node_id);
    if(is_template)
        node.querySelector("div").style.flex = `1 1 calc((100% / ${columns}) - (20px))`;

    node.querySelector("h2").textContent = header_text;

    if(is_template)
        document.getElementById("mainContainer").appendChild(node);
}

eel.expose(updateParagraph);
function updateParagraph(paragraph_text, node_id, columns, options) {
    const {node: node, is_template: is_template} = findTemplateOrCreate("paragraphTemplate", node_id);
    if(is_template)
        node.querySelector("div").style.flex = `1 1 calc((100% / ${columns}) - (20px))`;

    node.querySelector("p").textContent = paragraph_text;

    if(is_template)
        document.getElementById("mainContainer").appendChild(node);
}

eel.expose(updateDivider);
function updateDivider(node_id, columns, options) {
    const {node: node, is_template: is_template} = findTemplateOrCreate("dividerTemplate", node_id);
    if(is_template)
        node.querySelector("div").style.flex = `1 1 calc((100% / ${columns}) - (20px))`;

    if(is_template)
        document.getElementById("mainContainer").appendChild(node);
}

eel.expose(updateValueChart);
function updateValueChart(chart_data, node_id, columns, options){
    const {node: node, is_template: is_template} = findTemplateOrCreate("valueChartTemplate", node_id);
    if(is_template){
        console.log(columns);
        node.querySelector("div").style.flex = `1 1 calc((100% / ${columns}) - (20px))`;
    }

    var chart_options = {
        title: {
            text: options.title
        },
        grid:{
            left: 50,
            right: 30,
            top: 20,
            bottom: 30
        },
        xAxis: {
            type: "value",
        },
        yAxis: {
            type: "value",
        },
        series: [
            {
                type: "line",
                showSymbol: option_or(options, "showSymbol", false),
                itemStyle: {

                }
            }
        ],
        animation: false
    }
    
    if(chart_data.length > 0){
        chart_options.series[0].data = chart_data
    }

    if(chart_data.length > 2){
        chart_options.xAxis.min = chart_data[0][0];
        chart_options.xAxis.max = chart_data[chart_data.length - 1][0]
    }

    if(options.hideAxes){
        // TODO: Adjust grid
        chart_options.xAxis.show = false;
        chart_options.yAxis.show = false;

        chart_options.grid = {
            left: 5,
            right: 5,
            top: 5,
            bottom: 5
        }
    }

    if(options.gaugeValue && chart_data.length > 0){
        latestValue = chart_data[chart_data.length - 1][1];
        chart_options.graphic = [
            {
                type: 'text',
                left: 'center',
                top: "center",
                style: {
                    text: `${latestValue.toFixed(2)} ${option_or(options, "yUnit", "")}`, // Display last value
                    font: 'bold 48px Arial',
                    fill: "#ffffff", // option_or(options, "color", "#ffffff"),
                    textAlign: 'center'
                },
                silent: true,
                zlevel: 1,
            }
        ];
    }

    if(options.tooltip){
        chart_options.tooltip = {
            trigger: 'axis',
            axisPointer: {
                type: 'cross'
            }
        }
    }

    if(options.yUnit){
        chart_options.yAxis.axisLabel = {
            formatter: '{value} ' + options.yUnit
        }
    }

    if(options.xUnit){
        chart_options.xAxis.axisLabel = {
            formatter: '{value} ' + options.xUnit
        }
    }

    if(options.filled == true){
        chart_options.series[0].areaStyle ={};
    }

    if(options.zoom){
        chart_options.dataZoom = [
            {
              type: 'inside',
            },
            {

            }
          ]
    }

    if(options.color){
        chart_options.series[0].itemStyle.color = options.color;
    }

    var chart;

    if(is_template){
        chart = echarts.init(node.querySelector(".valueChart"));
        charts[node_id] = chart;
    } else {
        chart = charts[node_id]
    }
    chart.setOption(chart_options);

    if(is_template)
        document.getElementById("mainContainer").appendChild(node);

    chart.resize();
}

function findTemplateOrCreate(template_id, node_id){
    
    // Check if element exists
    if(node_id != "" && document.getElementById(node_id) ){
        // console.log("updating existing element");
        // Return existing element
        const existingNode = document.getElementById(node_id)
        return {node: existingNode, is_template: false};
    } else {
        // console.log("adding new element");
        // otherwise, make new element
        const template = document.getElementById(template_id);
        const newNode = template.content.cloneNode(true);
        if(node_id != "")
            newNode.querySelector('div').id = node_id;
        return {node: newNode, is_template: true}
    }
}

function option_or(options, key, default_value){
    if(options[key]){
        return options[key]
    } else {
        return default_value
    }
}