
from engine.ecs import System
from data.components import AI


class AISystem(System):

	def update(self, game):
		for e, ai in self.entity_manager.pairs_for_type(AI):
			ai.tree.blackboard.store('em', self.entity_manager)
			ai.tree.update(game, e)