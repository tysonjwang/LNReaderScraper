class FlashCard:
    allCards = []
    def __init__(self, word, definition):
        self.word = word
        self.definition = definition
        self.score = 0
        FlashCard.allCards.append(self)

    def review(self):
        print(self.word)
        result = input('Do you know this word?')
        if result not in ('True', 'False'):
            print('Thats not valid. Type True or False')
        elif result == 'True':
            print('congratulations!')
            self.score += 1
        else:
            print('Oops, please review again!')

    @classmethod
    def review_all(cls):
        for card in cls.allCards:
            card.review()

a = FlashCard('frog', 'animal')
b = FlashCard('bananna', 'fruit')
c = FlashCard('toyota', 'car')
FlashCard.review_all()


    