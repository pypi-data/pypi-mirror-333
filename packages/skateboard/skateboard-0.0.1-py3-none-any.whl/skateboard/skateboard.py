import eel
from importlib.resources import files

WEB_DIR = files('skateboard').joinpath('web')

class Skateboard():
    def __init__(self):
        self.chart_options = {}

        # Start eel
        eel.init(WEB_DIR, allowed_extensions=['.js', '.html', '.css'])

    def header(self, text, columns = 1, node_id = "", options = {}):
        eel.updateHeader(text, node_id, columns, options)

    def paragraph(self, text, node_id = "", columns = 1, options = {}):
        eel.updateParagraph(text, node_id, columns, options)

    def divider(self, node_id = "", columns = 1, options = {}):
        eel.updateDivider(node_id, columns, options)

    def value_chart(self, chart_data, title = "", node_id = "", columns = 1, options = None):
        if(options):
            options["title"] = title
            self.chart_options[node_id] = options

        eel.updateValueChart(chart_data, node_id, columns, self.chart_options[node_id])

    def start(self, block = True, allow_external = False):

        host = 'localhost'
        if(allow_external):
            host='0.0.0.0'
        eel.start("index.html", size=(800, 800), block = block, host = host)


    def close(self):
        pass