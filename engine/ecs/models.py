
class Entity(object):
    """ Entity Object wraps UUID for collecting Components """

    __slots__ = ('_uuid',)

    def __init__(self, uuid):
        self._uuid = uuid

    def __hash__(self):
        return self._uuid

    def __eq__(self, other):
        return self._uuid == hash(other)

    def __repr__(self):
        return '{0}({1})'.format(type(self).__name__, self._uuid)

class Component(object):
    """ Component Base Class """
    pass


class System():
    """ An object that represents an operation in the engine, it will operate
        over components from the entities in the Entity Manger
    """
    
    def __init__(self):
        self.entity_manager = None
        """ This is the Systems Entity Manager.
            It is set when each System is added to the Entity Manager.
            A System may only be allowed to belong to one Entity Manager for
            performance.
        """

        self.system_manager = None
        """ This is the Systems System Manager.
            It is set when each System is added to the System Manager
            Can only be assigned to one for reasons above.
        """
        self.priority = None
        """ Determines the priority of this System, or the order in which
            Systems are run.
        """

    def update(self, dt, keys):
        pass

    def draw(self, dt):
        pass