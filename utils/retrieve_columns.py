from datetime import datetime
import sys
import pandas as pd
import os
import math
import numpy as np
"""
this function aims to retrieve target features from many input files,
and merge them to a new file to do future data analysis
the input is a list of files
the output will be a new file with target features
"""
# make sure your current path is \ProjectW81XWH1910495-keras then use python utils/retrieve_columns.py to run it

def read_file(input_path):
    file_type = os.path.splitext(input_path)[1]
    if file_type == ".txt":
        df = pd.read_csv(input_path, sep="\t")
    elif file_type == ".csv":
        df = pd.read_csv(input_path)
    elif file_type == ".xlsx":
        df = pd.read_excel(input_path)
    else:
        return None
    print(f'the length of file: {len(df)}')
    return df

def find_columns_to_be_expanded(data):
    if data is None:
        print('the dataset is empty! Please check!!')
        return None
    columns = data.columns
    candidate_columns = []
    for column in columns:
        parameter_list = data[column].tolist()
        # print(parameter_list)
        # check if this column has multiple values
        if not isinstance(parameter_list[0], str) or ":" not in parameter_list[0] or not isinstance(eval(parameter_list[0]), dict):
            continue
        candidate_columns.append(column)
    print(candidate_columns)
    return candidate_columns

def expand_parameters_stored_in_one_column(input_path, target_columns):
    """
    This function aims to expand parameters stored in one column, and put them in separate columns, to make data analysis easier
    Args:
        input_path: the original file which needs to expand parameters stored in one column
        target_columns: the columns which need to be expanded
            (in each column, the parameters are stored in a dictionary format)
    Returns:
        the new dataset
    """
    df = read_file(input_path)
    if df is None:
        print(f"the type of this file is incorrect, return!")
        return None, None
    target_columns_2 = []
    new_df = pd.DataFrame(df, columns=df.columns)
    for column in target_columns:
        if column not in df.columns:
            print(f"this target column-{column} isn't in our dataset")
            continue
        print(f'now extract the values of column: {column}')
        print('********')
        parameter_list = df[column].tolist()
        #print(parameter_list)
        #check if this column has multiple values
        if  not isinstance(parameter_list[0], str) or not isinstance(eval(parameter_list[0]),dict):
            target_columns_2.append(column)
            continue
        new_df = new_df.drop(columns=[column])
        parameter_label = list(eval(parameter_list[0]).keys())
        parameter_df = pd.DataFrame(columns=parameter_label)
        for item in parameter_list:
            item_dict = eval(item)
            parameter_df = parameter_df.append(item_dict, ignore_index=True)
        new_df = pd.concat([new_df, parameter_df], axis = 1)
        target_columns_2 += parameter_label
    print('finish extracting')
    return new_df, target_columns_2

def retrieve_values_of_target_columns(input_path,target_columns, output_path, unique, expand):
    """
    This function aims to retrieve all values/unique values of target columns;
    if one of the target columns is in a dictionary format, set expand to be True,
    and we'll expand it, and put them in separate columns
    Args:
        input_path: the path of input file
        target_columns: the columns names of target values
        output_path: a csv file with all target columns values
        uniaue: if equals true, the result will be unique values, else the result will be all values
        expand: if its true, when the format of target column is dictionary, all sub-parameters will be put in separate columns
    Returns:
        a csv file with all target columns values stored in output_path
    """
    df = read_file(input_path)
    if df is None:
        print(f'the type of the input file-{input_path} is incorrect!Please check!!')
        return
    for column in target_columns:
        if column not in df.columns:
            expand = True
            break
    if expand:
        all_columns = df.columns
        df = expand_parameters_stored_in_one_column(input_path, all_columns)[0]
    else:
        df = read_file(input_path)
    for column in target_columns:
        if column not in df.columns:
            print(f"there's still at least one column {column} is not in the dataset after expanding!Please check!")
            return
    print('target_columns', target_columns)
    print(df.columns,'df_columns')
    target_df = df[target_columns]
    if not unique:
        target_df.to_csv(output_path, index=False)
        print('successfully retrieve values of target_columns')
    else:
        new_df = target_df.drop_duplicates(subset= target_columns)
        new_df.to_csv(output_path, index=False)
        print('successfully retrieve unique values of target_columns')
    return

