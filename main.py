# encoding: utf-8
import os
import models.parse as parse
import models.cal_fee as cal_fee
from config.config import Config

def fee(export_bool):
    print(cal_fee.fee(export_bool))

def job(export_bool):
    print(parse.get_job_info(export_bool))

if __name__ == '__main__':
    # 接收命令行参数
    import sys
    # 有两个参数 一个是fee 一个是job 如果job后有参数 export 则设置export_bool为True 否则为False
    if len(sys.argv) == 1:
        fee(0)
    elif len(sys.argv) == 2:
        if sys.argv[1] == 'fee':
            fee(0)
        elif sys.argv[1] == 'job':
            job(0)
        elif sys.argv[1] == 'help' or sys.argv[1] == '-h':
            print("Usage: welcome fee [export] | welcome job [export]")
        else:
            print("请输入正确的参数2！")
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'job' and sys.argv[2] == 'export':
            job(1)
        elif sys.argv[1] == 'fee' and sys.argv[2] == 'export':
            fee(1)
        else:
            print("请输入正确的参数3！")
    else:
        print("请输入正确的参数1！")