from PySide2 import QtWidgets, QtCore
import os
import sys
import scrape_and_convert
import zdic_lookup
import string
import pickle
import flashcards
import datetime

def getAvailableNovels():
    curDir = os.getcwd()
    os.chdir('novels')
    dirs = os.listdir('.')
    os.chdir(curDir)
    return dirs

class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.currentChapter = str()
        self.chapterContent = 'Nothing is here!'
        self.curDir = ['e']
        self.curCard = 0
        self.initUI()

    def initUI(self):

        self.frame = QtWidgets.QFrame()
        self.largeStack = QtWidgets.QStackedLayout()

        self.mainPage = QtWidgets.QWidget()
        self.mainPageLayout = QtWidgets.QVBoxLayout()

        novelSubmit = QtWidgets.QLineEdit()
        novelSubmit.returnPressed.connect(self.novelSubmitted)
        self.mainPageLayout.addWidget(novelSubmit)

        self.novelList = QtWidgets.QListWidget()
        self.novels = getAvailableNovels()
        for index, novel in enumerate(self.novels):
            self.novelList.addItem(novel)
        self.novelList.itemDoubleClicked.connect(self.novelClicked)
        self.mainPageLayout.addWidget(self.novelList)
        flashcardButton = QtWidgets.QPushButton('Review Flashcards')
        flashcardButton.pressed.connect(
            lambda: self.largeStack.setCurrentIndex(3)
        )
        self.mainPageLayout.addWidget(flashcardButton)
        self.mainPage.setLayout(self.mainPageLayout)


        self.largeStack.addWidget(self.mainPage)


        # Novel Navigation

        self.novelNavigation = QtWidgets.QListWidget()
        for chapter in self.curDir:
            self.novelNavigation.addItem(chapter)
        self.novelNavigation.itemDoubleClicked.connect(self.chapterClicked)
        self.largeStack.addWidget(self.novelNavigation)


        self.novelBox = QtWidgets.QTextEdit()
        self.next_chapter_button = QtWidgets.QPushButton('Next Chapter')
        self.next_chapter_button.pressed.connect(self.nextChapter)
        self.toc_button = QtWidgets.QPushButton('Table Of Contents')
        self.toc_button.pressed.connect(
            lambda: self.largeStack.setCurrentIndex(1)
        )
        self.prev_chapter_button = QtWidgets.QPushButton('Previous Chapter')
        self.prev_chapter_button.pressed.connect(self.prevChapter)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.prev_chapter_button)
        self.button_layout.addWidget(self.toc_button)
        self.button_layout.addWidget(self.next_chapter_button)
        self.novelBox.setText(self.chapterContent)
        self.novelLayout = QtWidgets.QVBoxLayout()
        self.novelWidget = QtWidgets.QWidget()
        self.novelLayout.addWidget(self.novelBox)
        self.buttonWidget = QtWidgets.QWidget()
        self.buttonWidget.setLayout(self.button_layout)
        self.novelLayout.addWidget(self.buttonWidget)
        self.novelWidget.setLayout(self.novelLayout)
        self.largeStack.addWidget(self.novelWidget)

        self.flashcardWidget = QtWidgets.QWidget()
        self.flashcardLayout = QtWidgets.QVBoxLayout()
        self.flashFront = QtWidgets.QLabel()
        self.flashBack = QtWidgets.QLabel()
        self.showButton = QtWidgets.QPushButton('Show Card')
        self.showButton.pressed.connect(self.showCard)
        self.goodButton = QtWidgets.QPushButton('Good')
        self.goodButton.pressed.connect(self.goodCard)
        self.badButton = QtWidgets.QPushButton('Bad')
        self.badButton.pressed.connect(self.badCard)
        self.nextButton = QtWidgets.QPushButton('Next')
        self.nextButton.pressed.connect(self.nextCard)
        self.saveButton = QtWidgets.QPushButton('Save')
        self.saveButton.pressed.connect(self.saveCards)
        self.flashcardLayout.addWidget(self.flashFront)
        self.flashcardLayout.addWidget(self.flashBack)
        self.flashcardLayout.addWidget(self.showButton)
        self.flashcardLayout.addWidget(self.goodButton)
        self.flashcardLayout.addWidget(self.badButton)
        self.flashcardLayout.addWidget(self.nextButton)
        self.flashcardLayout.addWidget(self.saveButton)
        self.flashcardWidget.setLayout(self.flashcardLayout)
        self.largeStack.addWidget(self.flashcardWidget)

        # Flashcard Backend
        self.flashcardDict = pickle.load(open('flashcards.pickle', 'rb'))
        flashcards.FlashCard.update()
        self.cardsToReview = [self.flashcardDict[key] for key in self.flashcardDict
                              if self.flashcardDict[key].to_review]



        self.frame.setLayout(self.largeStack)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.frame)
        self.show()

    def saveCards(self):
        for card in self.cardsToReview:
            self.flashcardDict[card.word] = card
        with open('flashcards.pickle', 'wb') as flashcardsfile:
            pickle.dump(self.flashcardDict, flashcardsfile)

    def showCard(self):
        self.flashBack.setText(self.cardsToReview[self.curCard].definition)
        self.flashcardLayout.update()
        self.flashcardWidget.update()
        self.largeStack.update()
        self.repaint()
        print(self.flashFront.text())
        print(self.flashBack.text())
        print(self.curCard)

    def nextCard(self):
        self.curCard += 1
        if self.curCard < len(self.cardsToReview):
            self.flashFront.setText(self.cardsToReview[self.curCard].word)
            self.cardsToReview[self.curCard].to_review = False
        self.flashcardLayout.update()
        print(len(self.cardsToReview))
        self.largeStack.update()
        self.repaint()
        self.flashcardWidget.update()

    def goodCard(self):
        self.cardsToReview[self.curCard].last_interval *= 3
        self.cardsToReview[self.curCard].next_review = datetime.datetime.now()+ \
            datetime.timedelta(days=self.cardsToReview[self.curCard].last_interval)

    def badCard(self):
        self.cardsToReview[self.curCard].last_interval //= 3
        self.cardsToReview[self.curCard].last_interval = max(
            self.cardsToReview[self.curCard].last_interval, 1)
        self.cardsToReview[self.curCard].next_review = datetime.datetime.now()+ \
                                                       datetime.timedelta(days=self.cardsToReview[self.curCard].last_interval)



    def novelClicked(self, novel):
        os.chdir('./novels/' + novel.text())
        self.curDir = os.listdir('.')
        self.curDir.sort(key=lambda x: int(''.join([c for c in x if c in string.digits])))
        self.largeStack.setCurrentIndex(1)
        self.novelNavigation = QtWidgets.QListWidget()
        self.largeStack.removeWidget(self.largeStack.widget(1))
        for chapter in self.curDir:
            self.novelNavigation.addItem(chapter)
        self.novelNavigation.itemDoubleClicked.connect(self.chapterClicked)
        self.largeStack.insertWidget(1, self.novelNavigation)
        self.largeStack.setCurrentIndex(1)
        self.largeStack.update()
        print(self.novelNavigation.count())
        print(type(self.largeStack.widget(1)))
        print(os.getcwd())
        print('reeee')
        print(self.curDir)
        print(os.listdir('.'))
        # self.initUI()


    def novelSubmitted(self):
        sender = self.sender()
        scrape_and_convert.main(sender.text())

    def chapterClicked(self, chapter):
        self.currentChapter = chapter.text()
        self.chapterContent = open(self.currentChapter, 'r').read()
        self.largeStack.setCurrentIndex(2)
        self.updateText()

    def nextChapter(self):
        allChapters = sorted(os.listdir('.'))
        print(self.chapterContent[:20])
        if allChapters[-1] == self.currentChapter:
            pass
        else:
            self.currentChapter = allChapters[allChapters.index(self.currentChapter) + 1]
            self.chapterContent = open(self.currentChapter, 'r').read()
            self.updateText()


    def prevChapter(self):
        allChapters = sorted(os.listdir('.'))
        if allChapters[0] == self.currentChapter:
            pass
        else:
            self.currentChapter = allChapters[allChapters.index(self.currentChapter) - 1]
            self.chapterContent = open(self.currentChapter, 'r').read()
            self.updateText()

    def updateText(self):
        self.novelBox.setText(self.chapterContent)
        self.novelLayout.update()
        self.largeStack.update()

    def keyPressEvent(self, e):
        key = e.key()
        if key == QtCore.Qt.Key_F1:
            self.selected = self.novelBox.textCursor().selectedText()
            self.text = str(zdic_lookup.get_page(self.selected))
            print(self.text)
            ok = QtWidgets.QMessageBox(self)
            # self.addToFlashButton = QtWidgets.QMessageBox.standardButton
            # self.addToFlashButton
            # self.addToFlashButton.pressed.connect(self.addTermToFlashcards)
            ok.setText(self.text)
            # ok.addButton(self.addToFlashButton)
            ok.show()

    def addTermToFlashcards(self):
        self.flashcardDict[self.selected] = flashcards.FlashCard(self.selected, self.text)


def main():
    app = QtWidgets.QApplication([])

    w = Window()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

l

        
        
