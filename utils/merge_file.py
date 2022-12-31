import pandas as pd

def merge(file_paths, keep_index, output_path):
    """
    this functions is used to combine multiple files with same format into one merge file
    the input is a list of file paths which need to be combined,
    the output will be a csv file with merged data
    """
    names = pd.read_csv(file_paths[0]).columns
    df = pd.concat([pd.read_csv(f, header=None, skiprows=[0], names=names) for f in file_paths], ignore_index=True)
    print(len(df))
    if keep_index == True:
        df.to_csv(output_path)
    else:
        df.to_csv(output_path, index=False)

if __name__ == "__main__":
    # file_paths = ['../DNM-RF/stage3-5/15_year_stage3-5_160_summary_ip96.csv',
    #               '../DNM-RF/stage3-5/15_year_stage3-5_160_summary_ip141.csv',
    #               '../DNM-RF/stage3-5/15_year_stage3-5_160_summary_ip163.csv',
    #               '../DNM-RF/stage3-5/15_year_stage3-5_160_summary_ip164.csv',
    #               '../DNM-RF/stage3-5/15_year_stage3-5_160_summary_mac.csv',]#input path
    # output_path = '../DNM-RF/stage3-5/15_year_stage3-5_160_summary_merge.csv'
    # file_paths = ['../DNM-RF/stage3-5/15_year_stage3-5_180_desktop.csv',
    #               '../DNM-RF/stage3-5/15_year_stage3-5_180_ip96.csv',
    #               '../DNM-RF/stage3-5/15_year_stage3-5_180_ip141.csv',]#input path
    # output_path = '../DNM-RF/stage3-5/15_year_stage3-5_180_merge.csv'
    file_paths = ['../DNM-RF/stage3-5/15_year_stage3-5_100.csv',
                  '../DNM-RF/stage3-5/15_year_stage3-5_120.csv',
                  '../DNM-RF/stage3-5/15_year_stage3-5_140.csv',
                  '../DNM-RF/stage3-5/15_year_stage3-5_160.csv',
                  '../DNM-RF/stage3-5/15_year_stage3-5_180.csv',
                  ]
    output_path ='../DNM-RF/stage3-5/15_year_stage3-5.csv'
    keep_index = False
    merge(file_paths, output_path, keep_index)

