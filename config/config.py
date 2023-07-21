# encoding: utf-8
import sys,yaml,os
sys.path.append("../")

BASE_DIR = os.path.dirname(__file__)
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "config.yaml")


class Config(object):
    def __init__(self):
        self.config = yaml.load(open(CONFIG_FILE_PATH, "r", encoding="utf-8"), Loader=yaml.FullLoader)
        
        # sacct_raw_data_path 路径
        self.sacct_raw_data_path = self.config["sacct_raw_data_path"]

        # 遍历part_info 中的所有part中name、gpu_price 、cpu_price ,并且将其存入嵌套的dict中
        self.part_info = {}
 
        for part in self.config["part_info"]:
            name = part["part"]["name"]
            gpu_price = part["part"]["gpu_price"]
            cpu_price = part["part"]["cpu_price"]

            self.part_info[name] = {}
            self.part_info[name]["gpu_price"] = gpu_price
            self.part_info[name]["cpu_price"] = cpu_price


if __name__ == "__main__":
    print(Config().part_info)
    # {'hyper': {'gpu_price': 25, 'cpu_price': 5}, 'super': {'gpu_price': 20, 'cpu_price': 3}, '88cores': {'gpu_price': 0, 'cpu_price': 1}}
