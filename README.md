# Ludo Game
*Author: Martin Klokočík*

This is one of my first larger projects. So it may contain a lot of mistakes and not efficient solution. This project has a certain code structure which is outlined below.

**If the project does not run, it may be necessary to install the interpreter - Pillow on your computer.**

## Game Rules:
* The number of consecutive rolls of the dice is infinite.
* The game ends when one player first gets all 4 pieces to the finish line.
* The game can be played by at least 2 players.

## Code Structure:
The game is created in 3 classes: `Menu`, `Clovece` and `EndScreen`.

* `Menu`: This class is used to obtain information such as the number of players (sliding on a scale) and subsequently the names of the players. The names of the players are automatically filled in the Entry field according to the names that were in the previous game. They are retrieved from a text file. The game must be finished to have the names filled in. If a player decides to enter fewer players, a window will pop up and alert them, and possibly shut down the program.

* `Clovece`: This class is the entire game. The board is drawn in tkinter. Each field has its unique coordinates stored in dictionaries. The dice roll is created with an animation of jumping images - at the beginning they are flipped very quickly, and later slower and slower, I tried to create the effect of throwing a real dice. The game ends when a player has all 4 pieces at the finish line.

* `EndScreen`: This class contains the winner, the previous 5 games, and the most dominant color for the entire time.

At the end of the game, the names of the players, the winner, the winning color, and the number of pieces killed are written to the text file `"./data/previous_games.txt"`. Similarly, the winning color is written to the text file `"./data/the_most_wins.txt"` to create statistics on which color wins the most. All of this is subsequently displayed in the `EndScreen` class, which automatically starts after the end of the game.

## Game Assistance:
If you'd like to play the game faster to reach the EndScreen and the winner and try all the features, You can modify the code so that the players are not in the house, so the game can be played faster, and so on. If you have any questions, I am happy to answer them (mklokocik@gmail.com). I have spent a considerable amount of time on this project so I hope you appreciate it.
