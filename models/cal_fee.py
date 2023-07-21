# encoding: utf-8
import sys
sys.path.append("../")
import os
import pandas as pd
import models.parse as parse
from config.config import Config
import pretty_errors
# 获取当前环境下用户名
def get_user():
    return os.environ.get("USER")


def fee_cal_use_pd(part_info,data):
    # 计算每条作业的费用 新增gpu_fee、cpu_fee两列
    for index, row in data.iterrows():
        # 获取作业所在的队列
        part = row['Partition']
        # 获取作业的cpu核时 gpu核时
        cpu_core_time = row['cpu']
        gpu_core_time = row['gpu']
        try:
            # 计算费用 保留5位小数
            cpu_fee = round(cpu_core_time / 3600 * part_info[part]['cpu_price'], 5)
            gpu_fee = round(gpu_core_time / 3600 * part_info[part]['gpu_price'], 5)
            # 将费用添加到data中
            data.loc[index, 'cpu_fee'] = cpu_fee
            data.loc[index, 'gpu_fee'] = gpu_fee
        except:
            pass
    return data

def fee_cal_groupby(part_info,data):
    # 根据组分类统计
    group_fee = data.groupby(['Group']).sum()
    # 新增一列total_fee
    group_fee['total_fee'] = group_fee['cpu_fee'] + group_fee['gpu_fee']
    # 保留5位小数
    group_fee = group_fee.round(5)
    print(group_fee)
    return group_fee

def fee(export_bool):
    user = get_user()
    # 获取part_info
    part_info = Config().part_info

    # 获取作业信息
    data = parse.parse_sacctdata()
    # 筛选JobID 、User 、Partition 、AllocCPUS 、time_span、cpu 、gpu
    data = data[['JobID', 'User', 'Group', 'Partition', 'time_span', 'cpu', 'gpu']]

    # 获取作业信息
    if export_bool:
        if user == 'root':
            fee_data  =  fee_cal_use_pd(part_info,data)
            groupby_fee = fee_cal_groupby(part_info,fee_data)
            # 保存到两个csv文件中
            fee_data.to_csv('/tmp/all_user_fee_data.csv',index=False)
            groupby_fee.to_csv('/tmp/all_user_fee_data_groupby.csv',index=True)
            return "所有用户费用导出至/tmp/all_user_fee_data.csv ,分组统计导出至/tmp/all_user_fee_data_groupby.csv"
        else:
            data = data[data['User'] == user]
            fee_data  =  fee_cal_use_pd(part_info,data)
            fee_data.to_csv('/tmp/{}_fee_data.csv'.format(user),index=False)
            return "{}用户费用导出至/tmp/{}_fee_data.csv".format(user,user)
    else:
        data = data[data['User'] == user]
        fee_data  =  fee_cal_use_pd(part_info,data)
        # 分类统计
        fee_data = fee_data.groupby(['User', 'Partition']).sum()
        print("尊敬的 {} 用户您好!".format(user))
        total_fee_list = []
        for part in part_info:
            try:
                cpu_fee = fee_data.loc[(user, part), 'cpu_fee']
                gpu_fee = fee_data.loc[(user, part), 'gpu_fee']
                total_fee_list.append(cpu_fee + gpu_fee)
                # 保留5位小数
                print("{}队列消耗的cpu核时为:{}s, 费用为:{}元; gpu核时为:{}s, 费用为:{}元".format(part, fee_data.loc[(user, part), 'cpu'], round(cpu_fee, 5), fee_data.loc[(user, part), 'gpu'], round(gpu_fee, 5)))
            except:
                pass
        # 计算总费用 保留5位小数
        total_fee = round(sum(total_fee_list), 5)
        return  "总费用为:{}元".format(total_fee)

    
if __name__ == '__main__':
    print(fee(1))
