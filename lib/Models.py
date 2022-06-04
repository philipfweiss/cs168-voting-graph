class RollCall:
    def __init__(self, identifier, topics):
        self.identifier = identifier ## (Congress, Role Number)
        self.topics = topics
        self.votes = {
            "yes": [],
            "no": [],
            "abstain": []
        }
