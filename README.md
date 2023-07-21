# slurmweb
一个致力于slurm web开发的项目
## 安装
```shell
git clone https://github.com/wehpc/slurmweb.git
```

/etc/profile中加入
```shell
alias welcome='export PYTHONIOENCODING=utf-8 && /usr/bin/python3 -u "/opt/slurmweb/welcome.py"'
``` 

contab -e 添加定时任务
```
*/10 * * * * sacct -X -a -p -S 2022-07-13 -E now --format=jobid,user,group,partition,start,end,workdir,JobName,ReqTRES,State > /opt/slurmweb/data/sacct_raw

```

## welcome 命令行
语法
```
$ welcome -h
Usage: welcome fee [export] | welcome job [export]
```

### welcome fee
查询核时、账单信息
```
test@master 16:04:05 ~ $ welcome fee
尊敬的 test 用户您好!
hyper队列消耗的cpu核时为:1.0s, 费用为:0.00139元; gpu核时为:0.0s, 费用为:0.0元
super队列消耗的cpu核时为:2.0s, 费用为:0.00166元; gpu核时为:0.0s, 费用为:0.0元
总费用为:0.00305元

```
### welcome fee export
导出 核时、账单信息
```
test@master 16:04:09 ~ $ welcome fee export
test用户费用导出至/tmp/test_fee_data.csv
```

### welcome job
查询作业信息
```
test@master 16:04:40 ~ $ welcome job
JobID  User Group Partition               Start                 End               WorkDir JobName      State  time_span  cpu  gpu
   49  test  test     super 2023-06-21 16:02:20 2023-06-21 16:02:33            /home/test   sleep  COMPLETED         13    1    0
   50  test  test     super 2023-06-21 16:03:35 2023-06-21 16:03:47  /superfile/home/test   sleep  COMPLETED         12    1    0
   51  test  test     hyper 2023-06-21 16:04:15 2023-06-21 16:04:37  /superfile/home/test   sleep  COMPLETED         22    1    0

```

### welcome job export
导出作业信息
```
test@master 16:05:35 ~ $ welcome job export
导出用户 test 的作业信息成功！保存至 /tmp/test_job_info.csv
```