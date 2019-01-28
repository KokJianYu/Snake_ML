# Genetic Algorithm

## Introduction

This directory contains code for a Snake Game AI that is trained using Genetic Algorithm 

![Snake Gameplay](image/generation_40.gif)

## Description
This algorithm trains the AI by simulating natural selection. The population for the first generation was generated at random, and the later generations will then be produced by crossbreeding the top performing snakes from the previous generation. 

The snakes chosen to crossbreed are selected based on their fitness function, with a higher fitness meaning that they have a higher chance to be selected as a parent. 

The snake runs on a neural network with 14 input units, 3 hidden layers with 30 units, and an output layer with 3 units.

The input layer consists of:
* Distance of snake to the wall boundaries (Left, Front, Right)
* Distance of snake to its tail (Left, Front, Right)
* Direction the snake is facing (Up, Down, Left, Right)
* Distance from food to snake (Up, Down, Left, Right)

The output layer consists of the following possible actions the snake can take:
* Move left
* Move front
* Move right
  
## Running Instructions
You can train the snake AI model by running `main.py`.

Performance of pretrained models can be viewed by running `plotGenerationToScoreGraph.py`.

By default, the Snake game GUI will not be shown. The boolean `SHOW_GUI` in both of this file can be changed to `True` to display GUI.

## Results
I have trained the AI for 40 generations, with the average score of 10 games for each generation of AI compiled in the following graph. 

![Graph of performance](image/Figure_1.png)


