from mesa.batchrunner import BatchRunner
from Infect_Model import BaseModel, compute_infected, compute_healthy, compute_recovered
import matplotlib.pyplot as plt
import pandas as pd


container = pd.DataFrame()
vars_alt = [1,25,50,75,100]
for altrui in vars_alt:
    fixed_params = {
    "altruism": altrui,
    "sick_N": 10,
    "p_nodes": 0.1,
    "healthy_N": 357,
    "network_params": [
        (357, "House", "Grey"),
        (76, "Work", "yellow"),
        (15, "School", "green"),
        (125, "Shop", "Brown"),
        (31, "Bar", "Brown"),
        (5, "Park", "Brown"),
        (1, "University", "Red")
    ]
}

    m = BaseModel(**fixed_params)
    for i in range(1000):
        if i % 100 == 0:
            print(i)
        m.step()


    infected = m.datacollector.get_model_vars_dataframe()["infected"]
    infected = infected.groupby(infected.index // 24).mean()
    container[altrui] = infected



print(container)    
container.plot()
plt.show()
# f = pd.DataFrame()
# f["1t25"] = container[1] - container[25]
# f["25t50"] = container[25] - container[50]
# f["75t100"] = container[75] - container[100]
# f.plot()
# plt.show()
