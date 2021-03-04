from mesa.batchrunner import BatchRunner
from Infect_Model import BaseModel, compute_infected

fixed_params = {
    "p_nodes": 0.04,
    "healthy_N": 100,
    "sick_N": 10,
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

variable_params = None

batchrun = BatchRunner(
    BaseModel,
    variable_params,
    fixed_params,
    iterations=1,
    max_steps=100,
    model_reporters={"infected": compute_infected}
)

batchrun.run_all()
