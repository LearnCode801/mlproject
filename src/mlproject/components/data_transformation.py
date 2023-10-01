import sys
import os
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from src.mlproject.exception import CustomException
from src.mlproject.logger import logging
from src.mlproject.utils import save_object
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path= os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_columns=['writing_score','reading_score']
            categorical_cloumns=['gender','race_ethnicity','parental_level_of_education','lunch','test_preparation_course']
            
            num_pipline=Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('scalar',StandardScaler())
            ])
            cat_pipeline=Pipeline(steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('one_hot_encoder',OneHotEncoder()),
                ('scaler',StandardScaler(with_mean=False))
            ])

            logging.info(f"Categorical Columns:{categorical_cloumns}")
            logging.info(f"Numercal Columns:{numerical_columns}")
            
            preprocessor=ColumnTransformer(
                [
                    ("num_pipline",num_pipline,numerical_columns),
                    ('cat_pipeline',cat_pipeline,categorical_cloumns)
                ]
            )

            return preprocessor
            
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            print(train_df)
            print(test_df)
            
            logging.info("Reading the train and test data")
            
            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math_score"
            # numerical_columns=['writing_score','reading_score']

            # divide the train dataset to independent and dependent feature
            input_features_train_df= train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            # divivde the test dataset to independent and dependent feature
            input_features_test_df= test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info("Now applying the preprocessing on the training and test dataset")
            
            input_features_train_arr=preprocessing_obj.fit_transform(input_features_train_df)
            input_features_test_arr=preprocessing_obj.transform(input_features_test_df)

            train_arr=np.c_[input_features_train_arr, np.array(target_feature_train_df)]
            test_arr=np.c_[input_features_test_arr,np.array(target_feature_test_df)]

            logging.info("Saved preprocessing object ")
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return( 
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
                )



        except Exception as e:
            raise CustomException(e,sys)






