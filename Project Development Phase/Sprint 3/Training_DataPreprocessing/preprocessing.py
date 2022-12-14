import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import RandomOverSampler
from imblearn.combine import SMOTETomek


from Application_Logging.logger import App_Logger


class Preprocessor:

    def __init__(self):
        self.file_object = 'Training_Preprocessing.txt'
        self.logger_object = App_Logger()

    def remove_unwanted_spaces(self,data):

        self.logger_object.log(self.file_object, 'Entered the remove_unwanted_spaces method of the Preprocessor class')
        self.data = data
        try:
            self.df_without_spaces = self.data.apply(
                lambda x: x.str.strip() if x.dtype == "object" else x)  # drop the labels specified in the columns
            self.logger_object.log(self.file_object,'Unwanted spaces removal Successful.Exited the remove_unwanted_spaces method of the Preprocessor class')
            return self.df_without_spaces

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in remove_unwanted_spaces method of the Preprocessor class. Exception message:  ' + str(e))

            self.logger_object.log(self.file_object,'unwanted space removal Unsuccessful. Exited the remove_unwanted_spaces method of the Preprocessor class')

            raise Exception()


    def manual_preprocessing(self, data):

        """
        This method contains various manual preprocessing steps which needed to be done based on the EDA Performed

        """
        try:
            self.logger_object.log(self.file_object,
                                   'Entered the manual_preprocessing method of the Preprocessor class')


            data.rename(
                columns={"default payment next month": "default_payment_next_month"}, inplace=True
            )

            # Lets handle the Education column
            data = data.drop(data[data['EDUCATION'] == 0].index)
            data["EDUCATION"] = np.where(data["EDUCATION"] == 6, 5, data["EDUCATION"])

            # for Marriage column
            data['MARRIAGE'].replace(0, 3, inplace=True)

            # for PAY_n columns
            # since PAY_n can take as values only -1,1,2,3,4,5,6,7,8,9
            # for att in ['PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6']:
            #     # categories -2,-1 are grouped into a single class -1: pay duty
            #     filter = (data[att] == -2) | (data[att] == -1)
            #     data.loc[filter, att] = -1
            #     # print(data[att].unique())
            #     # moreover the category 0 is undocumented
            #     # so each category >= 0 has been updated by adding 1
            #     data[att] = data[att].astype('int64')
            #     filter = (data[att] >= 0)
            #     data.loc[filter, att] = data.loc[filter, att] + 1

            self.logger_object.log(self.file_object,
                                   'manual_preprocessing method of the Preprocessor class is successfully executed!!')
            return data

        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in manual_preprocessing method of the Preprocessor class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'manual_preprocessing failed. Exited the manual_preprocessing method of the Preprocessor class')
            raise Exception()


    def one_hot_encoding(self, data):
        # Set 'category' type to categorical attributes

        try:
            self.logger_object.log(self.file_object,
                                   'Entered the one_hot_encoding method of the Preprocessor class')

            for att in ['SEX', 'EDUCATION', 'MARRIAGE']:
                data[att] = data[att].astype('category')

            # one-hot encoding
            data = pd.concat([pd.get_dummies(data['SEX'], prefix='SEX'),
                              pd.get_dummies(data['EDUCATION'], prefix='EDUCATION'),
                              pd.get_dummies(data['MARRIAGE'], prefix='MARRIAGE'),
                              data], axis=1)

            # drop original columns
            data.drop(['EDUCATION'], axis=1, inplace=True)
            data.drop(['SEX'], axis=1, inplace=True)
            data.drop(['MARRIAGE'], axis=1, inplace=True)

            self.logger_object.log(self.file_object,
                                   'one_hot_encoding is completed!!!')
            return data


        except Exception as e:
            self.logger_object.log(self.file_object,
                                   'Exception occured in one_hot_encoding method of the Preprocessor class. Exception message:  ' + str(
                                       e))
            self.logger_object.log(self.file_object,
                                   'one_hot_encoding failed. Exited the one_hot_encoding method of the Preprocessor class')
            raise Exception()


    def impute_missing_values(self, data, cols_with_missing_values, imputer='mean'):
        """
                    Method Name: impute_missing_values
                    Description: This method replaces all the missing values in the Dataframe using KNN Imputer.
                    Output: A Dataframe which has all the missing values imputed.
                    On Failure: Raise Exception

        """
        self.logger_object.log(self.file_object, 'Entered the impute_missing_values method of the Preprocessor class')
        self.data= data
        self.cols_with_missing_values=cols_with_missing_values
        try:
            for col in self.cols_with_missing_values:
                if imputer == 'mean':
                    self.data[col] = self.data.fillna(self.data[col].mean())
                elif imputer == 'mode':
                    self.data[col] = self.data.fillna(self.data[col].mode()[0])
                else:
                    self.data[col] = self.data.fillna(self.data[col].median())

            self.logger_object.log(self.file_object, 'Imputing missing values Successful. Exited the impute_missing_values method of the Preprocessor class')
            return self.data

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in impute_missing_values method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'Imputing missing values failed. Exited the impute_missing_values method of the Preprocessor class')
            raise Exception()

    def remove_unwanted_columns(self,data,columns):

        self.logger_object.log(self.file_object, 'Entered the remove_columns method of the Preprocessor class')
        self.data = data
        self.columns = columns
        try:
            self.useful_data = self.data.drop(labels=self.columns, axis=1)  # drop the labels specified in the columns
            self.logger_object.log(self.file_object, 'Column removal Successful.Exited the remove_columns method of the Preprocessor class')
            return self.useful_data
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in remove_columns method of the Preprocessor class. Exception message:  '+str(e))
            self.logger_object.log(self.file_object,'Column removal Unsuccessful. Exited the remove_columns method of the Preprocessor class')

            raise Exception()

    def separate_target_feature(self, data, label_column_name):

        self.logger_object.log(self.file_object, 'Entered the separate_label_feature method of the Preprocessor class')
        self.data=data
        self.label_column_name=label_column_name
        try:
            self.X = self.data.drop(labels=self.label_column_name,
                                    axis=1)  # drop the columns specified and separate the feature columns
            self.Y = self.data[self.label_column_name]  # Filter the Label columns
            self.logger_object.log(self.file_object,'Label Separation Successful. Exited the separate_label_feature method of the Preprocessor class')

            return self.X, self.Y
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in separate_label_feature method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'Label Separation Unsuccessful. Exited the separate_label_feature method of the Preprocessor class')
            raise Exception()

    def is_null_present(self,data):

        self.logger_object.log(self.file_object, 'Entered the is_null_present method of the Preprocessor class')
        self.data=data
        self.null_present = False
        self.cols_with_missing_values = []
        self.cols = self.data.columns
        try:
            self.null_counts = self.data.isna().sum()  # check for the count of null values per column
            for i in range(len(self.null_counts)):
                if self.null_counts[i] > 0:
                    self.null_present = True
                    self.cols_with_missing_values.append(self.cols[i])
            if (self.null_present):  # write the logs to see which columns have null values
                self.dataframe_with_null = pd.DataFrame()
                self.dataframe_with_null['columns'] = self.data.columns
                self.dataframe_with_null['missing values count'] = np.asarray(self.data.isna().sum())
                self.dataframe_with_null.to_csv('preprocessing_data/null_values.csv') # storing the null column information to file
            self.logger_object.log(self.file_object,'Finding missing values is a success.Data written to the null values file. Exited the is_null_present method of the Preprocessor class')
            return self.null_present, self.cols_with_missing_values
        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in is_null_present method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'Finding missing values failed. Exited the is_null_present method of the Preprocessor class')
            raise Exception()

    def scale_numerical_columns(self,data):

        self.logger_object.log(self.file_object,'Entered the scale_numerical_columns method of the Preprocessor class')
        self.data=data

        try:
            self.cat_df = self.data.select_dtypes(exclude=['int64']).copy()
            print(self.cat_df.shape)
            self.num_df = self.data.select_dtypes(include=['int64']).copy()
            print(self.num_df.shape)

            self.scaler = StandardScaler()
            self.scaled_data = self.scaler.fit_transform(self.num_df)#scaling the numerical values
            self.scaled_num_df = pd.DataFrame(data=self.scaled_data, columns=self.num_df.columns)

            #self.cat_df.append(self.scaled_num_df)
            self.scaled_num_df = pd.concat([self.cat_df, self.scaled_num_df], axis=1, join='inner')
            print(self.scaled_num_df.head())
            self.logger_object.log(self.file_object, 'scaling for numerical values successful. Exited the scale_numerical_columns method of the Preprocessor class')
            return self.cat_df

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in scale_numerical_columns method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'scaling for numerical columns Failed. Exited the scale_numerical_columns method of the Preprocessor class')
            raise Exception()

    def encode_categorical_columns(self,data):

        self.logger_object.log(self.file_object, 'Entered the encode_categorical_columns method of the Preprocessor class')
        self.data=data

        try:
            self.cat_df = self.data.select_dtypes(include=['object']).copy()
            # Using the one hot encoding to encode the categorical columns to numerical ones
            for col in self.cat_df.columns:
                self.cat_df = pd.get_dummies(self.cat_df, columns=[col], prefix=[col], drop_first=True)

            self.logger_object.log(self.file_object, 'encoding for categorical values successful. Exited the encode_categorical_columns method of the Preprocessor class')
            return self.cat_df

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in encode_categorical_columns method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object, 'encoding for categorical columns Failed. Exited the encode_categorical_columns method of the Preprocessor class')
            raise Exception()

    def handle_imbalanced_data(self,x,y):

        self.logger_object.log(self.file_object,'Entered the handle_imbalanced_dataset method of the Preprocessor class')

        try:
            rdsmple = SMOTETomek() #Using Oversampling balancing the dataset
            x_sampled, y_sampled = rdsmple.fit_resample(x, y)
            self.logger_object.log(self.file_object,'dataset balancing successful. Exited the handle_imbalanced_dataset method of the Preprocessor class')
            return x_sampled, y_sampled

        except Exception as e:
            self.logger_object.log(self.file_object,'Exception occured in handle_imbalanced_dataset method of the Preprocessor class. Exception message:  ' + str(e))
            self.logger_object.log(self.file_object,'dataset balancing Failed. Exited the handle_imbalanced_dataset method of the Preprocessor class')
            raise Exception()

