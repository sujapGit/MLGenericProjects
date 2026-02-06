## Transform data

import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd 
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline   
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.utils import save_object

## sklearn
## Composer - ColumnTransformer -  it use to create a pipeline
## impute - SimpleImputer- it is used for Missing values
## pipeline - Pipelien - implement pipeline

## preprocessing 
## OneHotEncoder 
## Purpose: Converts categorical data (like "red", "blue", "green") into numbers that models understand.

##StandardScaler
##Purpose: Standardizes numeric features to have mean=0, std=1.
## Why needed: ML algorithms (SVM, neural networks, logistic regression) perform better when features are on the same scale.

from src.exception import CustomException
from src.logger import logging
import os

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts',"preprocessor.pkl")



class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation_object(self):
        '''
         This function is responsible for data transformation
        '''      
        try:
            numberical_columns =["writing_score","reading_score"]
            categorical_columns =[
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]
            
            #numerical pipeline 
            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")), # handle missing values
                    ("scaler",StandardScaler())                    # standard scaling
                ])
            
            

            #categorical pipeline
            cat_pipeline=Pipeline(
                    steps=[
                        ("imputer",SimpleImputer(strategy="most_frequent")), # handle missing values with mode
                         ("one_hot_encoder", OneHotEncoder()),                # 
                        ("scaler",StandardScaler(with_mean=False))                        
                    ])
            
                
            
            logging.info("Numerical columns standard scaling completed")
            logging.info("Categorical columns encoding completed")
          
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,numberical_columns),
                    ("cat_pipelines",cat_pipeline,categorical_columns)

                ]
            )

            return preprocessor
            
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df =pd.read_csv(test_path)
            
            logging.info("Read train and test data completed")
            
            logging.info("Obtaining preprocessing object")

            preprocessing_obj =self.get_data_transformation_object()

            target_column_name ="math_score"
            numerical_columns = ["writing_score","reading_score"]
            
            input_feature_train_df = train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df = test_df[target_column_name]


            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )


            input_feature_train_arr =preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr =preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[
                input_feature_train_arr,np.array(target_feature_train_df)                
            ]

            test_arr = np.c_[input_feature_test_arr,np.array(target_feature_test_df )]
            logging.info("saved preprocessing object.") 

            save_object(
                file_path =self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (train_arr,
                    test_arr,
                    self.data_transformation_config.preprocessor_obj_file_path,)

        except Exception as e:
            raise CustomException(e,sys)

