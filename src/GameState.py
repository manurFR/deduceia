class GameState(object):
    def __init__(self):
        self.players = []
        self.human_player = None

        self.interrogation_deck = []
        self.discard_deck = []
        self.evidence_cards = []
        self.extra_card = None

        self.question_cards = []