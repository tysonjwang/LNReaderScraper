import datetime
import pickle

class FlashCard:
    allCards = []
    cards_to_review = []
    cardAssociation = {}
    def __init__(self, word, definition):
        self.word = word
        self.definition = definition
        self.next_review = datetime.datetime.now() + datetime.timedelta(days=3)
        self.last_interval = 3
        self.to_review = False
        self.score = 0
        FlashCard.allCards.append(self)
        FlashCard.cardAssociation[word] = self

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

    @classmethod
    def review_due(cls):
        for card in cls.cards_to_review:
            card.review()

    @classmethod
    def update(cls):
        for card in FlashCard.allCards:
            if card.next_review < datetime.datetime.now():
                FlashCard.cards_to_review.append(card)
                card.to_review = True

if __name__ == '__main__':
    a = FlashCard('frog', 'animal')
    b = FlashCard('bananna', 'fruit')
    c = FlashCard('toyota', 'car')

    with open('flashcards.pickle', 'wb') as flashcard_file:
        pickle.dump(FlashCard.cardAssociation, flashcard_file)


    