def retrieve_values_based_on_target_columns(input_path, requirements, range_requirements, output_path, unique, expand):
    """
    This function aims to extract subdataset based on the value of a specific column
    Args:
        input_path: the path of input files
        requirements: a dictionary of columns and its require values
        output_path: the path to store the target subdataset
        unique: if keep duplicate results
        expand: if needs to expand parameters stored in one column
    """
    df = read_file(input_path)
    if df is None:
        print(f'the type of the input file-{input_path} is incorrect!Please check!!')
        return
    for column in requirements.keys():
        if column not in df.columns:
            expand = True
            break
    for column in range_requirements.keys():
        if column not in df.columns:
            expand = True
            break
    if expand:
        all_columns = df.columns
        df = expand_parameters_stored_in_one_column(input_path, all_columns)[0]
    else:
        df = read_file(input_path)
    new_df = pd.DataFrame(df, columns = df.columns)
    for requirement in requirements:
        if requirement not in df.columns:
            print(f"this column-{requirement} isn't in this dataset! Please check again!")
            continue
        new_df = new_df.loc[new_df[requirement].isin(requirements[requirement])]
    for requirement in range_requirements:
        print(requirement)
        if requirement not in df.columns:
            print(f"this column-{requirement} isn't in this dataset! please check again!")
            continue
        #new_df = new_df.loc[new_df[requirement].map(lambda x: float(x) >= range_requirements[requirement][0])]
        #new_df = new_df.loc[new_df[requirement].map(lambda x: float(x) <= range_requirements[requirement][1])]
        new_df = new_df.loc[(new_df[requirement] <= range_requirements[requirement][1]) & (new_df[requirement] >= range_requirements[requirement][0])]

    if not unique:
        new_df.to_csv(output_path,index=False)
        print('not unique! successfully retrieve values of target_columns')
    else:
        new_df = new_df.drop_duplicates()
        new_df.to_csv(output_path , index=False)
        print('unique! successfully retrieve unique values of target_columns')
    print(f'the length of new dataset is: {len(new_df)}')
    return new_df

def retrieve_target_columns_based_on_values(input_path, requirements, range_requirements, target_columns,output_path, unique, expand):
    df = read_file(input_path)
    if df is None:
        print(f'the type of the input file-{input_path} is incorrect!Please check!!')
        return
    for column in requirements.keys():
        if column not in df.columns:
            expand = True
            break
    for column in range_requirements.keys():
        if column not in df.columns:
            expand = True
            break
    for column in target_columns:
        if column not in df.columns:
            expand = True
            break
    if expand:
        all_columns = df.columns
        df = expand_parameters_stored_in_one_column(input_path, all_columns)[0]
    else:
        df = read_file(input_path)
    for column in target_columns:
        if column not in df.columns:
            print(f"this target column-{column} isn't in this dataset! We will return!")
            return
    new_df = pd.DataFrame(df, columns=df.columns)
    for requirement in requirements:
        if requirement not in df.columns:
            print(f"this column-{requirement} isn't in this dataset! Please check again!")
            continue
        new_df = new_df.loc[new_df[requirement].isin(requirements[requirement])]
    for requirement in range_requirements:
        print(requirement)
        if requirement not in df.columns:
            print(f"this column-{requirement} isn't in this dataset! please check again!")
            continue
        # new_df = new_df.loc[new_df[requirement].map(lambda x: float(x) >= range_requirements[requirement][0])]
        # new_df = new_df.loc[new_df[requirement].map(lambda x: float(x) <= range_requirements[requirement][1])]
        new_df = new_df.loc[(new_df[requirement] <= range_requirements[requirement][1]) & (
                    new_df[requirement] >= range_requirements[requirement][0])]
    new_df = new_df[target_columns]
    if not unique:
        new_df.to_csv(output_path, index=False)
        print('not unique! successfully retrieve values of target_columns')
    else:
        new_df = new_df.drop_duplicates()
        new_df.to_csv(output_path, index=False)
        print('unique! successfully retrieve unique values of target_columns')
    print(f'the length of new dataset is: {len(new_df)}')
    return new_df
