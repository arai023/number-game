from PyQt6.QtWidgets import *
from numbergame import *
import random

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        '''
        Sets up UI and initalizes values
        '''
        super().__init__()
        self.setupUi(self)
        self.random_number = random.randint(1,100) #random number
        self.attempt = 10 #sets initial value for number of attempts
        self.round_number = 1 #sets initial value for number of rounds
        self.rounds_won = 0 #sets initial value for number of rounds won
        self.rounds_lost = 0 #sets initial value for number of rounds lost
        self.checkButton.clicked.connect(lambda: self.check()) #ensures that the number is submitted
        self.quitButton.clicked.connect(lambda: self.reset()) #if user clicks this, the game resets
    
    def check(self) -> None:
        '''
        Check the guess and provide hints
        '''
        try:
            guess = int(self.guessNumber.text())

            if guess < 1 or guess > 100: #if the guess is not in the range, it asks the user to input a correct value
                self.instructionLabel.setText("Please guess a number between 1-100.")
                self.instructionLabel.setStyleSheet("color: red;")
                return
            
            self.attempt -= 1 #decreases number of tries each time

            if guess == self.random_number: #if guess is correct, the following things happen
                self.rounds_won += 1 #round increases
                self.instructionLabel.setText(f"You are correct!\n"
                                              f"You guessed in {10 - self.attempt} tries.") #summary of one round
                self.instructionLabel.setStyleSheet("color: green;")
                self.checkButton.setEnabled(False) #prevents the user from clicking the check button
                self.play_again() #if guess is correct, a pop up box opens
                return
            
            #hints for the user to guess the correct number
            if guess < self.random_number:  
                self.instructionLabel.setText("Guess is low. Please try again.")
                self.instructionLabel.setStyleSheet("color: red;")
            else:
                self.instructionLabel.setText("Guess is high. Please try again.")
                self.instructionLabel.setStyleSheet("color: red;")
            
            #if the user runs out of attempts, the game stops and they are told the actual number and asked if they want to play again
            if self.attempt == 0:
                self.rounds_lost += 1
                self.instructionLabel.setText(f"Game over. You have used all tries.\n" 
                                              f"Please try again.")
                self.instructionLabel.setStyleSheet("color: black;")
                self.hints.setText(f"The correct answer was {self.random_number}.")
                self.checkButton.setEnabled(False)
                self.play_again()
            
            self.hints.setText(f"Tries remaining: {self.attempt}") #tells the number of tries remaining

        except ValueError: #checks if the input is a number or not
            self.instructionLabel.setText("Please guess a number between 1-100.")
            self.instructionLabel.setStyleSheet("color: red;")
        
    def play_again(self) -> None:
        '''
        allows the user to play again if they wish to do so
        '''
        #prompts the user to click yes or no
        messageBox = QMessageBox(self)
        messageBox.setWindowTitle("Play again?")
        messageBox.setText(f"Round {self.round_number} complete. Would you like to play another round?")
        messageBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        messageBox.setDefaultButton(QMessageBox.StandardButton.Yes)
        reply = messageBox.exec()
        
        if reply == QMessageBox.StandardButton.Yes: #if user clicks yes, another round begins
            self.round_number += 1
            self.reset()
        else:
            self.guessNumber.clear()
            self.guessNumber.setEnabled(False)
            self.checkButton.setEnabled(False)
            self.quitButton.setEnabled(False)
            self.instructionLabel.setText(f"Thank you for playing.\n "
                                          f"{self.rounds_won} rounds won. {self.rounds_lost} rounds lost.\n"
                                          f"Close to exit.")
            self.instructionLabel.setStyleSheet("color: black;")
            self.hints.setText("")
    
    def reset(self) -> None:
        self.attempt = 10
        self.random_number = random.randint(1,100)
        self.hints.setText(f"Tries remaining: {self.attempt}")
        self.guessNumber.clear()
        self.checkButton.setEnabled(True)
        self.instructionLabel.setText("Please guess a number between 1-100.")
        self.instructionLabel.setStyleSheet("color: black;")