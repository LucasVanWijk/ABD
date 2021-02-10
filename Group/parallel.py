"""
Mesa Time Module
================
Objects for handling the time component of a model. In particular, this module
contains Schedulers, which handle agent activation. A Scheduler is an object
which controls when agents are called upon to act, and when.
The activation order can have a serious impact on model behavior, so it's
important to specify it explicitly. Example simple activation regimes include
activating all agents in the same order every step, shuffling the activation
order every time, activating each agent *on average* once per step, and more.
Key concepts:
    Step: Many models advance in 'steps'. A step may involve the activation of
    all agents, or a random (or selected) subset of them. Each agent in turn
    may have their own step() method.
    Time: Some models may simulate a continuous 'clock' instead of discrete
    steps. However, by default, the Time is equal to the number of steps the
    model has taken.
"""

from collections import OrderedDict

# mypy
from typing import Dict, Iterator, List, Optional, Union
from mesa.agent import Agent
from mesa.model import Model
from multiprocessing.dummy import Pool

# BaseScheduler has a self.time of int, while
# StagedActivation has a self.time of float
TimeT = Union[float, int]


class BaseScheduler:
    """Simplest scheduler; activates agents one at a time, in the order
    they were added.
    Assumes that each agent added has a *step* method which takes no arguments.
    (This is explicitly meant to replicate the scheduler in MASON).
    """

    def __init__(self, model: Model) -> None:
        """ Create a new, empty BaseScheduler. """
        self.model = model
        self.steps = 0
        self.time: TimeT = 0
        self._agents: Dict[int, Agent] = OrderedDict()

    def add(self, agent: Agent) -> None:
        """Add an Agent object to the schedule.
        Args:
            agent: An Agent to be added to the schedule. NOTE: The agent must
            have a step() method.
        """

        if agent.unique_id in self._agents:
            raise Exception(
                "Agent with unique id {0} already added to scheduler".format(
                    repr(agent.unique_id)
                )
            )

        self._agents[agent.unique_id] = agent

    def remove(self, agent: Agent) -> None:
        """Remove all instances of a given agent from the schedule.
        Args:
            agent: An agent object.
        """
        del self._agents[agent.unique_id]

    def step(self) -> None:
        """ Execute the step of all the agents, one at a time. """
        for agent in self.agent_buffer(shuffled=False):
            agent.step()
        self.steps += 1
        self.time += 1

    def get_agent_count(self) -> int:
        """ Returns the current number of agents in the queue. """
        return len(self._agents.keys())

    @property
    def agents(self) -> List[Agent]:
        return list(self._agents.values())

    def agent_buffer(self, shuffled: bool = False) -> Iterator[Agent]:
        """Simple generator that yields the agents while letting the user
        remove and/or add agents during stepping.
        """
        agent_keys = list(self._agents.keys())
        if shuffled:
            self.model.random.shuffle(agent_keys)

        for key in agent_keys:
            if key in self._agents:
                yield self._agents[key]

class SimultaneousActivation(BaseScheduler):
    """A scheduler to simulate the simultaneous activation of all the agents.
    This scheduler requires that each agent have two methods: step and advance.
    step() activates the agent and stages any necessary changes, but does not
    apply them yet. advance() then applies the changes.
    """

    def step(self) -> None:
        """
        Step all agents, then advance them. 
        """
        
        agent_keys = list(self._agents.keys())

        # https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
        batch_size = len(agent_keys) // self.model.parallel_amount  
        agent_batch_keys = [agent_keys[i:i + batch_size] for i in range(0, len(agent_keys), batch_size)]

        def f(agent_keys):
            for key in agent_keys:
                self._agents[key].step()
            
        p = Pool(batch_size)
        p.map(f,agent_batch_keys)
        p.close()

        for agent_key in agent_keys:
            self._agents[agent_key].advance()

        self.steps += 1
        self.time += 1
