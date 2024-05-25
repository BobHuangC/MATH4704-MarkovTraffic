# 在本次研究中, 我们关注的Contious Count Station, 
# 666/1674: this point is ambiguous
# 675
# 643
# 1673
# 662
# 648

# 626
# 618
# 632
# 672
# 658

# 601
# 656

# 671
# 645
# 647

import pandas as pd
# Transition Point 指的是车辆流量的连续计数站
class ContinuousCountStation:
    # file_path: the path of the file that contains the traffic data
    def __init__(self, idx, file_path) -> None:
        self.idx = idx
        self.file_path = file_path

    # get the data of the transition point
    def get_data(self, date, hour, direction):
        """
        date: the date of the data
        hour: the hour of the data
        direction: the direction of the data
        for the direction, we denote that 
        P means the traffic flow from the west to the east / north to the south
        N means the traffic flow from the east to the west / south to the north
        """
        _data = pd.read_csv(self.file_path)
        _data = _data[_data['date'] == date]
        _data = _data[_data['hour'] == hour]
        return _data
        


class Region:
    # Region 有一个idx, 还有一个string的名字
    # input_CCS 代表这些CCS的数据中的P车道相关的数据是进入这个Region的数据, N车道相关的数据是离开这个Region的数据
    # output_CCS 代表这些CCS的数据中的P车道相关的数据是离开这个Region的数据, N车道相关的数据是进入这个Region的数据
    def __init__(self, idx, name):
                #  input_CCSs : list[ContinuousCountStation], 
                #  output_CCSs : list[ContinuousCountStation]) -> None:
        self.idx = idx
        self.name = name
        # self.input_CCSs = input_CCSs
        # self.output_CCSs = output_CCSs
    
    # 传入所有的CCS, 根据CCS的数据, 
    def get_CCS_direction(self, CCSs):
        pass
        self.input_CCSs = []
        self.output_CCSs = []    

class TrafficNetwork:
    def __init__(self):
        self.regions = []
        self.transition_points  = []

    def transition():
        pass



# transition point represents the continuous Count Station
# in fact the coutinous count of the traffic flow represents the transition mount of different states