from mesa.batchrunner import BatchRunner
from Infect_Model import BaseModel, compute_infected
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
    iterations=1,
    max_steps=100,
    model_reporters={"infected": compute_infected}
)

batch_run.run_all()

run_data = batch_run.get_model_vars_dataframe()
plt.plot(run_data["sick_N"], run_data["infected"])
plt.show()
