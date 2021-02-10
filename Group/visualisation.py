from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from Infect_Agents import Infect_Agent
from Infect_Model import BaseModel

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}

    if agent.infected:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
        
    return portrayal

# grid = CanvasGrid(agent_portrayal, vakjes_x, vakjes_y, aantal_x_pixel, aantal_y_pixel)
grid = CanvasGrid(agent_portrayal, 100, 100, 1000, 1000)
chart = ChartModule([{"Label": "infected",
                      "Color": "Green"}],
                    data_collector_name='datacollector')


server = ModularServer(BaseModel,
                       [grid,chart],
                       "Infected model",
                    #    {"N":250,"width":100, "height":100})
                       {"healthy_N":250,"sick_N":10, "width":100, "height":100})
server.port = 8521 # The default
server.launch()

