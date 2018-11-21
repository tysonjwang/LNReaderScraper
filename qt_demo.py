def next_chapter():
    global tex_docs
    global chapter_number
    global text
    global text_display
    print('next')
    if chapter_number < len(tex_docs) - 1:
        chapter_number += 1
        with open(tex_docs[chapter_number], 'r') as doc:
            text = doc.read()
            text_display.clear()
            text_display.insertPlainText(text)



def home():
    os.chdir('./novels')
    home_layout = QVBoxLayout()
    for novel in os.listdir('.'):
        novelButton = QPushButton(novel)
        novelButton.clicked.connect(lambda x: print(novel))
        home_layout.addWidget(novelButton)
    homeW = QWidget()
    homeW.setLayout(home_layout)
    homeW.show()


    #home_layout.addWidget(menuBar)


def prev_chapter():
    global tex_docs
    global chapter_number
    global text
    global text_display
    print('prev')
    if chapter_number != 0:
        chapter_number -= 1
        with open(tex_docs[chapter_number], 'r') as doc:
            text = doc.read()
            text_display.clear()
            text_display.insertPlainText(text)

if __name__ == '__main__':
    from PySide2.QtWidgets import *
    import os
    app = QApplication([])
    # home()

    text_display = QTextBrowser()
    next_chapter_button = QPushButton('Next Chapter')
    next_chapter_button.setStyleSheet('background-color: red')
    toc_button = QPushButton('Table Of Contents')
    prev_chapter_button = QPushButton('Previous Chapter')
    button_layout = QHBoxLayout()
    button_layout.addWidget(prev_chapter_button)
    button_layout.addWidget(toc_button)
    button_layout.addWidget(next_chapter_button)
    main_layout = QVBoxLayout()
    main_layout.addWidget(text_display)
    main_layout.addLayout(button_layout)
    text = str()
    # Here comes a jank implementation of navigating pre-loaded chapters
    tex_docs = sorted(list(filter(lambda x: x[-4:] == '.txt', os.listdir('.'))))
    chapter_number = 0
    next_chapter_button.clicked.connect(next_chapter)
    prev_chapter_button.clicked.connect(prev_chapter)
    text_display.insertPlainText(text)
    text_display.setReadOnly(True)
    window = QWidget()
    window.setLayout(main_layout)
    window.show()

    app.exec_()

