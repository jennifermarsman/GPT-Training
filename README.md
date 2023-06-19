# GPT-Training
Leverage the power of GPT models to train new employees.  

## Overview
Training of new employees can be a costly endeavor.  This demonstration uses GPT-4 to generate a quiz question for a new employee, given a manual excerpt.  The employee can then answer the quiz question, and the AI will evaluate the answer and provide feedback.  This can be used to train new employees on the job, and to evaluate their understanding of the material.

Note that the manual excerpt is shown here for demonstration purposes, but in a real-world application, the manual excerpt would be hidden from the employee.  You are also not limited to one short excerpt; code can iterate over a manual or group of documents and generate many questions on the material.

## Setup
Use the following commands in a python environment (such as an Anaconda prompt window) to set up your environment.  This creates and activates an environment and installs the required packages.  For subsequent runs after the initial install, you will only need to activate the environment and then run the python script.  

```
conda create --name trainer python=3.9 -y
conda activate trainer

pip install -r requirements.txt
python run.py
```
