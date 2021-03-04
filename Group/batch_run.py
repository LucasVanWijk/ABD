from mesa.batchrunner import BatchRunner
from Infect_Model import BaseModel, compute_infected, compute_healthy, compute_recovered
import matplotlib.pyplot as plt

fixed_params = {
    "p_nodes": 0.04,
    "healthy_N": 100,
    "network_params": [
        (110, "House", "Grey"),
        (25, "Work", "yellow"),
        (10, "School", "green"),
        (5, "Shop", "Brown"),
        (5, "Bar", "Brown"),
        (5, "Park", "Brown"),
        (2, "University", "Red")
    ]
}

variable_params = {"sick_N": [10, 20, 30, 40 , 50]}

batch_run = BatchRunner(
    BaseModel,
    variable_params,
    fixed_params,
    iterations=10,
    max_steps=100,
    model_reporters={"healthy": compute_healthy,
                    "infected": compute_infected,
                    "recovered": compute_recovered}
)

batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
plt.plot(run_data["infected"])
plt.plot(run_data["healthy"])
#plt.plot(run_data["recovered"])
plt.show()
