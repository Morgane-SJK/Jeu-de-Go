from PyQt5.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, QMessageBox, QPushButton
#TODO import additional Widget classes as desired
from PyQt5.QtCore import pyqtSlot

class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.center()
        self.setWindowTitle('ScoreBoard')
        #create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        #create seven labels which will be updated by signals
        self.label_whoseTurn = QLabel("Turn of player: BLACK")
        self.label_numberOfBlackPrisoners = QLabel("Number of Black prisoners = 0")
        self.label_numberOfWhitePrisoners = QLabel("Number of White prisoners = 0")
        self.label_blackTerritory = QLabel("Black territory = 0%")
        self.label_whiteTerritory = QLabel("White territory = 0%")

        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time remaining: ")

        #create three buttons
        self.rulesButton = QPushButton('Rules', self)
        self.passTurnButton = QPushButton('Pass Turn', self)
        self.resetGameButton = QPushButton('Reset Game', self)

        self.mainWidget.setLayout(self.mainLayout)

        #we add the labels and the buttons to our main layout
        self.mainLayout.addWidget(self.label_whoseTurn)
        self.mainLayout.addWidget(self.label_numberOfBlackPrisoners)
        self.mainLayout.addWidget(self.label_numberOfWhitePrisoners)
        self.mainLayout.addWidget(self.label_blackTerritory)
        self.mainLayout.addWidget(self.label_whiteTerritory)

        self.mainLayout.addWidget(self.passTurnButton)

        self.mainLayout.addWidget(self.label_timeRemaining)

        self.mainLayout.addWidget(self.resetGameButton)
        self.mainLayout.addWidget(self.rulesButton)


        self.rulesButton.clicked.connect(self.rules)
        self.mainLayout.addWidget(self.label_clickLocation)

        self.setWidget(self.mainWidget)
        self.show()

    def center(self):
        '''centers the window on the screen, you do not need to implement this method'''

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)

        board.changeTurnSignal.connect(self.setPlayerTurn)
        board.changeNumberOfBlackPrisonersSignal.connect(self.setNumberOfBlackPrisoners)
        board.changeNumberOfWhitePrisonersSignal.connect(self.setNumberOfWhitePrisoners)
        board.changeBlackTerritorySignal.connect(self.setBlackTerritory)
        board.changeWhiteTerritorySignal.connect(self.setWhiteTerritory)
        self.passTurnButton.clicked.connect(board.buttonPassed)
        self.resetGameButton.clicked.connect(board.resetGame)

    def setPlayerTurn(self, player):
        update = ""
        if player == 1:
            update = "Turn of player: WHITE"
        if player == 2:
            update = "Turn of player: BLACK"
        self.label_whoseTurn.setText(update)
        print('slot' + update)

    @pyqtSlot(str)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location:" + clickLoc)
        print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemainng):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining:" + str(timeRemainng)
        self.label_timeRemaining.setText(update)
        print('slot '+update)
        # self.redraw()

    def rules(self):
        rulesMessage = QMessageBox()
        rulesMessage.setIcon(QMessageBox.Information)
        rulesMessage.setText("The BLACK always begin. \n"
                            "The purpose of the game is to occupy the largest territorry of the board. For that, you need to cash piece."
                            "To cash the piece: private the liberty of a oppenment piece or a groupe of opponement pieces.")

        #rulesMessage.setInformativeText("This is additional information")
        rulesMessage.setWindowTitle("RULES - THE GO GAME ")
        #rulesMessage.setDetailedText("The details are as follows:")
        rulesMessage.exec_()


    @pyqtSlot(int)
    def setNumberOfBlackPrisoners(self, blackPrisoners):
        update = "Number of Black prisoners = " + str(blackPrisoners)
        self.label_numberOfBlackPrisoners.setText(update)
        print('slot' + update)

    @pyqtSlot(int)
    def setNumberOfWhitePrisoners(self, whitePrisoners):
        update = "Number of White prisoners = " + str(whitePrisoners)
        self.label_numberOfWhitePrisoners.setText(update)
        print('slot' + update)

    @pyqtSlot(int)
    def setBlackTerritory(self, blackTerritory):
        update = "Black Territory = " + str(blackTerritory) + " %"
        self.label_blackTerritory.setText(update)
        print('slot' + update)

    @pyqtSlot(int)
    def setWhiteTerritory(self, whiteTerritory):
        update = "White Territory = " + str(whiteTerritory) + " %"
        self.label_whiteTerritory.setText(update)
        print('slot' + update)


