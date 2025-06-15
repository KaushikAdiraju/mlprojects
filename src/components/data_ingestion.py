import os
import sys
from src.exception import CustomException
from src.logging import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")  #the resultant path would be artifacts/train.csv
    test_data_path: str=os.path.join('artifacts',"test.csv")    #the resultant path would be artifacts/test.csv
    raw_data_path: str=os.path.join('artifacts',"data.csv")     # the resultant path would be artifacts/data.csv for the raw data


class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df=pd.read_csv(r"C:\Users\kaush\Downloads\stud.csv") # Reading the dataset
            logging.info("Read the Dataset as a Data Frame")
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)  
            #Here the directories are made self.ingestion_config is the object and train_data_path is the attribute
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)  #Raw data is stored in a seperate file
            train_data,test_data = train_test_split(df,test_size = 0.20) #traintest split is made 80% for training and 20% for testing
            train_data.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            #train data is stored in artifacts/train_data
            test_data.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            #test data is stored in artifacts/test_data
            logging.info("Ingestion of the data is completed")
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )



        except Exception as e:
            raise CustomException(e,sys)
obj1 = DataIngestion()
obj1.initiate_data_ingestion()
#after this step the data is stored in this format
