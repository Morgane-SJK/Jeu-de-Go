from copy import deepcopy

class GameLogic:
    print("Game Logic Object Created")
    # TODO add code here to manage the logic of your game

    def canWePlay(self, boardArray, mouseToCol, mouseToRow, player, previousStates):
        self.canweplay = False
        print("Can we play")
        pri = 0
        if(boardArray[mouseToCol][mouseToRow] == 0):
            if(self.koRule(boardArray, mouseToCol, mouseToRow, player, previousStates) == False):

                cash, pri = self.surrounded(boardArray, player, mouseToCol, mouseToRow)
                if(cash==True): #cash piece
                    self.canweplay = True #NO SUICIDE RULE APPLLY

                elif(cash==False): #cash piece
                    if(self.suicideRule(boardArray, mouseToCol, mouseToRow, player) == False):
                          self.canweplay = True

        if (self.canweplay == False):
            previousStates.pop()
        print(str(pri))
        print(self.canweplay)
        return self.canweplay, pri #return if we can play or not (True/False) and the number of prisoners


    def suicideRule(self, boardArray, mouseToCol, mouseToRow, player):
        print("SUCIDE RULE")
        self.suicide = True
        boardArray[mouseToCol][mouseToRow] = player #we place the piece of the actual player to be able to make tests
        group = [] #this is the group of the pieces of the same colour as the player
        group.append([mouseToCol, mouseToRow])
        self.lenght = len(group)
        index = 0

        while index != self.lenght:
            group = self.groups(boardArray, group, group[index][0], group[index][1], player)
            index = index + 1

        for i in range(0, len(group)):
            neighb2, pos2 = self.neighbours(boardArray, group[i][0], group[i][1])
            for j in range(0, len(neighb2)):
                if neighb2[j] == 0: #for each piece of the group, we look for a liberty (so for a 0 in the board)
                    self.suicide = False #there is a liberty so this is not suicide
                    break

        boardArray[mouseToCol][mouseToRow] = 0 #we remove the piece of the actual player (if he can play, his piece will be add in the class board)
        return self.suicide


    def groups(self, boardArray, groupBis, position1, position2, player): #we create a group with the neighbours of the piece with the colour of the actual player
        neighb, pos = self.neighbours(boardArray, position1, position2)

        for i in range(0, len(neighb)):
            if (neighb[i] == player):
                bool = True
                for j in range(0, len(groupBis)):
                    if (groupBis[j] == pos[i]):
                        bool = False
                if bool == True:
                    print("Add piece to the group")
                    groupBis.append(pos[i])
                    self.lenght = self.lenght + 1

        return groupBis

    def koRule(self, boardArray, mouseToCol, mouseToRow, player, previousStates):
        self.ko = False  # if we CAN play
        print("KO RULES")
        boardArray[mouseToCol][mouseToRow] = player #we place the piece of the actual player to be able to make tests
        for i in range(0, len(previousStates)):

            if boardArray == previousStates[i]:
                self.ko = True  # if we CAN'T play
                break

        previousStates.append(deepcopy(boardArray))  # Delate the last one if can we play == False
        boardArray[mouseToCol][mouseToRow] = 0 #we remove the piece of the actual player (if he can play, his piece will be add in the class board)
        print(self.ko)
        return self.ko


    def surrounded(self, boardArray, player, mouseToCol, mouseToRow):
        self.cashPieces = True  # if a piece (or more) IS cashed
        self.numberOfPrisoners = 0
        print("CASH")

        boardArray[mouseToCol][mouseToRow] = player #we place the piece of the actual player to be able to make tests

        if(player == 1):
            otherPlayer = 2
        else:
            otherPlayer = 1

        neighb, pos = self.neighbours(boardArray, mouseToCol, mouseToRow)  # group of all the neighbour around the piece
        group1 = []  # group of all the neighbour around the piece WITH the opposit coulour

        for i in range(0, len(neighb)):
            if (neighb[i] == otherPlayer):
                group1.append(pos[i])
        if(len(group1) == 0):
            self.cashPieces = False

        for i in range(0, len(group1)):  # create 1 to 4 neighbours group around the piece WITH the opposit coulour
            group2 = []

            group2.append(group1[i])  # put the 1st neighbours (than the 2nd ext...) of the around the piece WITH the opposit coulour in a group
            index = 0
            groupCashed = True

            while index != len(group2):  # while index != lenght
                group2 = self.groups(boardArray, group2, group2[index][0], group2[index][1], otherPlayer)  # created a groupe link to the neigbourg (of opposite coulour)
                #than add to the group other opposit coulours's piece thar are near. the len of the group have to increse. When each piece of the groupe have their neigbourg check, it can stop.
                index = index + 1

            for j in range(0, len(group2)):  # look if the 1st group have liberty for each member of the group
                neighb2, pos2 = self.neighbours(boardArray, group2[j][0], group2[j][1])

                for k in range(0, len(neighb2)):
                    if neighb2[k] == 0:
                        self.cashPieces = False
                        groupCashed = False
                        break

            if(groupCashed == True):
                for j in range(0, len(group2)):
                    boardArray[group2[j][0]][group2[j][1]] = 0
                self.numberOfPrisoners = self.numberOfPrisoners + len(group2)

        boardArray[mouseToCol][mouseToRow] = 0  #we remove the piece of the actual player (if he can play, his piece will be add in the class board)
        return self.cashPieces, self.numberOfPrisoners


    def neighbours(self, boardArray, i, j):
        self.neighbour = [] #this saves the colours of the neigbours (0, 1 or 2)
        self.position = [] #this saves the positions of the neighbours

        if (i == 0 and j == 0):
            self.neighbour = [boardArray[i][j + 1], boardArray[i + 1][j]] #just 2 neighbours
            self.position.append([i, j+1])
            self.position.append([i + 1, j])
        if (i == 0 and j == 6):
            self.neighbour = [boardArray[i][j - 1], boardArray[i + 1][j]] #just 2 neighbours
            self.position.append([i, j - 1])
            self.position.append([i + 1, j])
        if (i == 6 and j == 0):
            self.neighbour = [boardArray[i - 1][j], boardArray[i][j + 1]] #just 2 neighbours
            self.position.append([i-1, j])
            self.position.append([i, j+1])
        if (i == 6 and j == 6):
            self.neighbour = [boardArray[i - 1][j], boardArray[i][j - 1]] #just 2 neighbours
            self.position.append([i-1, j])
            self.position.append([i, j-1])

        if (i == 0 and j != 0 and j != 6):
            self.neighbour = [boardArray[i][j - 1], boardArray[i][j + 1], boardArray[i + 1][j]] #3 neighbours
            self.position.append([i, j - 1])
            self.position.append([i, j+1])
            self.position.append([i + 1, j])
        if (i == 6 and j != 0 and j != 6):
            self.neighbour = [boardArray[i][j - 1], boardArray[i - 1][j], boardArray[i][j + 1]] #3 neighbours
            self.position.append([i, j - 1])
            self.position.append([i-1, j])
            self.position.append([i, j+1])
        if (j == 0 and i != 0 and i != 6):
            self.neighbour = [boardArray[i - 1][j], boardArray[i][j + 1], boardArray[i + 1][j]] #3 neighbours
            self.position.append([i-1, j])
            self.position.append([i, j + 1])
            self.position.append([i + 1, j])
        if (j == 6 and i != 0 and i != 6):
            self.neighbour = [boardArray[i - 1][j], boardArray[i][j - 1], boardArray[i + 1][j]] #3 neighbours
            self.position.append([i-1, j] )
            self.position.append([i, j - 1])
            self.position.append([i + 1, j])

        if (i != 0 and i != 6 and j != 0 and j != 6): #4 neighbours

            self.neighbour = [boardArray[i][j - 1], boardArray[i][j + 1], boardArray[i - 1][j],
                              boardArray[i + 1][j]]
            self.position.append([i, j - 1])
            self.position.append([i, j + 1])
            self.position.append([i - 1, j])
            self.position.append([i + 1, j])

        return self.neighbour, self.position #we return the type of neighbours with their positions




