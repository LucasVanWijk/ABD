from mesa.visualization.modules import NetworkModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from Infect_Model import BaseModel
from mesa.visualization.UserParam import UserSettableParameter


def network_portrayal(G):

    portrayal = dict()
    portrayal["nodes"] = []
    for n in G.nodes.data():
        color = "blue"
        if n[1]["type"] == "work":
            color = "gray"
        elif n[1]["type"] == "recreation":
            color = "orange"

        portrayal["nodes"].append(
            {
                "size": 6,
                "color": color,
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


    # portrayal["nodes"] = [
    #     {
    #         "size": 6,
    #         "color": "blue",
    #     }
    #     for _ in G.nodes
    # ]
    #
    # portrayal["edges"] = [
    #     {
    #         "source": source,
    #         "target": target,
    #         "color": "red",
    #         "width": 1,
    #     }
    #     for (source, target) in G.edges
    # ]


    return portrayal


class Time(TextElement):
    def render(self, model):
        time = model.date
        return str(time)


network = NetworkModule(network_portrayal, 500, 500, library="d3")
chart = ChartModule([{"Label": "infected",
                      "Color": "Green"}],
                    data_collector_name='datacollector')
model_params = {
    "n_nodes": UserSettableParameter("slider", "amount nodes", 20, 1, 30),
    "p_nodes": UserSettableParameter("number", "prob nodes", value=0.5),
    "healthy_N": UserSettableParameter("slider", "amount healthy", 250, 1, 500),
    "sick_N": UserSettableParameter("slider", "amount sick", 10, 1, 500),
    "work_n": UserSettableParameter("slider", "amount work locations", 5, 1, 50),
    "rec_n": UserSettableParameter("slider", "amount recreation locations", 5, 1, 50)
}

server = ModularServer(BaseModel,
                       [network, Time(), chart],
                       "Infected model",
                       model_params
                       )
server.port = 8521 # The default
server.launch()
