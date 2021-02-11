from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from Infect_Agents import Infect_Agent, Work, Recreation
from Infect_Model import BaseModel
from mesa.visualization.UserParam import UserSettableParameter


def agent_portrayal(agent):
    """ Determins how a agent needs to be portrayed. A agent is passed. 
    Depending on there charasteristics they will be portrayed a certain way.
    
    :param agent: a agent of type agent
    :returns portrayal: a portrayal object"""

    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.5}

    if isinstance(agent, Infect_Agent) and agent.infected:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
    elif isinstance(agent, Infect_Agent) and not agent.infected:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 1
    elif isinstance(agent, Work):
        portrayal["Color"] = "gray"
        portrayal["Layer"] = 0
        portrayal["r"] = 2
    elif isinstance(agent, Recreation):
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 0
        portrayal["r"] = 2

    return portrayal


# grid = CanvasGrid(agent_portrayal, vakjes_x, vakjes_y, aantal_x_pixel, aantal_y_pixel)
grid = CanvasGrid(agent_portrayal, 100, 100, 1000, 1000)
chart = ChartModule([{"Label": "infected",
                      "Color": "Green"}],
                    data_collector_name='datacollector')
model_params = {
    "width":  UserSettableParameter("slider", "width", 100, 1, 500),
    "height":  UserSettableParameter("slider", "height", 100, 1, 500),
    "healthy_N": UserSettableParameter("slider", "amount healthy", 250, 1, 500),
    "sick_N": UserSettableParameter("slider", "amount sick", 10, 1, 500),
    "work_n": UserSettableParameter("slider", "amount work locations", 20, 1, 50),
    "rec_n": UserSettableParameter("slider", "amount recreation locations", 20, 1, 50)
}

server = ModularServer(BaseModel,
                       [grid,chart],
                       "Infected model",
                       model_params
                       )
server.port = 8521 # The default
server.launch()
