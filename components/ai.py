from __future__ import annotations

from typing import List, Tuple

import numpy as np  # type: ignore
import tcod

from actions import Action
from components.base_component import BaseComponent

class BaseAI(Action, BaseComponent):
    def perform(self) -> None:
        raise NotImplementedError()
    
    def get_path_to(self, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        """Compute and return a path to the target position.
        
        if there is no valid path then returns and empty list."""
        # copy the walkable array
        cost = np.array(self.entity.gamemap.tiles["walkable"], dtype=np.int8)

        for entity in self.entity.gamemap.entities:
            #check that an entity blocks movement and the cost isnt zero(blocking.)
            if entity.blocks_movement and cost[entity.x, entity.y]:
                #add to the cost of a blocked position
                # a lower number means more enemies will crow behind each oher in hallways
                # a higher number means enimies will take longer paths in order to surround the player
                cost[entity.x, entity.y] += 10
        
        #create a graph from the cost array and pass that graph to the new pathfinder 
        graph = tcod.path.SimpleGraph(cost=cost, cadinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity.x, self.entity.y)) #start position

        #compute the path to the destination and remove the starting point
        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        #convert from List[List[int]] to List[Tuple[int, int]].
        return [(index[0], index[1]) for index in path]
    