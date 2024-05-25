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
    def __init__(self, idx, file_path, P_input_region, P_output_region) -> None:
        self.idx = idx
        self.file_path = file_path
        self.P_input_region = P_input_region
        self.P_output_region = P_output_region

        # NLane is contrary to PLane
        self.N_input_region = P_output_region
        self.N_output_region = P_input_region

    # get the data of the transition point
    # 根据region, 判断经过这个收费站给这个region的车辆的变化量
    def get_data(self, date, hour, region):
        """
        date: the date of the data
        hour: the hour of the data
        region: 
        """

        # 首先判断这个region是不是在
        _data = pd.read_csv(self.file_path)
        _data = _data[_data['date'] == date]
        _data = _data[_data['hour'] == hour]
        return _data
        


class Region:#
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



# 因为数据的相关原因, 实际上不是很清楚PLane和NLane代表的方向.
# 尽量采取以下的规则, 
# 对于横向的道路, P代表的是从西到东, N代表的是从东边到西边
# 对于纵向的道路, P代表的是从北到南, N代表的是从南到北
# 对于从西北到东南的那条主干道, P代表的是从西北到东南, N代表的是从东南到西北



# 601 还是有用的, 它实际上也对应了一条道路.
# 1 -> 5
CCS_601 = ContinuousCountStation(idx=601,
                                    file_path='data/2023-data/2023-Station-601.csv',
                                    P_input_region=5,
                                    P_output_region=1)

# 7 -> 3
CCS_626 = ContinuousCountStation(idx=626, 
                                 file_path='data/2023-data/2023-Station-626.csv', 
                                 P_input_region=3, 
                                 P_output_region=7)

# 3 -> 4
CCS_632 = ContinuousCountStation(idx=632,
                                    file_path='data/2023-data/2023-Station-632.csv',
                                    P_input_region=4,
                                    P_output_region=3)

# 6-> 2
CCS_635 = ContinuousCountStation(idx=635,
                                    file_path='data/2023-data/2023-Station-635.csv',
                                    P_input_region=2,
                                    P_output_region=6)

# 618 作为内点, 其实也不用
# CCS_618 = ContinuousCountStation(idx=618,
#                                     file_path='data/2023-data/2023-Station-618.csv',
#                                     P_input_region=None,
#                                     P_output_region=None)

# 1 -> 2
CCS_643 = ContinuousCountStation(idx=643,
                                    file_path='data/2023-data/2023-Station-643.csv',
                                    P_input_region = 2,
                                    P_output_region = 1)

# 4 -> 8
CCS_645 = ContinuousCountStation(idx=645,
                                    file_path='data/2023-data/2023-Station-645.csv',
                                    P_input_region=8,
                                    P_output_region=4)

# 4-> 8
CCS_647 = ContinuousCountStation(idx=647,
                                    file_path='data/2023-data/2023-Station-647.csv',
                                    P_input_region=8,
                                    P_output_region=4)


CCS_648 = ContinuousCountStation(idx=648, 
                                 file_path='data/2023-data/2023-Station-648.csv', 
                                 P_input_region=2, 
                                 P_output_region=3)

# 1 -> 4
CCS_656 = ContinuousCountStation(idx=656,
                                    file_path='data/2023-data/2023-Station-656.csv',
                                    P_input_region=4,
                                    P_output_region=1)

# 2-> 4
CCS_658 = ContinuousCountStation(idx=658,
                                    file_path='data/2023-data/2023-Station-658.csv',
                                    P_input_region=4,
                                    P_output_region=2)

CCS_662 = ContinuousCountStation(idx=662,
                                    file_path='data/2023-data/2023-Station-662.csv',
                                    P_input_region=3,
                                    P_output_region=2)


# 4 -> 7
CCS_671 = ContinuousCountStation(idx=671,
                                    file_path='data/2023-data/2023-Station-671.csv',
                                    P_input_region=8,
                                    P_output_region=4)

CCS_672 = ContinuousCountStation(idx=672,
                                    file_path='data/2023-data/2023-Station-672.csv',
                                    P_input_region=4,
                                    P_output_region=2)



# 675 实际上是两个点, 既有675, 又有676
# 2 -> 1
CCS_675 = ContinuousCountStation(idx=675,
                                    file_path='data/2023-data/2023-Station-675.csv',
                                    P_input_region=1,
                                    P_output_region=2)

# 2 - 1
CCS_676 = ContinuousCountStation(idx=676,
                                    file_path='data/2023-data/2023-Station-676.csv',
                                    P_input_region=1,
                                    P_output_region=2)
                                 
