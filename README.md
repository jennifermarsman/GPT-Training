# GPT-Training
Leverage the power of GPT models to train new employees.  

## Overview
Training of new employees can be a costly endeavor.  This demonstration uses GPT-4 to generate a quiz question for a new employee, given a manual excerpt.  The employee can then answer the quiz question, and the AI will evaluate the answer and provide feedback.  This can be used to train new employees on the job, and to evaluate their understanding of the material.

Note that the manual excerpt is shown here for demonstration purposes, but in a real-world application, the manual excerpt would be hidden from the employee.  You are also not limited to one short excerpt; code can iterate over a manual or group of documents and generate many questions on the material.

## Setup
This project requires creating an Azure OpenAI resource to run the GPT-4 model in the Azure cloud.  
+ You can request access to Azure OpenAI at https://aka.ms/oai/access.  
+ After approval, create an Azure OpenAI resource at https://portal.azure.com/#create/Microsoft.CognitiveServicesOpenAI following the instructions at https://learn.microsoft.com/azure/cognitive-services/openai/how-to/create-resource.  
+ You will need to create a model deployment of a gpt-4 model.  Follow the instructions [here](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource#deploy-a-model).  

Next, after cloning this repo locally, update the run.py file with your settings.  
+ Update **gpt4_endpoint** with the name of your Azure OpenAI resource; this value should look like this: "https://YOUR_AOAI_RESOURCE_NAME.openai.azure.com/"
+ Update **gpt4_api_key** with the corresponding API key for your Azure OpenAI resource.  
+ Update **gpt4_deployment_name** with the name of your model deployment for GPT-4 in your Azure OpenAI resource.  

Finally, use the following commands in a python environment (such as an Anaconda prompt window) to set up your environment.  This creates and activates an environment and installs the required packages.  For subsequent runs after the initial install, you will only need to activate the environment and then run the python script.  

### First run
```
conda create --name trainer python=3.9 -y
conda activate trainer

pip install -r requirements.txt
python run.py
```

### Subsequent runs
```
conda activate trainer
python run.py
```
