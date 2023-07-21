# encoding: utf-8
import os,sys,pandas as pd
sys.path.append("../")
from config.config import Config
part_info = Config().part_info
sacct_raw_data_path = Config().sacct_raw_data_path

# 获取当前环境下用户名
def get_user():
    return os.environ.get("USER")
'''
解析sacctdata文件 转化成dataframe类型 29ms
'''
def parse_sacctdata():
    columns = ['JobID', 'User', 'Group', 'Partition', 'Start', 'End', 'WorkDir', 'JobName', 'ReqTRES', 'State']
    # 将sacctdata文件读取到dataframe中
    line_list = []
    with open(sacct_raw_data_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # 每行数据用| 分割  去除每行数据中最后一个元素的 "\n 
            line = line.split('|')[:-1]
            line_list.append(line)
    # 将line_list转换为dataframe
    data_df = pd.DataFrame(line_list[1:], columns=columns)
    # 将Start、End列转换为datetime类型 replace将None值和Unknown值替换为NaT
    data_df['Start'] = pd.to_datetime(data_df['Start'].replace('None', pd.NaT).replace('Unknown', pd.NaT))
    data_df['End'] = pd.to_datetime(data_df['End'].replace('None', pd.NaT).replace('Unknown', pd.NaT))
    # 新增一列 time_span 为End - Start , 单位为秒 ，如果Start、End为NaT 则time_span为0， 只保留整数部分
    data_df['time_span'] = (data_df['End'] - data_df['Start']).dt.total_seconds().fillna(0).astype(int)
    # 拆分ReqTRES列，得到cpu、gpu 列
    data_df['cpu'] = data_df['ReqTRES'].str.split(',').str[1].str.split('=').str[1].fillna(0).astype(int)
    data_df['gpu'] = data_df['ReqTRES'].str.extract(r'gres/gpu=(\d+)').fillna(0).astype(int)
    # 删除 ReqTRES 列
    data_df.drop('ReqTRES', axis=1, inplace=True)
    return data_df

'''
计算给定用户、分区的cpu、gpu核时 45ms
'''
def calculate_user_core_time(user, partition):
    data_df = parse_sacctdata()
    # 筛选出给定用户、分区的time_span、cpu和gpu列
    user_df = data_df[(data_df['User'] == user) & (data_df['Partition'] == partition)][['time_span', 'cpu', 'gpu']]
    # 计算核时
    cpu_core_time = (user_df['time_span'] * user_df['cpu']).sum() 
    gpu_core_time = (user_df['time_span'] * user_df['gpu']).sum() 
    return cpu_core_time, gpu_core_time
    
'''
获取给定用户作业信息
'''
def get_job_info(export_bool):
    user = get_user()
    data_df = parse_sacctdata()
    # 如果user为root用户，返回所有用户的作业信息
    if user == 'root':
        if export_bool:# 如果为真，则导出所有用户的作业信息
            data_df.to_csv('/tmp/all_user_job_info.csv', index=False)
            return "导出所有用户的作业信息成功！保存至 /tmp/all_user_job_info.csv"
        else:
            return data_df.to_string(index=False)
    else:
        if export_bool:# 如果为真，则导出用户的作业信息
            user_df = data_df[data_df['User'] == user]
            user_df.to_csv('/tmp/{}_job_info.csv' .format(user), index=False)
            return "导出用户 {} 的作业信息成功！保存至 /tmp/{}_job_info.csv" .format(user, user)
        else:
            user_df = data_df[data_df['User'] == user]
            return user_df.to_string(index=False)


if __name__ == '__main__':
    
    # 获取用户核时
    user = "kusuan009"
    partition = "hyper"
    export_bool = 1

    
    # print(calculate_user_core_time(user, partition))
    print(get_job_info(user, export_bool))