class GameState(object):
    def __init__(self):
        self.players = []
        self.human_player = None

        self.interrogation_deck = []
        self.discard_deck = []
        self.evidence_cards = []
        self.extra_card = None

        self.turn = 0
        self.current_player = None
        self.question_cards = []

        self.history = []
        self.accusations = []

        self.status = 'playing'