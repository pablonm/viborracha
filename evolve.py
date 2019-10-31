import os
import numpy as np
from game import Game, Point
from model import get_model_decision
from population import get_initial_population, select_best_chromosomes, get_new_population
from config import game_size, generations, population_size

# Function that is executed when the game is lost
def get_on_lost_func(i):
  def _on_lost(game):
    scores[i] = game.score
  return _on_lost

# Function to print the game status on console
def get_on_tick(generation, chromosomeIndex, scores):
  def on_tick(game):
    os.system( 'clear' )
    print("Generation: ", generation + 1)
    print("Chromosome: ", chromosomeIndex + 1, "/", population_size)
    print("Best score: ", max(scores))
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
  return on_tick

# Create the starting generation
models = get_initial_population(population_size)

# for each generation...
for g in range(generations):

  # Run the game for each chromosome
  decision_funcs = [get_model_decision(model, game_size) for model in models]
  scores = np.array([0 for model in models])
  lost_funcs = [get_on_lost_func(i) for i in range(population_size)]
  for i in range(len(models)):
    Game(game_size, 
          decision_funcs[i], 
          lost_funcs[i], 
          get_on_tick(g, i, scores))

  # Save the best chromosome weights and bias to disk
  np.savetxt('weights.txt', models[np.argmax(scores)].get_weights(), fmt='%f')
  np.savetxt('bias.txt', models[np.argmax(scores)].get_bias(), fmt='%f')

  # Choose the best chromosomes
  selected_chromosomes = select_best_chromosomes(models, scores)

  # Get a new generation doing crossover and mutations
  models = get_new_population(models, selected_chromosomes, population_size)
