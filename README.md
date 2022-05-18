# Rubik's cube color classification with Raspberry Pi using MobileNetV2

*This is my school project and also my first project to train a deep learning model. As a beginner, I just want to share how I trained so this is not something like a tutorial. And I am not sure whether my method is good but it works well with my own dataset. So if you get stuck with a similar application, you may give it a try. Any comments or suggestions are welcome.*

## Introduction
  My goal is to train many models, each one can detect a single color on the Rubik's cube. Then with the prediction results, I give it to the rubik_solver module (installed from [here](https://pypi.org/project/rubik-solver/)) to get a near optimal solution, and then show it to the screen so that any user can solve the cube within 26 moves, all they have to do is just click the Next button, take 2 images, and wait for the result.
  ![alt text](https://github.com/[cheee123]/[Rubik-classification]/concept.jpg?raw=true "The final result")
  The problem is split into two parts, first is how to train the model, second is how to build the app on Raspberry Pi. I trained the model using Google Colab Pro, . About the hardware, I am using Raspeberry Pi 4, a PiCamera module, 
  
  
## Dataset


## Build and train the model

## Things to do on Raspberry Pi
