import numpy as np
from copy import copy
from game import Point
from neural_network import Neural_Network
from config import game_size

class_names = ['L', 'F', 'R']

def get_model(weights=[], bias=[]):
    return Neural_Network(9, 6, 3, weights, bias)

def get_model_decision(model, game_size):
  def decide(game):
    def _get_vision_in_direction(directions):
      def _next_pos(pos, directions):
        pos.x += directions[0]
        pos.y += directions[1]
      def _is_out_of_bounds(pos):
        return pos.x < 0 or pos.x >= game_size or pos.y < 0 or pos.y >= game_size
      def _food_in_pos(pos):
        return pos == game.food
      def _tail_in_pos(pos):
        return pos in game.tail
      def _normalize(val):
        return  1 - val / (game_size - 1)

      pos = copy(game.position)
      _next_pos(pos, directions)
      will_crash = 0
      food_found = 0
      tail_distance = 9
      tail_found = False
      distance = 0
      if _is_out_of_bounds(pos) or _tail_in_pos(pos): will_crash = 1
      while not _is_out_of_bounds(pos):
        if _tail_in_pos(pos) and not tail_found: 
          tail_found = True
          tail_distance = distance
        if _food_in_pos(pos) and not tail_found: food_found = 1
        _next_pos(pos, directions)
        distance += 1
      return [will_crash, food_found, _normalize(tail_distance)]

    left = _get_vision_in_direction(game.direction[3])
    front = _get_vision_in_direction(game.direction[0])
    right = _get_vision_in_direction(game.direction[1])
    input = np.array([left, front, right]).flatten()
    decision = model.think(input)
    return class_names[decision]
  return decide

def calculate_fitness(game):
  return game.score