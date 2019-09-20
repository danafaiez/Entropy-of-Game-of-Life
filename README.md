**About this repository**

This is a project with a gole of understanding the role of (different) entropy fluctuations in the emergence of organized patterns in Conway's Game of Life.  
Credit to Adrian Chifor for [game_of_life.py](https://github.com/adrianchifor/conway-game-of-life/blob/master/game_of_life.py)code that I've used here.

* [entropy_game_of_life.py](https://github.com/danafaiez/Game-of-Life/blob/master/entropy_game_of_life.py): 
This code computes Boltzmann entropy with different macrostates: 
1. population: this macrostate is based on the number of live cells in every dxd box.  
2. Edges: this macrostate is based on the number of edges in every dxd box; i.e. the edge between any live cell and dead cell. 
This quantifies the "interestig" patterns that emerge in GOL, within a given resolution of size dxd.

* [d4_Ehalf.py](https://github.com/danafaiez/Game-of-Life/blob/master/d4_Ehalf.py):
This code includes the volume matrix that corresponds to a box of size 4x4. The entries of this matrix are the volume
(size of the microstate corresponding to a given macrostate (population and edge)). The sum of the volumes in a given coloum
result in the volume for population macrostate, and the sum of the volumes in a given row result in the volume for edge macrostate.

