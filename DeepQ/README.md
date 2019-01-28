# Deep Q Learning

## Introduction

This directory contains code for a Snake Game AI that utilises an algorithm in Deep Reinforcement Learning known as Deep Q Learning. 

![Snake Gameplay](image/episode_380_62.gif)

## Description
This algorithm trains the AI by providing it with either a reward or penalty depending on its action. Overtime, the AI will be able to learn the actions that it should perform in order to obtain the highest reward.

The snake runs on a neural network with 14 input units, 3 hidden layer with 30 units, and an output layer with 3 units.

The input layer consist of:
* Distance of snake to the wall boundaries (Left, Front, Right)
* Distance of snake to its tail (Left, Front, Right)
* Direction the snake is facing (Up, Down, Left, Right)
* Distance from food to snake (Up, Down, Left, Right)

The output layer consist of the following possible actions the snake can take:
* Move left
* Move front
* Move right
* 
## Results
I have trained the AI for 400 episodes, with the performance of it compiled in the following graph. 

![Graph of performance](image/Figure_1.png)


