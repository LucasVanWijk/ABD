from mesa.visualization.modules import NetworkModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule, TextElement
from Infect_Model import BaseModel
from mesa.visualization.UserParam import UserSettableParameter


def node_size_based_on_crowd(node):
    init_size = 5
    amount_agenst = len(node[1]["agent"])
    if amount_agenst <= 3:
        return init_size + amount_agenst*2
    elif amount_agenst > 3:
        return init_size + 6 + amount_agenst/2


def run_visual():
    def network_portrayal(G):
        portrayal = dict()
        portrayal["nodes"] = []

        for n in G.nodes.data():
            portrayal["nodes"].append(
                {
                    "size": node_size_based_on_crowd(n),
                    "color": n[1]["color"],
                }
            )

        portrayal["edges"] = []
        for source, target in G.edges:
            portrayal["edges"].append(
                {
                    "source": source,
                    "target": target,
                    "color": "black",
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
                        "Color": "Green"},
                        {"Label": "healthy",
                        "Color": "Red"},
                        {"Label": "recovered",
                        "Color": "Blue"}
                        ],
                        data_collector_name='datacollector')
    model_params = {
        "p_nodes": UserSettableParameter("number", "prob nodes", value=0.04),
        "healthy_N": UserSettableParameter("slider", "amount healthy", 95, 1, 500),
        "sick_N": UserSettableParameter("slider", "amount sick", 5, 1, 500),
        "altruism": UserSettableParameter("slider", "amount sick", 10, 1, 100)
    }

    model_params["network_params"] = [
            (model_params["healthy_N"].value + model_params["sick_N"].value, "House", "Grey"),
            (15, "Work", "yellow"),
            (5, "School", "green"),
            (3, "Shop", "Brown"),
            (3, "Bar", "Brown"),
            (3, "Park", "Brown"),
            (1, "University", "Red")
    ]

    server = ModularServer(BaseModel,
                        [network, Time(), chart],
                        "Infected model",
                        model_params
                        )
    server.port = 8521 # The default
    server.launch()

if __name__ == "__main__":
    run_visual()
