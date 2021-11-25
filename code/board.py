from PyQt5.QtWidgets import QFrame, QMessageBox, QMainWindow
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint, QRect
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from piece import Piece
from game_logic import GameLogic

class Board(QFrame):  # base the board on a QFrame widget

    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location
    changeTurnSignal = pyqtSignal(int)  # signal sent when the turn is updated
    changeNumberOfBlackPrisonersSignal = pyqtSignal(int)  # signal sent when the number of black prisoner is updated
    changeNumberOfWhitePrisonersSignal = pyqtSignal(int)  # signal sent when the number of white prisoner is updated
    changeBlackTerritorySignal = pyqtSignal(int)  # signal sent when the number of black territory is updated
    changeWhiteTerritorySignal = pyqtSignal(int)  # signal sent when the number of white territory is updated

    # TODO set the board width and height to be square
    boardWidth = 8   # board is 9 squares wide
    boardHeight = 8     # board is 9 squares height
    timerSpeed = 1000     # the timer updates ever 1 second
    counter = 30    # the number the counter will count down from 30 for each player's turn

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''

        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False      # game is not currently started
        self.start()                # start the game which will start the timer

        self.gameLogic = GameLogic()

        #Board initiation
        self.boardArray = []  # TODO - create a 2d int/Piece array to store the state of the game
        for i in range(7):
            self.boardArray.append([0] * 7) #we fill the board with 0 everywhere because at the beginning of the game it is empty

        #Initiation
        self.previousStates = []
        self.playerBlackTurn = True
        self.player = 2 #The player Black begins

        self.blackPrisoners = 0 #no black prisoner at the beginning of the game
        self.whitePrisoners = 0 #no white prisoner at the beginning of the game
        self.blackTerritory = 0 #no black pieces on the board at the beginning of the game
        self.whiteTerritory = 0 #no white pieces on the board at the beginning of the game

        self.numberOfWhitePass = 0 #the white player didn't use the Pass Turn button yet
        self.numberOfBlackPass = 0 #the black player didn't use the Pass Turn button yet
        self.index = 0

        self.printBoardArray()
        self.paintEvent(self.event)

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''
        self.mouseToRow = int((event.x() - (self.squareWidth()/2)) / self.squareWidth())
        self.mouseToCol = int((event.y() - (self.squareHeight()/2)) / self.squareHeight())
        print(self.mouseToRow)
        print(self.mouseToCol)
        self.mousePosToBoard()


    def mousePosToBoard(self): #convert the mouse click of the user in the placement of a piece on the board or the announce of the winner

        if (self.numberOfWhitePass == 2 or self.numberOfBlackPass == 2): #TEST the winning: if a same player passed his turn 2 times, then it's the end
            endMessage = QMessageBox() #a window appear to announce the winner
            endMessage.setIcon(QMessageBox.Information)
            endMessage.setWindowTitle("END")
            if (self.blackPrisoners > self.whitePrisoners):
                endMessage.setText("This is the end ! \n The player White is the winner")
            elif (self.blackPrisoners < self.whitePrisoners):
                endMessage.setText("This is the end ! \n The player Black is the winner")

            else:  # same number of prisoners
                if (self.blackTerritory < self.whiteTerritory):
                    endMessage.setText("This is the end ! \n The player White is the winner")
                elif (self.blackTerritory > self.whiteTerritory):
                    endMessage.setText("This is the end ! \n The player Black is the winner")
                else:  # same territory
                    if (self.numberOfWhitePass == 2):
                        endMessage.setText("This is the end ! \n The player White is the winner")
                    else:
                        endMessage.setText("This is the end ! \n The player Black is the winner")
            endMessage.exec_()
            QMainWindow.exec_()

        else: #PLAY
            canWePlay, pri = self.gameLogic.canWePlay(self.boardArray, self.mouseToCol, self.mouseToRow, self.player, self.previousStates)

            if (self.playerBlackTurn and canWePlay == True): #the black player can play
                self.boardArray[self.mouseToCol][self.mouseToRow] = 2
                self.playerBlackTurn = False #this will be the turn of the White player
                self.player = 1

                self.counter = 30
                #change the displays on the scoreboard
                self.changeTurnSignal.emit(self.player)
                self.whitePrisoners = self.whitePrisoners + pri
                self.changeNumberOfWhitePrisonersSignal.emit(self.whitePrisoners)
                self.territory()
                self.changeBlackTerritorySignal.emit(self.blackTerritory)
                self.changeWhiteTerritorySignal.emit(self.whiteTerritory)

                self.printBoardArray()


            elif (self.playerBlackTurn == False and canWePlay == True): #the white player can play
                self.boardArray[self.mouseToCol][self.mouseToRow] = 1
                self.playerBlackTurn = True #this will be the turn of the black player
                self.player = 2

                self.counter = 30
                #change the displays on the scoreboard
                self.changeTurnSignal.emit(self.player)
                self.blackPrisoners = self.blackPrisoners + pri
                self.changeNumberOfBlackPrisonersSignal.emit(self.blackPrisoners)
                self.territory()
                self.changeBlackTerritorySignal.emit(self.blackTerritory)
                self.changeWhiteTerritorySignal.emit(self.whiteTerritory)

                self.printBoardArray()

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        #self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed, self)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapter this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                print("Game over")
            self.counter -= 1
            print('timerEvent()', self.counter)
            self.updateTimerSignal.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)      # if we do not handle an event we should pass it to the super
                                                        # class for handelingother wise pass it to the super class for handling

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "["+str(event.x())+","+str(event.y())+"]"     # the location where a mouse click was registered
        print("mousePressEvent() - "+clickLoc)
        # TODO you could call some game logic here
        self.clickLocationSignal.emit(clickLoc)
        self.mousePosToColRow(event)
        self.update()

    def resetGame(self): #if a player clicks on the button "Reset Game", this function is called
        '''clears pieces from the board'''
        # TODO write code to reset game
        print("RESET GAME")
        #reset the board
        for i in range(7):
            for j in range(7):
                self.boardArray[i][j] = 0
        self.previousStates = []
        #reset scoreboard
        self.counter = 30
        self.changeTurnSignal.emit(2)
        self.changeNumberOfBlackPrisonersSignal.emit(0)
        self.changeNumberOfWhitePrisonersSignal.emit(0)
        self.changeBlackTerritorySignal.emit(0)
        self.changeWhiteTerritorySignal.emit(0)

        self.update()

    def tryMove(self, newX, newY):
        '''tries to move a piece'''

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # TODO set the default colour of the brush
        painter.setPen(QPen(QColor(0, 0, 0)))
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                self.rectangle = QRect(0, 0, self.squareWidth(), self.squareHeight())

                colTransformation = self.squareWidth() * col  # TODO set this value equal the transformation in the column direction
                rowTransformation = self.squareHeight() * row  # TODO set this value equal the transformation in the row direction
                painter.translate(colTransformation, rowTransformation)

                painter.fillRect(self.rectangle, QColor(220, 200, 140))  # Color of the board  # TODO provide the required arguments
                painter.drawRect(self.rectangle)
                painter.restore()
                # TODO change the colour of the brush so that a checkered board is drawn

    def drawPieces(self, painter):
        '''draw the prices on the board'''
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray)):
                painter.save()
                colTransformation = self.squareWidth() * col  # TODO set this value equal the transformation in the column direction
                rowTransformation = self.squareHeight() * row  # TODO set this value equal the transformation in the row direction
                painter.translate(colTransformation, rowTransformation)

                radius = (self.squareWidth() - 2) / 2
                center = QPoint(100, 100)  #position of the first ellipse

                if self.boardArray[row][col] == 1: #we draw a white piece
                    colour = Qt.white
                    painter.setBrush(QBrush(colour))
                    painter.drawEllipse(center, radius, radius)

                if self.boardArray[row][col] == 2: #we draw a black piece
                    colour = Qt.black
                    painter.setBrush(QBrush(colour))
                    painter.drawEllipse(center, radius, radius)

                if self.boardArray[row][col] == 0: #we draw a transparent piece
                    colour = Qt.transparent
                    painter.setBrush(QBrush(colour))
                    painter.drawEllipse(center, radius, radius)

                painter.restore()

    def territory(self):
        numberOfBlack = 0
        numberOfWhite = 0

        for i in range(0, 6):
            for j in range(0, 6):
                if self.boardArray[i][j] == 2:
                    numberOfBlack = numberOfBlack + 1 #we count the number of black piece on the board
        for i in range(0, 6):
            for j in range(0, 6):
                if self.boardArray[i][j] == 1:
                    numberOfWhite = numberOfWhite + 1 #we count the number of white pieces on the board
        self.blackTerritory = (int)((numberOfBlack / 49) * (100)) #we calculate the percentage of territory occupied by black pieces
        self.whiteTerritory = (int)((numberOfWhite / 49) * (100)) #we calculate the percentage of territory occupied by white pieces


    def buttonPassed(self): #if a player clicks on the button "Pass Turn", this function is called
        if (self.player == 1):
            self.player = 2
            self.playerBlackTurn = True #we change the player
            self.changeTurnSignal.emit(self.player)
            self.numberOfWhitePass = self.numberOfWhitePass + 1 #we increase the number of pass of the white player

        elif (self.player == 2):
            self.player = 1
            self.playerBlackTurn = False #we change the player
            self.changeTurnSignal.emit(self.player)
            self.numberOfBlackPass = self.numberOfBlackPass + 1 #we increase the number of pass of the black player