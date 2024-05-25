# 在本次研究中, 我们关注的Contious Count Station 为:
# [601, 626, 632, 635, 643, 645, 647, 648, 656, 658, 662, 671, 672, 675, 676] 

# 我们研究一天之内的数据, 所以在程序的开始加载当日的所有数据.
Date = '2023-01-03'

import pandas as pd

# Continuous Count Station 代表了一个交通流的连续计数站
# 它记录了PLane 方向的车道上的车辆的数量, 以及NLane方向的车道上的车辆的数量
# 在我们的研究中, 我们只关注那些横跨不同Region 的 CCS
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
        _data = pd.read_csv(self.file_path)
        self.Tdata = _data[_data['DATE'] == Date]
        if len(self.Tdata) == 0:
            print("Error: the data for this date is not available")

    # get the data of the transition point
    # 根据region, 判断经过这个收费站给这个region的车辆的变化量
    def get_traffic_flow(self, hour, region_idx):
        """
        date: the date of the data
        hour: the hour of the data
        region: 
        """
        if region_idx != self.P_input_region and region_idx != self.P_output_region:
            print(f'Error: the region {region_idx} is not related to the CCS {self.idx}')
            return 0
        
        # traffic flow 对于该region的变化量分为两方面
        # 一方面是进入这个region的车辆的数量
        # 另一方面是离开这个region的车辆的数量
        if region_idx == self.P_input_region:
            _tmp_input_data = self.Tdata[self.Tdata['LANE'].str.startswith('P')]
            traffic_amount = _tmp_input_data['H' + str(hour).zfill(2) + '00'].sum()
            _tmp_output_data = self.Tdata[self.Tdata['LANE'].str.startswith('N')]
            traffic_amount -= _tmp_output_data['H' + str(hour).zfill(2) + '00'].sum()
        else:
            _tmp_input_data = self.Tdata[self.Tdata['LANE'].str.startswith('N')]
            traffic_amount = _tmp_input_data['H' + str(hour).zfill(2) + '00'].sum()
            _tmp_output_data = self.Tdata[self.Tdata['LANE'].str.startswith('P')]
            traffic_amount -= _tmp_output_data['H' + str(hour).zfill(2) + '00'].sum()
        return traffic_amount
            


        


class Region:#
    # Region 有一个idx, 还有一个string的名字
    # relatedCSS 表示和当前Region相关的CSS
    def __init__(self, idx, name, relatedCSSs, initial_traffic_amount):
        self.idx = idx
        self.name = name
        self.relatedCSSs = relatedCSSs
        self.traffic_amount = initial_traffic_amount
    
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
                                 
