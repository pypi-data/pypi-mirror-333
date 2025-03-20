from src.skateboard import Skateboard
import eel
import math
import time

board = Skateboard()

board.header("Hello!")
board.paragraph("Hello from skateboard!")
board.divider()

board.paragraph("Here is a number being set live from python", columns=2)
board.paragraph("number", "value", columns=2)
board.divider()

board.paragraph("Here are some charts!")

main_chart_options = {
    "yUnit": "A",
    "xUnit": "s",
    "tooltip": False,
    "showSymbol": False,
    "filled": True,
    "zoom": False,
    "color": "#85ffa5",
    "gaugeValue": True,
    "animation": False,
    "hideAxes": True
}

board.value_chart([], node_id = "value_chart", columns=2, options=main_chart_options)
board.value_chart([], node_id = "value_chart2", columns=2, options=main_chart_options)


second_chart_options = {
    "yUnit": "m",
    "xUnit": "s",
    "tooltip": True,
    "showSymbol": False,
    "filled": False,
    "zoom": False,
    "color": "#d9962b",
    "gaugeValue": False,
    "animation": False,
    "hideAxes": False
}

board.value_chart([],  node_id = "value_chart3", columns=1, title="Chart title!", options=second_chart_options)

board.start(block = False, allow_external = False)

chart_data = []
chart_data2 = []

for i in range(10000):
    board.paragraph(i, "value")
    print(i)

    if(len(chart_data) > 300):
        chart_data.pop(0)
    
    if(len(chart_data2) > 1003):
        chart_data2.pop(0)

    chart_data.append([i/50, math.sin(i/30)])
    chart_data2.append([i/50, math.cos(i/30)])
    board.value_chart(chart_data, node_id = "value_chart")
    board.value_chart(chart_data, node_id = "value_chart2")

    board.value_chart(chart_data2, node_id = "value_chart3")


    eel.sleep(0.02)

# board.close()