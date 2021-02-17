from mesa.visualization.modules import NetworkModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from Infect_Model import BaseModel
from mesa.visualization.UserParam import UserSettableParameter


def network_portrayal(G):

    portrayal = dict()
    portrayal["nodes"] = [
        {
            "size": 6,
            "color": "blue",
        }
        for _ in G.nodes
    ]

    portrayal["edges"] = [
        {
            "source": source,
            "target": target,
            "color": "red",
            "width": 1,
        }
        for (source, target) in G.edges
    ]

    return portrayal


class Time(TextElement):
    def render(self, model):
        time = model.date
        return str(time)


network = NetworkModule(network_portrayal, 1000, 1000, library="d3")
chart = ChartModule([{"Label": "infected",
                      "Color": "Green"}],
                    data_collector_name='datacollector')
model_params = {
    "n_nodes": UserSettableParameter("slider", "amount nodes", 15, 1, 30),
    "p_nodes": UserSettableParameter("number", "prob nodes", value=0.5),
    "healthy_N": UserSettableParameter("slider", "amount healthy", 250, 1, 500),
    "sick_N": UserSettableParameter("slider", "amount sick", 10, 1, 500),
    "work_n": UserSettableParameter("slider", "amount work locations", 20, 1, 50),
    "rec_n": UserSettableParameter("slider", "amount recreation locations", 20, 1, 50)
}

server = ModularServer(BaseModel,
                       [network, Time(), chart],
                       "Infected model",
                       model_params
                       )
server.port = 8521 # The default
server.launch()