def sort_data_based_on_target_columns(input_path, target_columns, expand, unique, output_path, ascending, k):
    df = read_file(input_path)
    if df is None:
        print(f'the type of the input file-{input_path} is incorrect!Please check!!')
        return
    # for column in target_columns:
    #     if column not in df.columns:
    #         expand = True
    #         break
    if expand:
        all_columns = df.columns
        df = expand_parameters_stored_in_one_column(input_path, all_columns)[0]
    else:
        df = read_file(input_path)
    for column in target_columns:
        if column not in df.columns:
            print(f"there's still at least one column {column} is not in the dataset after expanding!Please check!")
            return
    if not k:
        sorted_df = df.sort_values(by = target_columns, ascending = ascending)
    else:
        sorted_df = df.sort_values(by = target_columns, ascending = ascending)[:k]
    if not unique:
        sorted_df.to_csv(output_path, index=False)
        print('successfully retrieve values of target_columns')
    else:
        sorted_df = sorted_df.drop_duplicates(subset= target_columns)
        sorted_df.to_csv(output_path, index=False)
        print('successfully retrieve unique values of target_columns')
    print(f'the length of new file: {len(sorted_df)}')
    return sorted_df
def find_intersection_of_different_table(file_paths, output_path, target_columns, expand, unique):
    df = read_file(input_path)
    if df is None:
        print(f'the type of the input file-{input_path} is incorrect!Please check!!')
        return
    for column in target_columns:
        if column not in df.columns:
            expand = True
            break
    if expand:
        all_columns = df.columns
        df = expand_parameters_stored_in_one_column(input_path, all_columns)[0]
    else:
        df = read_file(input_path)
    for column in target_columns:
        if column not in df.columns:
            print(f"there's still at least one column {column} is not in the dataset after expanding!Please check!")
            return
    names = df.columns
    df = pd.concat([pd.read_csv(f, header=None, skiprows=[0], names=names) for f in file_paths], how='inner', on=target_columns,ignore_index=True)
    print(len(df))
    if not unique:
        df.to_csv(output_path, index=False)
        print('successfully find intersections of input datasets')
    else:
        df = df.drop_duplicates(subset= target_columns)
        df.to_csv(output_path, index=False)
        print('successfully find intersections of input datasets')
    print(f'the length of new file: {len(sorted_df)}')
    return

def find_available_filters(data_path):
    data = read_file(data_path)
    print('begin to find available filters')
    diversity_filters = {}
    continuous_filters = {}
    #data.replace("nan", np.nan, inplace=True)
    #data = data.dropna(axis=1,how='any')
    print('begin')
    for column in data.columns:
        print(column)
        if pd.isnull(data.at[0, column]): continue
        if ":" in str(data.at[0,column]): continue
        length= len(data[column].unique())
        print(length)

        #if not result[0]: continue
        #if isinstance(result[0], str) and ":" in result[0]:
        #    continue
        if length <= 1: continue
        print(data.iloc[0:5][column].values)
        result = data.iloc[0:5][column]
        #print(result)
        if column =='rank_test_auc':
            print(result.dtype)
        if isinstance(result[0],str) and ":" in result[0]:
            continue
        if length>=20:
            if pd.api.types.is_float(result[0]) or isinstance(result[0],np.int32) or isinstance(result[0],np.int64):
                continuous_filters[column] = [data[column].min(), data[column].max()+0.001]
            else:
                diversity_filters[column] = data[column].unique()
        else:
            diversity_filters[column] = data[column].unique()
    print('finish')
    return diversity_filters, continuous_filters
