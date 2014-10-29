class AIPlayer(object):
    def __init__(self, id):
        self._name = 'AI #{0}'.format(id)

    @property
    def name(self):
        return self._name