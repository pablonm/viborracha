from random import randrange
from dataclasses import dataclass
from collections import deque
from copy import copy

@dataclass()
class Point:
  x: int
  y: int
  def __hash__(self):
    return hash("{}-{}".format(self.x, self.y))


class Game:
  def __init__(self, map_size, snakeDecisionCallback, lostCallback, tickCallback, randomizePosDir = False):
    self.snakeDecisionCallback = snakeDecisionCallback
    self.tickCallback = tickCallback
    self.lostCallback = lostCallback
    self.map_size = map_size
    self.tail = deque([], 5)
    self.score = 0
    self.moves = 0
    self.direction = deque([[-1, 0], [0, 1], [1, 0], [0, -1]], 4)
    if randomizePosDir:
      self.position = Point(randrange(1, map_size), randrange(1, map_size))
      self.direction.rotate(randrange(0, 3))
    else:
      self.position = Point(round(self.map_size / 2), round(self.map_size / 2))
    self.energy = self._calculate_energy()
    self._spanw_initial_food()
    self._play()

  def _spawn_food(self):
    new_food = Point(randrange(1, self.map_size), randrange(1, self.map_size))
    if new_food == self.position or new_food in self.tail or new_food.x == self.position.x or new_food.y == self.position.y:
      self._spawn_food()
      return 
    self.food = new_food
    return

  def _spanw_initial_food(self):
    self._spawn_food()
    while (self._get_distance_to_food() < self.map_size / 2):
      self._spawn_food()
  
  def _inscrese_tail(self):
    self.tail = deque(self.tail, self.tail.maxlen + 1)
    self.tail.appendleft(3)

  def _eat_food(self):
    self.score += 1
    self.visited = {self.position}
    self.moves_in_food_direction = 0
    self.energy = self._calculate_energy()
    self._inscrese_tail()
    self._spawn_food()

  def _calculate_energy(self):
    return self.map_size * self.map_size

  def _check_lost(self):
    return (
      self.position.x >= self.map_size or
      self.position.x < 0 or
      self.position.y >= self.map_size or
      self.position.y < 0 or
      self.position in self.tail or
      self.energy == 0
    )

  def _move(self):
    self.energy -= 1
    self.moves += 1
    self.tail.append(Point(self.position.x, self.position.y))
    self.position = Point(self.position.x + self.direction[0][0], self.position.y + self.direction[0][1])
    if (self.position == self.food):
      self._eat_food()

  def _tick(self):
    self._relative_direction_to_absolute(self.snakeDecisionCallback(self))
    self._move()

  def _play(self):
    while(True):
      if self.tickCallback: self.tickCallback(self)
      self._tick()
      if self._check_lost():
        if self.lostCallback: self.lostCallback(self)
        break

  def _get_distance_to_food(self):
    return abs(self.food.x - self.position.x) + abs(self.food.y - self.position.y)
    
  def _relative_direction_to_absolute(self, dir):
    if (dir == 'R'):
      self.direction.rotate(1)
    if (dir == 'L'):
      self.direction.rotate(-1)