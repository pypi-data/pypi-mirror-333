from typing import Literal
from pydantic import Extra
from pogema_toolbox.algorithm_config import AlgoBase
import numpy as np
from pypibt.pibt import PIBT
from pogema import GridConfig

class PIBTInferenceConfig(AlgoBase, extra=Extra.forbid):
    name: Literal['PIBT'] = 'PIBT'
    parallel_backend: Literal[
        'multiprocessing', 'dask', 'sequential', 'balanced_multiprocessing', 'balanced_dask',
        'balanced_dask_gpu'] = 'balanced_dask'
    device: str = 'cpu'
    num_process: int = 8
    centralized: bool = True
    
class PIBTInference:
    def __init__(self, cfg: PIBTInferenceConfig):
        self.cfg = cfg
        self.agent = None
        self.last_actions = None
        self.positions = None
        self.actions = {tuple(coord): i for i, coord in enumerate(GridConfig().MOVES)}
    
    def get_agents_in_obs(self, agent_idx, agents_pos, obs_radius):
        agents_in_obs = [agent_idx]
        agent_pos = agents_pos[agent_idx]
        for i, pos in enumerate(agents_pos):
            if i != agent_idx and abs(agent_pos[0] - pos[0]) <= obs_radius and abs(agent_pos[1] - pos[1]) <= obs_radius:
                agents_in_obs.append(i)
        return agents_in_obs
    
    def act(self, observations, rewards=None, dones=None, info=None, skip_agents=None):
        num_agents = len(observations)
        global_xy = [obs['global_xy'] for obs in observations]
        global_target_xy = [obs['global_target_xy'] for obs in observations]
        grid = np.array(observations[0]['global_obstacles']).astype(np.bool_)
        actions = []
        if self.cfg.centralized:
            starts = global_xy
            goals = global_target_xy
            pibt = PIBT(grid, starts, goals)
            configs = pibt.run()
            actions = [self.actions[(configs[1][i][0] - configs[0][i][0], 
                                    configs[1][i][1] - configs[0][i][1])] 
                                    for i in range(num_agents)]
        else:
            for i in range(num_agents):
                agents_in_obs = self.get_agents_in_obs(i, global_xy, 5)
                starts = []
                goals = []
                for agent_idx in agents_in_obs:
                    starts.append(global_xy[agent_idx])
                    goals.append(global_target_xy[agent_idx])
                pibt = PIBT(grid, starts, goals)
                configs = pibt.run(max_timestep=1)
                action = self.actions[(configs[1][0][0] - configs[0][0][0], 
                                    configs[1][0][1] - configs[0][0][1])] 
                actions.append(action)
        return actions

    def reset_states(self):
        pass