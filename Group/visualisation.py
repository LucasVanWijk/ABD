from mesa.visualization.modules import NetworkModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from Infect_Model import BaseModel
from mesa.visualization.UserParam import UserSettableParameter


def network_portrayal(G):

    portrayal = dict()
    portrayal["nodes"] = []

    for n in G.nodes.data():
        portrayal["nodes"].append(
            {
                "size": 6,
                "color": n[1]["color"],
            }
        )

    portrayal["edges"] = []
    for source, target in G.edges:
        portrayal["edges"].append(
            {
                "source": source,
                "target": target,
                "color": "red",
                "width": 1,
            }
        )

    return portrayal


class Time(TextElement):
    def render(self, model):
        time = model.date
        return str(time)


network = NetworkModule(network_portrayal, 800, 800, library="d3")
chart = ChartModule([{"Label": "infected",
                      "Color": "Green"}],
                    data_collector_name='datacollector')
model_params = {
    "p_nodes": UserSettableParameter("number", "prob nodes", value=0.04),
    "healthy_N": UserSettableParameter("slider", "amount healthy", 100, 1, 500),
    "sick_N": UserSettableParameter("slider", "amount sick", 10, 1, 500),
}

model_params["network_params"] = [
        (model_params["healthy_N"].value + model_params["sick_N"].value, "House", "purple"),
        (15, "Work", "yellow"),
        (5, "Shop", "green"),
        (5, "Bar", "Brown")
]

server = ModularServer(BaseModel,
                       [network, Time(), chart],
                       "Infected model",
                       model_params
                       )
server.port = 8521 # The default
server.launch()
