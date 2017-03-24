from engine.ecs.models import Entity

class EnitityManager(object):
    """Provide database-like access to components based on an entity key."""

    def __init__(self):
        self._database = {}
        self._next_guid = 0

    @property
    def database(self):
        return self._database

    def create_entity(self):
        entity = Entity(self._next_guid)
        self._next_guid += 1
        return entity

    def add_component(self, entity, component_instance):
        
        component_type = type(component_instance)
        if component_type not in self._database:
            self._database[component_type] = {}

        self._database[component_type][entity] = component_instance

    def remove_component(self, entity, component_type):
        try:
            del self._database[component_type][entity]
            if self._database[component_type] == {}:
                del self._database[component_type]

        except KeyError:
            pass

    def pairs_for_type(self, component_type):
        # TODO(jhives): This should return an iterator of tuples of type
        #                (entity, component_instance) for the given component_type    
        pass

    def component_for_entity(self, entity, component_type):
        try:
            return self._database[component_type][entity]
        except KeyError:
            raise NonexistentComponentTypeForEntity(
                entity, component_type)                

    def remove_entity(self, entity):
        for comp_type in list(self._database.keys()):
            try:
                del self._database[comp_type][entity]
                if self._database[comp_type] == {}:
                    del self._database[comp_type]
            except KeyError:
                pass


class SystemManager(object):

    def __init__(self, entity_manager):
        self._systems = []
        self._system_types = {}
        self._entity_manager = entity_manager

    @property
    def systems(self):
        return self._systems

    def add_system(self, system_instance, priority=0):

        system_type = type(system_instance)

        if system_type in self._system_types:
            raise DuplicateSystemTypeError(system_type)
        if system_instance.system_manager is not None:
            raise SystemAlreadyAddedToManagerError(system_instance, self, 
                system_instance.system_manager)
    
        system_instance.entity_manager = self._entity_manager
        system_instance.system_manager = self
        self._system_types[system_type] = system_instance
        self._systems.append(system_instance)

    def remove_system(self, system_type):
        system = self._system_types[system_type]

        system.entity_manager = None
        system.system_manager = None
        self._systems.remove(system)
        del self._system_types[system_type]

    def update(self, dt):
        for system in self._systems:
            system.update(dt)