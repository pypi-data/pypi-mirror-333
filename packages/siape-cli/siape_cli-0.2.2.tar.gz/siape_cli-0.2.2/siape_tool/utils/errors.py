class NotAdmissibleCombination(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
        
class NotAdmissibleYearRange(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)