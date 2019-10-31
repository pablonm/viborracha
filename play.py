import os
import numpy as np
from time import sleep
from model import get_model_decision, get_model
from game import Game, Point
from config import game_size

w = np.loadtxt('weights.txt', dtype=float)
b = np.loadtxt('bias.txt', dtype=float)
model = get_model(w, b)

def on_tick(game):
  os.system( 'clear' )
  print('Score: ', game.score)
  def mapPosition(pos):
    if pos == game.position:
      if game.direction[0] == [-1, 0]: return "^"
      if game.direction[0] == [1, 0]: return "v"
      if game.direction[0] == [0, 1]: return ">"
      if game.direction[0] == [0, -1]: return "<"
    if pos in game.tail:
        return 'T'
    if pos == game.food:
        return 'F'
    return '.'
  for i in range(game.map_size):
    print(*[mapPosition(Point(i, j)) for j in range(game.map_size)])
  sleep(0.1)

while True:
  Game(game_size, get_model_decision(model, game_size), None, on_tick, True)