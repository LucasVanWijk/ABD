from mesa.batchrunner import BatchRunner
from Infect_Model import BaseModel, compute_infected, compute_healthy, compute_recovered
import matplotlib.pyplot as plt

fixed_params = {
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

# variable_params = {"sick_N": [10, 20, 30, 40 , 50]}

# batch_run = BatchRunner(
#     BaseModel,
#     variable_params,
#     fixed_params,
#     iterations=1,
#     max_steps=100,
#     model_reporters={"healthy": compute_healthy,
#                     "infected": compute_infected,
#                     "recovered": compute_recovered}
# )

# # #batch_run.run_all()

# # run_data = batch_run.get_model_vars_dataframe()
# # print(run_data)
# # plt.plot(run_data["infected"])
# # plt.plot(run_data["healthy"])
# # #plt.plot(run_data["recovered"])
# # plt.show()


m = BaseModel(**fixed_params)
for i in range(1000):
    if i % 100 == 0:
        print(i)
    m.step()


gini = m.datacollector.get_model_vars_dataframe()
wow = gini["infected"]
print(wow)
wow = wow.groupby(wow.index // 24).mean()
plt.plot(wow)
plt.show()
