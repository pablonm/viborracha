
import numpy as np
from model import get_model
from random import randrange
from config import best_selection_rate

def get_initial_population(size):
  return [get_model() for i in range(size)]

def select_best_chromosomes(population, scores):
  amount_to_select = round(len(population) * best_selection_rate)
  best_indexes = np.argpartition(scores, -amount_to_select)[-amount_to_select:]
  return [population[i] for i in best_indexes] 

def get_new_population(models, selected_chromosomes, size):
  new_chromosomes = np.array([])
  for i in range(len(selected_chromosomes)):
    for j in range(int(1 / best_selection_rate)):
      random_partner_index = randrange(0, len(selected_chromosomes))
      new_model = get_model(
        _crossover(selected_chromosomes[i].get_weights(), selected_chromosomes[random_partner_index].get_weights()),
        _crossover(selected_chromosomes[i].get_bias(), selected_chromosomes[random_partner_index].get_bias()))
      new_chromosomes = np.append(new_chromosomes, new_model)
  for i in range(len(new_chromosomes)):
    if i % 2 == 0:
      new_chromosomes[i].set_weights(_mutate(new_chromosomes[i].get_weights()))
      new_chromosomes[i].set_bias(_mutate(new_chromosomes[i].get_bias()))
  return new_chromosomes

def _crossover(chromosome1, chromosome2):
  return np.array([chromosome1[i] if i % 2 == 0 else chromosome2[i] for i in range(len(chromosome1))])

def _mutate(chromosome):
  new_chromosome = np.copy(chromosome)
  for i in range(len(chromosome)):
    if np.random.random() > 0.9:
      if np.random.random() > 0.5:
        new_chromosome[i] += chromosome[i] * 0.05
      else:
        new_chromosome[i] -= chromosome[i] * 0.05
  return new_chromosome
