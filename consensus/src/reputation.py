
class Reputation:
    def __init__(self):
        self.positives = 0
        self.negatives = 0
    
    def update(self, correct: bool):
        if correct:
            self.positives += 1
        else:
            self.negatives += 1
    
    def get_beta(self) -> float:
        return (self.positives - self.negatives) / (self.positives + self.negatives + 2)

