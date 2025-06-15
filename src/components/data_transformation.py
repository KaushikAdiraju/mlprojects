import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer 
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.exception import CustomException
from src.logging import logging
import os
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")
    #This is where all the data after preprocessing converted into pickle file.
class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()   #self.data_transformation configuration is the object made with DataTransformationConfig() class
    
    def get_data_transformer_object(self):
        '''
        This function si responsible for data transformation
        
        '''
        try:
            numerical_columns = ["writing_score", "reading_score"]  #Numerical Columns in the data
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]                                    #categorical columns in the data
            num_pipeline= Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())

                ]
            )      #IN pipeline for numerical columns first null values are imputed with mean and then standard scaling done
            cat_pipeline=Pipeline(

                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]   #IN pipleline for categorical columns first null values with mode,encoded,and those are standard scaling.

            )
            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]


            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)   #reading training dataset
            test_df=pd.read_csv(test_path)     #reading testing dataset
            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")
            preprocessing_obj=self.get_data_transformer_object()  #preprocessing_obj is an object which contains all the pipeline
            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)  #all the columns except target_column
            target_feature_train_df=train_df[target_column_name] #target_column is taken (for training)
            input_feature_test_df = test_df.drop(columns=target_column_name,axis=1) #for testing all the columns except target_column is taken
            target_feature_test_df = test_df[target_column_name]    #for validation we have target_column is taken
            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )
            


            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)  #undergoing all the preprocessing steps in the pipeline
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)   #undergoing all the preprocessing steps in the pipeline but it is transform as it is test data

            train_arr = np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]  #combining column wise input_feature_train_arr and its corresponding target feature
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            #combining column wise input_feature_test_arr and its corresponding target feature
            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e,sys)

            