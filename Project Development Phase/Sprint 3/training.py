import pandas as pd
from train_validation_insertion import TrainingFilesValidation as train_validation
from training_model import TrainModel as trainModel

"""
Starting point of the training
def start_training():
    try:
        path = 'Training_BatchFiles/'

        # Entry point of the data validation and data preprocessing stages
        train_valObj = train_validation(path)  # object initialization
        train_valObj.train_validation()  # calling the training_validation function



    except Exception as e:
        print("Something went wrong in start_training.The exception is "+str(e))

if __name__ == "__main__":
    start_training()