# def retrieve_columns(input_path,parameterList,output_path, ifDeleteNull=False):
#     """
# this function is designed to retrieve a series important parameters from the original result table and merge into a new
# table to make further data analysis
#     Args:
#         originaltablepath: the path of the original result table as the input
#         parameterList: if the parameterList include parameter_and_values, it will separate to different columns respectively.
#         outputPath: the path that you want to store this new retrieve table
#     """
#     df = pd.read_csv(input_path, sep='\s|,|;')
#     if 'parameters_and_values' in parameterList:
#         parameter_list = df['parameters_and_values'].tolist()
#     if 'best_params_' in parameterList:
#         parameter_list = df['best_params_'].tolist()
#     parameter_label = list(eval(parameter_list[0]).keys())
#     parameter_df = pd.DataFrame(columns=parameter_label)
#     for item in parameter_list:
#         item_dict = eval(item)
#         if 'mstruct' in item_dict:
#             layer = list(item_dict['mstruct'])[0:-1]
#             layer_number = len(layer)
#             layer.extend([0, 0, 0, 0])
#             for i in range(4):
#                 item_dict["layer_number"] = layer_number
#                 item_dict[i+1] = layer[i]
#         parameter_df=parameter_df.append(item_dict,ignore_index=True)
#     if 'parameters_and_values' in parameterList:
#         parameterList.remove("parameters_and_values")
#     if 'best_params_' in parameterList:
#         parameterList.remove('best_params_')
#     rest_df = pd.DataFrame(df, columns=parameterList)
#     newTable = pd.concat([rest_df, parameter_df],axis=1)
#     if ifDeleteNull:
#         newTable.dropna(axis=0, how='any', inplace=True)
#     newTable.to_csv(output_path, index=False)
#     print(output_path + " generated successfully")


