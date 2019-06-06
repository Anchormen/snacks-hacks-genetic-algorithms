#!/usr/bin/python

"""
Below is an example of how to paint a polygon in TK. Your mission, if you choose to accept, is to create a genetic
algorithm that tries to approximate a given target image.
A gene is a random collections of points together with an RGBA color. In other words: The genome is a collection of polygons.
As a fitness function you can sum the pixel distance with the target image.
"""

from tkinter import *
import PIL
import random
import math
import numpy as np
from sortedcontainers import SortedList
from PIL import Image, ImageDraw, ImageTk

TARGET_IMAGE_PATH = "/home/jvlek/Desktop/anchormen-logomark-rgb.png"
GENOME_SIZE = 8
MIN_POLYGON_SIZE = 3
MAX_POLYGON_SIZE = 9
NUM_REPRODUCTIONS = 50
POPULATION_SIZE = 300
MAX_ITERATIONS = 10000
EVOLUTION_PERIOD_MS = 1
UPDATE_INTERVAL = 10
DRAW_MODE = 'RGBA'


class PolygonOrganism:
    def __init__(self, num_polygons, environment):
        self.genome = []
        for _ in range(num_polygons):
            num_points = random.randint(MIN_POLYGON_SIZE, MAX_POLYGON_SIZE)
            polygon = [(random.randint(0, environment["width"]), random.randint(0, environment["height"])) for _ in
                       range(num_points)]
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.genome.append((polygon, color))
        self.environment = environment
        self.fitness = 0

    def mate(self, other_organism):
        mid_point = math.floor(len(self.genome) / 2)
        child_genome = self.genome
        child_genome[mid_point:-1] = other_organism.genome[mid_point:-1]

        child_organism = PolygonOrganism(0, self.environment)
        child_organism.genome = child_genome

        return child_organism

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __ge__(self, other):
        return self.fitness >= other.fitness


class Population:
    def __init__(self, population_size, environment, fitness_func):
        self.max_population_size = population_size
        self.environment = environment
        self.fitness_func = fitness_func

        initial_population = [PolygonOrganism(GENOME_SIZE, environment) for _ in range(population_size)]
        for organism in initial_population:
            organism.fitness = self.fitness_func(organism)
        self.population = SortedList(initial_population)

    def evolve(self):
        """
        Do one epoch of evolution and return the fittest organism
        """

        offspring = self.procreate()
        self.population.update(offspring)
        self.decimate()

    def procreate(self):
        offspring = []
        for i in range(NUM_REPRODUCTIONS):
            left_parent = self.population[i]
            right_parent = self.population[i + NUM_REPRODUCTIONS]
            child = left_parent.mate(right_parent)
            child.fitness = self.fitness_func(child)
            offspring.append(child)

        return offspring

    def decimate(self):
        while self.max_population_size < len(self.population):
            self.population.pop()


def draw_phenotype(organism):
    phenotype = PIL.Image.new(DRAW_MODE, (organism.environment["width"], organism.environment["height"]))
    draw = PIL.ImageDraw.Draw(phenotype, DRAW_MODE)

    for (polygon, color) in organism.genome:
        draw.polygon(polygon, color, color)

    del draw
    return phenotype


def make_fitness_function(target_image):
    def fitness(organism):
        phenotype = np.array(draw_phenotype(organism)).astype(float)
        return np.sum(((target_image - phenotype) ** 2))

    return fitness


class App:
    def __init__(self, population):
        self.root = Tk()
        self.panel = Label(self.root)
        self.population = population
        self.iter_count = 0

    def update_panel(self):
        self.population.evolve()
        self.iter_count += 1

        if self.iter_count % UPDATE_INTERVAL == 0:
            best_organism = self.population.population[0]
            worst_organism = self.population.population[-1]
            print("Iteration: " + str(self.iter_count) + " -- Best fitness: " + str(best_organism.fitness) +
                  " -- Worst fitness: " + str(worst_organism.fitness))
            best_phenotype = draw_phenotype(best_organism)
            photo_image = ImageTk.PhotoImage(best_phenotype)
            self.panel.configure(image=photo_image)
            self.panel.image = photo_image
            self.panel.pack(side="bottom", fill="both", expand="yes")

        self.root.after(EVOLUTION_PERIOD_MS, self.update_panel)

    def start(self):
        self.update_panel()
        self.root.mainloop()



target_image = Image.open(TARGET_IMAGE_PATH)

environment = {
    "width": target_image.size[0],
    "height": target_image.size[1]
}

target_image_np_array = np.array(target_image).astype(float)
population = Population(POPULATION_SIZE, environment, make_fitness_function(target_image_np_array))
app = App(population)
app.start()