if __name__ == "__main__":
    print("hello")
    flag = int(sys.argv[1])
    table_path = "dataset/"
    table_name_list = ['10_year_stage3-5_test_expand.csv']  # Input path
    if flag == 1: #expand parameters which are stored in one column
        for file_name in table_name_list:
            output_path = "output_test_data/target_features_table_test_function1.csv"
            #target_columns = ['parameters_and_values', 'start_date_time']
            target_columns = ['parameters_and_values', ]
            new_df, target_columns = expand_parameters_stored_in_one_column(table_path + file_name, target_columns)
            new_df.to_csv(output_path, index=False)
    elif flag == 2:
        for file_name in table_name_list:
            output_path = "output_test_data/target_features_table_test_function2.csv"
            target_columns = ['start_date_time', 'end_date_time','parameters_and_values',]
            #target_columns = ['distant_recurrence']
            #   if unique == True: return unique values of target columns
            #   else: return all values of target columns
            unique = False
            #   if expand == True, use the function of expand_parameters_stored_in_one_column first,
            #   and retrieve target columns from the expanded dataset
            #   else: just retrieve from the original datasetgit sta

            expand = False
            retrieve_values_of_target_columns(table_path+file_name,target_columns, output_path, unique, expand)
    elif flag == 3:
        for file_name in table_name_list:
            output_path = "testing/output_test_data/xia_test_retrieving_subset_2022.11.2-ORG.csv"
            requirements = {'batch_size' : [100, 200],
                              'mstruct':[(354, 430, 392, 444, 1)]}
            #if there's no lowest bound, you could use min_left
            #if there's no highest bound, you could use max_right
            min_left = - float('INF')
            max_right = float('INF')
            range_requirements = {'percent_auc_diff': [min_left, 0.1],
                                  } #show the lowest bound and largest bound
            #   if unique == True: return unique values of target columns
            #   else: return all values of target columns
            unique = True
            #   if expand == True, use the function of expand_parameters_stored_in_one_column first,
            #   and retrieve target columns from the expanded dataset
            #   else: just retrieve from the original dataset
            #expand = True #if the requirement is sub-parameter, expand should be True
            # (if there's one request doesn't in the original column name, expand will be set to be True automatically
            expand = False #if the requirement is sub-parameter, expand should be True
            retrieve_values_based_on_target_columns(table_path + file_name, requirements, range_requirements, output_path, unique, expand)
        #retrieve_columns(table_path+file_name,target_features, output_path )
    elif flag == 4:
        for file_name in table_name_list:
            output_path = "../testing/output_test_data/2022.11.7_test_retrieve_columns_function4.csv"
            requirements = {'batch_size' : [100, 200],
                              'mstruct':[(354, 430, 392, 444, 1)]}
            #requirements = {'batch_size' : [100]}
            #requirements = {'distant_recurrence': [0]}
            #if there's no lowest bound, you could use min_left
            #if there's no highest bound, you could use max_right
            min_left = - float('INF')
            max_right = float('INF')
            range_requirements = {'percent_auc_diff': [min_left, 0.1],
                                  } #show the lowest bound and largest bound
            #   if unique == True: return unique values of target columns
            #   else: return all values of target columns
            unique = True
            #   if expand == True, use the function of expand_parameters_stored_in_one_column first,
            #   and retrieve target columns from the expanded dataset
            #   else: just retrieve from the original dataset
            #expand = True #if the requirement is sub-parameter, expand should be True
            # (if there's one request doesn't in the original column name, expand will be set to be True automatically
            expand = False #if the requirement is sub-parameter, expand should be True
            target_columns = ['start_date_time', 'end_date_time','parameters_and_values',]
            retrieve_target_columns_based_on_values(table_path + file_name, requirements, range_requirements, target_columns,output_path, unique, expand)
    elif flag == 5:
        for file_name in table_name_list:
            output_path = "output_test_data/yijun_test_sort_best_10_2022.11.4_epoch180.csv"
            target_columns = ['mean_test_auc']
            ascending = False #return the increasing sequence or not
            expand = False
            unique = False
            k = 10 # if need all samples, set it to be None
            sort_data_based_on_target_columns(table_path+file_name, target_columns, expand, unique, output_path, ascending, k)
    elif flag == 6:
        file_paths = ['input_test_data/10_year_stage3-5_140_merge.csv',
                      'input_test_data/10_year_stage3-5_140_ip164.csv',
                      'input_test_data/10_year_stage3-5_140_with_ip163.csv']  # input path
        output_path = 'output_test_data/intersection_test.csv'  # output path
        expand = False
        unique = False
        target_columns = ['parameters_and_values']
        find_intersection_of_different_table(file_paths, output_path, target_columns, expand,unique)
    elif flag == 7:

        for file_name in table_name_list:
            data = read_file(table_path+file_name)
            result = find_available_filters(data)
            print(result)
    #tablelist = {"20000.csv": "20000_retrieve.csv"}
    #tablelist = {"DNMStage1merged15Year.csv":"any.csv"}
    #tablelist = {"new_sk_model.csv":"anyML.csv"}
    # tablelist = {
    #     "h4_1.csv": "h4_retrieve_1.csv",
    #     "h4_2.csv": "h4_retrieve_2.csv",
    #     "h4_3.csv": "h4_retrieve_3.csv",

    #     "h4_4.csv": "h4_retrieve_4.csv",
    # }
    #tablelist = {
     #   "5_MandR_M7D26.csv": "5_LearningRateAndMomentum_M7D26_retrieved.csv",
       # "5_lrateanddecay_M6D30.csv": "5_lrateanddecay_M7D14_retrieved.csv",
        # "5 year_top10_validation.csv": "5 year_top10_validation_retrieved.csv",
        # "10 year_top10_validation.csv": "10 year_top10_validation_retrieved.csv",
        # "15 year_top10_validation.csv": "15 year_top10_validation_retrieved.csv"
        #"5 Year_top50_mean_test_AUC.csv": "5 Year_top50_mean_test_AUC_retrieved.csv",
        #"5_year_batchsize_superex.csv":"5_year_batchsize_superex_retrieve.csv"
        # "DNM-RF_stage2_5year_top50.csv":"DNM-RF_stage2_5year_top50_retrieve.csv",
        # "DNM-RF_stage2_10year_top50.csv":"DNM-RF_stage2_10year_top50_retrieve.csv",
        # "DNM-RF_stage2_15year_top50.csv": "DNM-RF_stage2_15year_top50_retrieve.csv"
        #"DNM-RF_stage2_15year_top1000.csv": "DNM-RF_stage2_15year_top1000_retrieve.csv",
        # "10_year_batchsize.csv": "10_year_batchsize_retrieve.csv",
        # "10_year_L1.csv": "10_year_L1_retrieve.csv",
        # "10_year_L2.csv": "10_year_L2_retrieve.csv",
        # "10_year_learningrate.csv": "10_year_learningrate_retrieve.csv",
        # "10_year_epochs.csv": "10_year_epochs_retrieve.csv",
        # "10_year_decay.csv": "10_year_decay_retrieve.csv",
        # "10_year_dropout.csv": "10_year_dropout_retrieve.csv",
    #}
    # tablelist = {
    #             # "batchsize_new_1.csv": "batchsize_new_1_retrieve.csv",
    #             # "batchsize_new_2.csv": "batchsize_new_2_retrieve.csv",
    #             # "learningrate_new_1.csv": "learningrate_new_1_retrieve.csv",
    #             # "learningrate_new_2.csv": "learningrate_new_2_retrieve.csv",
    #             # "L1_new_1.csv": "L1_new_1_retrieve.csv",
    #             # "L1_new_2.csv": "L1_new_2_retrieve.csv",
    #             # "L2_new_1.csv": "L2_new_1_retrieve.csv",
    #             # "L2_new_2.csv": "L2_new_2_retrieve.csv",
    #              "L1andL2_new_1.csv": "L1andL2_new_1_retrieve.csv",
    #              #"L1andL2_new_2.csv": "L1andL2_new_2_retrieve.csv",
    #
    #
    # }

    # for item in tablelist.keys():
    #     print("hello")
    #     retrieve_columns(originaltablePath = "DNM-RF/stage1/results/240/LSM-15Year-I-240_results/" + item,
    #                       parameterList = ["ml_classifier_name","host_name","running_time1(average sec)","parameters_and_values", "mean_test_auc","mean_train_auc", "percent_auc_diff"],
    #                      outputPath = "DNM-RF/stage1/retrieve/240/LSM-15Year-I-240_retrieve/" + tablelist[item],
    #                      ifDeleteNull=False)
    #for item in tablelist.keys():

        # retrieve_columns(originaltablePath = "manuscript_preparation/overfitting/supporting_docs/overfit result/overfit 11.28/" + item,
        #                   parameterList = ["ml_classifier_name","host_name","running_time1(average sec)","parameters_and_values", "mean_test_auc","mean_train_auc", "percent_auc_diff"],
        #                  outputPath = "manuscript_preparation/overfitting/supporting_docs/overfit result/overfit 11.28/" + tablelist[item],
        #                  ifDeleteNull=False)
   #     retrieve_columns(
            #originaltablePath="../DNM-RF/stage3-1/SummaryResultsAndAnalysis/" + item,
            #originaltablePath="../DNM-RF/stage3-4/" + item,
            # originaltablePath="../DNM/stage1/" + item,
            # parameterList=["ml_classifier_name", "host_name", "running_time1(average sec)", "running_time2(sec)","parameters_and_values",
            #                "mean_test_auc", "mean_train_auc", "percent_auc_diff"],
            # parameterList=["ml_classifier_name", "host_name", "running_time1(average sec)","running_time2(sec)","parameters_and_values",
            #                 "mean_test_auc", "mean_train_auc", "percent_auc_diff"],
            # parameterList=["exp_des", "best_index_", "val_score", "val_score_mal",
            #                "best_score_","best_params_", "best_estimator_", "n_splits_","refit_time_"],
            #outputPath="../DNM-RF/stage3-1/SummaryResultsAndAnalysis/" + tablelist[item],
            # outputPath="../DNM/stage1/" + tablelist[item],
            # ifDeleteNull=False)

    # tablelist = {
    #             "different_layer_2.csv": "different_layer_2_retrieve.csv",
    #             "different_layer_3.csv": "different_layer_3_retrieve.csv",
    #             "different_layer_4.csv": "different_layer_4_retrieve.csv",
    #             "different_layer_1.csv": "different_layer_1_retrieve.csv",
    #
    # }
    # tablelist = {
    #     "drate_new1.csv": "drate_new1_retrieve.csv",
    #     "drate_new2.csv": "drate_new2_retrieve.csv",
    #      "drate_new3.csv": "drate_new3_retrieve.csv",
    #      "drate_new4.csv": "drate_new4_retrieve.csv",
    # }
    # tablelist = {
    #              "batchsize_learningrate_1.csv": "batchsize_learningrate_1_retrieve.csv",
    #              "batchsize_learningrate_2.csv": "batchsize_learningrate_2_retrieve.csv",
    #              "batchsize_learningrate_3.csv": "batchsize_learningrate_3_retrieve.csv",
    #              "batchsize_learningrate_4.csv": "batchsize_learningrate_4_retrieve.csv",
    # }
    # tablelist = {
    #     "5_batchsize_1.csv": "5_batchsize_1_retrieve.csv",
    #     "5_batchsize_2.csv": "5_batchsize_2_retrieve.csv",
    #     "5_batchsize_3.csv": "5_batchsize_3_retrieve.csv",
    #     "5_batchsize_4.csv": "5_batchsize_4_retrieve.csv",
    # }
    # tablelist = {
    #     "5_epochs_1.csv": "5_epochs_1_retrieve.csv",
    #     "5_epochs_2.csv": "5_epochs_2_retrieve.csv",
    #     "5_epochs_3.csv": "5_epochs_3_retrieve.csv",
    #     "5_epochs_4.csv": "5_epochs_4_retrieve.csv",
    # }
    # tablelist = {
    #     "5_L1_1.csv": "5_L1_1_retrieve.csv",
    #     "5_L1_2.csv": "5_L1_2_retrieve.csv",
    #     "5_L1_3.csv": "5_L1_3_retrieve.csv",
    #     "5_L1_4.csv": "5_L1_4_retrieve.csv",
    # }
    # tablelist = {
    #     "5_L2_1.csv": "5_L2_1_retrieve.csv",
    #     "5_L2_2.csv": "5_L2_2_retrieve.csv",
    #     "5_L2_3.csv": "5_L2_3_retrieve.csv",
    #     "5_L2_4.csv": "5_L2_4_retrieve.csv",
    # }
    # tablelist = {
    #     "5_learningrate_1.csv": "5_learningrate_1_retrieve.csv",
    #     "5_learningrate_2.csv": "5_learningrate_2_retrieve.csv",
    #     "5_learningrate_3.csv": "5_learningrate_3_retrieve.csv",
    #     "5_learningrate_4.csv": "5_learningrate_4_retrieve.csv",
    # }
    # tablelist = {
    #     "5_drate_1.csv": "5_drate_1_retrieve.csv",
    #     "5_drate_2.csv": "5_drate_2_retrieve.csv",
    #     "5_drate_3.csv": "5_drate_3_retrieve.csv",
    #     "5_drate_4.csv": "5_drate_4_retrieve.csv",
    # }
    # tablelist = {
    #     "5_decay_1.csv": "5_decay_1_retrieve.csv",
    #     "5_decay_2.csv": "5_decay_2_retrieve.csv",
    #     "5_decay_3.csv": "5_decay_3_retrieve.csv",
    #     "5_decay_4.csv": "5_decay_4_retrieve.csv",
    # }
    # tablelist = {
    #     "5_momentum_1.csv": "5_momentum_1_retrieve.csv",
    #     "5_momentum_2.csv": "5_momentum_2_retrieve.csv",
    #     "5_momentum_3.csv": "5_momentum_3_retrieve.csv",
    #     "5_momentum_4.csv": "5_momentum_4_retrieve.csv",
    # }
    #tablelist = {
    #     "overfit_batchsize_epochs_combination_1.csv": "overfit_batchsize_epochs_combination_1_retrieve.csv",
    #     "overfit_batchsize_L2_combination_1.csv": "overfit_batchsize_L2_combination_1_retrieve.csv",
    #     "overfit_batchsize_learningrate_combination_1.csv": "overfit_batchsize_learningrate_combination_1_retrieve.csv",
    #     "overfit_batchsize_dropout_combination_1.csv": "overfit_batchsize_dropout_combination_1_retrieve.csv",
    #     "overfit_epochs_L2_combination_1.csv": "overfit_epochs_L2_combination_1_retrieve.csv",
    #     "overfit_epochs_learningrate_combination_1.csv": "overfit_epochs_learningrate_combination_1_retrieve.csv",
    #     "overfit_epochs_dropout_combination_1.csv": "overfit_epochs_dropout_combination_1_retrieve.csv",
    #     "overfit_L2_learningrate_combination_1.csv": "overfit_L2_learningrate_combination_1_retrieve.csv",
    #     "overfit_L2_dropout_combination_1.csv": "overfit_L2_dropout_combination_1_retrieve.csv",
        #"overfit_dropout_learningrate_combination_1.csv": "overfit_learningrate_dropout_combination_1_retrieve.csv",
     #}


        # retrieve_columns(originaltablePath="DNM-RF/stage1/mergedresult/240/" + item,
        #                  parameterList=["ml_classifier_name","host_name","running_time1(average sec)","parameters_and_values", "mean_test_auc",
        #                                 "mean_train_auc", "percent_auc_diff"],
        #                  outputPath="DNM-RF/stage1/mergedresult/240/" + tablelist[item],
        #                  ifDeleteNull=False)
        #Jiang test below (2021.8.9)
        # retrieve_columns(originaltablePath="DNM/stage1/results/" + item,
        #          parameterList=["ml_classifier_name","host_name","running_time1(average sec)","parameters_and_values", "mean_test_auc",
        #                         "mean_train_auc", "percent_auc_diff"],
        #          outputPath="testing/" + tablelist[item],
        #          ifDeleteNull=False)
        # retrieve_columns(originaltablePath="DNM/stage1/results/5 year/" + item,
        #          parameterList=["ml_classifier_name","host_name","running_time1(average sec)","parameters_and_values", "mean_test_auc","mean_train_auc", "percent_auc_diff"],
        #          outputPath="DNM/stage1/retrieve/" + tablelist[item],
        #          ifDeleteNull=False)
        # retrieve_columns(originaltablePath="C:/Users/CHX37/PycharmProjects/keras/DNM/stage1/results/5 year/" + item,
        #          parameterList=["ml_classifier_name","host_name","running_time1(average sec)","parameters_and_values", "mean_test_auc",
        #                         "mean_train_auc", "percent_auc_diff"],
        #          outputPath="DNM/stage1/results/" + tablelist[item],
        #          ifDeleteNull=False)