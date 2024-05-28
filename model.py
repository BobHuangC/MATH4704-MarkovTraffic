# 在本次研究中, 我们关注的Contious Count Station 为:
# [601, 626, 632, 635, 643, 645, 647, 648, 656, 658, 662, 671, 672, 675, 676] 
import pandas as pd
import numpy as np

# 我们需要记录一个全局的表示不同区域车辆数量的列表
# current_time_traffic_amont[i][j] represents the traffic amount of the i-th region at the current time
# 0:00 - 24:00(the 0:00 of tomorrow)
current_time_traffic_amount = np.zeros(shape=(8, 25))


# 我们需要一个显式的记录不同时刻, 不同区域之间车辆转移的情况(1小时的时间粒度)
# hourly_traffic_among_regions[m][i][j] represents 
# the traffic amount from the i-th region to j-th region during the time of m:00 - m+1:00
hourly_traffic_among_regions = np.zeros(shape=(24, 8, 8))


# 我们需要记录一个全局的表示从当前时刻开始的在每个区域, 到某个时刻结束的时候在另外一个区域的车辆数量的列表
# 根据这两个列表, 我们可以计算出一个转移概率矩阵
# region_transition_amount[i][j][m][k] represents the traffic amount 
# that at the m:00 hour at the Region i
# after k hours, AKA, at the (m+k):00 hour, 
# the traffic amount at the Region j
region_transition_amount = np.zeros(shape=(8, 8, 24, 25))
# the update rule of the region_transition_amount is :
# region_transition_amount[i][j][m][k] = 
# \sum_{l=0}^{7} region_transition_amount[i][l][m][k-1] * (region_traffic_amount[l][j][m+k-1][1] / current_time_traffic_amount[l][m+k-1])
# the rule of calculating region_transition_amount: first input all the cases for k=0 and k=1 then use the above rule to calculate the rest of the cases


# 我们需要记录一个全局的转移率的矩阵
# region_transition_matrix[i][j][m][k] represents the transition probability from the Region i to the Region j 
# the time of the transition is from the m:00 hour to the (m+k):00 hour
# k-step transition matrix
region_transition_matrix = np.zeros(shape=(8, 8, 24, 25))
# the update rule of the region_transition_matrix is:
# region_transition_matrix[i][j][m][k] = region_transition_amount[i][j][m][k] / current_time_traffic_amount[i][m]

region_transition_matrix_v2 = np.zeros(shape=(8, 8, 24, 25))

# Continuous Count Station 代表了一个交通流的连续计数站
# 它记录了PLane 方向的车道上的车辆的数量, 以及NLane方向的车道上的车辆的数量
# 在我们的研究中, 我们只关注那些横跨不同Region 的 CCS
class ContinuousCountStation:
    # file_path: the path of the file that contains the traffic data
    def __init__(self, idx, file_path, date, P_input_region, P_output_region) -> None:
        self.idx = idx
        self.file_path = file_path
        self.P_input_region = P_input_region
        self.P_output_region = P_output_region

        # NLane is contrary to PLane
        self.N_input_region = P_output_region
        self.N_output_region = P_input_region
        _data = pd.read_csv(self.file_path)
        self.Tdata = _data[_data['DATE'] == date]
        if len(self.Tdata) == 0:
            print('CCS idx: ', self.idx)
            print("Warning: the data for this date is not available")

    # get the data of the transition point
    # 根据region, 判断经过这个收费站给这个region的车辆的变化量
    # 分开表示， 既表示进入的车辆的数量， 又表示离开的车辆的数量
    def get_traffic_flow(self, hour, region_idx):
        """
        date: the date of the data
        hour: the hour of the data
        region: 
        """
        assert(region_idx == self.P_input_region or region_idx == self.P_output_region)
        if region_idx != self.P_input_region and region_idx != self.P_output_region:
            print(f'Warning: the region {region_idx} is not related to the CCS {self.idx}')
            return 0
        
        # traffic flow 对于该region的变化量分为两方面
        # 一方面是进入这个region的车辆的数量
        # 另一方面是离开这个region的车辆的数量
        if region_idx == self.P_input_region:
            _tmp_input_data = self.Tdata[self.Tdata['LANE'].str.startswith('P')]
            _tmp_input = _tmp_input_data['H' + str(hour).zfill(2) + '00'].sum()
            _tmp_output_data = self.Tdata[self.Tdata['LANE'].str.startswith('N')]
            _tmp_output = _tmp_output_data['H' + str(hour).zfill(2) + '00'].sum()
        else:
            _tmp_input_data = self.Tdata[self.Tdata['LANE'].str.startswith('N')]
            _tmp_input = _tmp_input_data['H' + str(hour).zfill(2) + '00'].sum()
            _tmp_output_data = self.Tdata[self.Tdata['LANE'].str.startswith('P')]
            _tmp_output = _tmp_output_data['H' + str(hour).zfill(2) + '00'].sum()
        return _tmp_input, _tmp_output
            

class Region:#
    # Region 有一个idx, 还有一个string的名字
    # relatedCSS 表示和当前Region相关的CSS
    def __init__(self, idx, name, relatedCSSs, initial_traffic_amount):
        self.idx = idx
        self.name = name
        self.relatedCSSs = relatedCSSs
        
        # initialization of the traffic amount of the region
        global current_time_traffic_amount
        current_time_traffic_amount[self.idx - 1][0] = initial_traffic_amount
        print('The initial traffic amount of Region ', self.idx, ' is ', initial_traffic_amount)

        # update the traffic number
        for _hour in range(24):
            current_time_traffic_amount[self.idx - 1][_hour + 1] = current_time_traffic_amount[self.idx - 1][_hour] + self.getRegionTrafficChange(_hour)

        global region_transition_amount
        for _hour in range(24):
            region_transition_amount[self.idx - 1][self.idx - 1][_hour][0] = current_time_traffic_amount[self.idx - 1][_hour]
            # 0 hour 内到other region的转移量自然是0, 不用初始化
        
        global hourly_traffic_among_regions
        for begin_hour in range(24):
            # 获取一个小时内的转移量的这个函数是正确的
            _tmp_one_hour_transition = self.getTransitionAmount2RegionOneHour(begin_hour)
            for _region_idx in range(8):
                region_transition_amount[self.idx - 1][_region_idx][begin_hour][1] = _tmp_one_hour_transition[_region_idx]
                hourly_traffic_among_regions[begin_hour][self.idx - 1][_region_idx] = _tmp_one_hour_transition[_region_idx]

    # 获得第hour个小时到第hour+1个小时之间的车辆数量的变化量
    def getRegionTrafficChange(self, hour):
        traffic_change = 0
        for _css in self.relatedCSSs:
            _tmp_input, _tmp_output = _css.get_traffic_flow(hour, self.idx)
            traffic_change += _tmp_input
            traffic_change -= _tmp_output
        return traffic_change

    # get the traffic amount of the region by the beginning of the hourth-hour
    # 例如, hour = 0, 表示获得第0个小时开始的时候的车辆数量, 即00:00的车辆数量
    # hour = 1, 表示获得第1个小时开始的时候的车辆数量, 即01:00的车辆数量
    # hour = 24, 表示获得第24个小时开始的时候的车辆数量, 即第二天的00:00的车辆数量
    def getTrafficAmountByHour(self, hour):
        global current_time_traffic_amount
        return current_time_traffic_amount[self.idx - 1][hour]

    # def updateTrafficNumber(self):
    #     global current_time_traffic_amount
    #     for _hour in range(24):
    #         current_time_traffic_amount[self.idx - 1][_hour + 1] = current_time_traffic_amount[self.idx - 1][_hour] + self.getRegionTrafficChange(_hour)


    # 计算begin_hour:00 在当前region, begin_hour + 1:00 在其他region的车辆的数量.
    # TODO(BobHuangC): test the correctness of this function
    def getTransitionAmount2RegionOneHour(self, begin_hour):
        # 当前还是有用的, 但是只能用来算一个hour内的
        output_trans_vector = [0] * 8
        for _css in self.relatedCSSs:
            assert(self.idx == _css.P_input_region or self.idx == _css.P_output_region)
            _another_region_idx = _css.P_input_region if _css.P_input_region != self.idx else _css.P_output_region
            # for _hour in range(begin_hour, end_hour):
            #     _tmp_input, _tmp_output = _css.get_traffic_flow(_hour, self.idx)
            #     _transition += _tmp_output
            _tmp_input, _tmp_output = _css.get_traffic_flow(begin_hour, self.idx)
            output_trans_vector[_another_region_idx - 1] += _tmp_output
        
        # 加入转移到自己的车辆数量
        global current_time_traffic_amount
        output_trans_vector[self.idx - 1] = current_time_traffic_amount[self.idx - 1][begin_hour] - sum(output_trans_vector)
        return output_trans_vector

    # 计算从begin_hour 到 end_hour之间 的转移概率
    # 一个列向量, 表示从自己到其他region的转移概率
    # 表示从hour:00 到 hour+1:00 的时间内从自己到其他region的转移概率
    def getTransitionMatrix2Regions(self, begin_hour, end_hour):
        # 8 个 regions 固定
        output_trans_vector = [0] * 8
        # hour:00 时候自己内部的车辆数量
        _current_traffic_amount = self.getTrafficAmountByHour(begin_hour)
        _output_vec = self.getTransitionAmount2RegionOneHour(begin_hour)
        output_trans_vector = [x / _current_traffic_amount for x in _output_vec]
        output_trans_vector[self.idx-1] = 1 - sum(output_trans_vector)
        return output_trans_vector
    
# 因为数据的相关原因, 实际上不是很清楚PLane和NLane代表的方向.
# 尽量采取以下的规则, 
# 对于横向的道路, P代表的是从西到东, N代表的是从东边到西边
# 对于纵向的道路, P代表的是从北到南, N代表的是从南到北
# 对于从西北到东南的那条主干道, P代表的是从西北到东南, N代表的是从东南到西北
def initialize_CSSs(date):
    # 601 还是有用的, 它实际上也对应了一条道路.
    # 1 -> 5
    CCS_601 = ContinuousCountStation(idx=601,
                                        file_path='data/2023-data/2023-Station-601.csv',
                                        date=date,
                                        P_input_region=5,
                                        P_output_region=1)

    # 7 -> 3
    CCS_626 = ContinuousCountStation(idx=626, 
                                    file_path='data/2023-data/2023-Station-626.csv', 
                                    date=date,
                                    P_input_region=3, 
                                    P_output_region=7)

    # 3 -> 4
    CCS_632 = ContinuousCountStation(idx=632,
                                        file_path='data/2023-data/2023-Station-632.csv',
                                        date=date,
                                        P_input_region=4,
                                        P_output_region=3)

    # 6-> 2
    CCS_635 = ContinuousCountStation(idx=635,
                                        file_path='data/2023-data/2023-Station-635.csv',
                                        date=date,
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
                                        date=date,
                                        P_input_region = 2,
                                        P_output_region = 1)

    # 4 -> 8
    CCS_645 = ContinuousCountStation(idx=645,
                                        file_path='data/2023-data/2023-Station-645.csv',
                                        date=date,
                                        P_input_region=8,
                                        P_output_region=4)

    # 4-> 8
    CCS_647 = ContinuousCountStation(idx=647,
                                        file_path='data/2023-data/2023-Station-647.csv',
                                        date=date,
                                        P_input_region=8,
                                        P_output_region=4)

    # 3 -> 2
    CCS_648 = ContinuousCountStation(idx=648, 
                                    file_path='data/2023-data/2023-Station-648.csv', 
                                    date=date,
                                    P_input_region=2, 
                                    P_output_region=3)

    # 1 -> 4
    CCS_656 = ContinuousCountStation(idx=656,
                                        file_path='data/2023-data/2023-Station-656.csv',
                                        date=date,
                                        P_input_region=4,
                                        P_output_region=1)

    # 2-> 4
    CCS_658 = ContinuousCountStation(idx=658,
                                        file_path='data/2023-data/2023-Station-658.csv',
                                        date=date,
                                        P_input_region=4,
                                        P_output_region=2)

    CCS_662 = ContinuousCountStation(idx=662,
                                        file_path='data/2023-data/2023-Station-662.csv',
                                        date=date,
                                        P_input_region=3,
                                        P_output_region=2)

    # 4 -> 7
    CCS_671 = ContinuousCountStation(idx=671,
                                        file_path='data/2023-data/2023-Station-671.csv',
                                        date=date,
                                        P_input_region=8,
                                        P_output_region=4)

    CCS_672 = ContinuousCountStation(idx=672,
                                        file_path='data/2023-data/2023-Station-672.csv',
                                        date=date,
                                        P_input_region=4,
                                        P_output_region=2)

    # 675 实际上是两个点, 既有675, 又有676
    # 2 -> 1
    CCS_675 = ContinuousCountStation(idx=675,
                                        file_path='data/2023-data/2023-Station-675.csv',
                                        date=date,
                                        P_input_region=1,
                                        P_output_region=2)

    # 2 - 1
    CCS_676 = ContinuousCountStation(idx=676,
                                        file_path='data/2023-data/2023-Station-676.csv',
                                        date=date,
                                        P_input_region=1,
                                        P_output_region=2)
    
    return CCS_601, CCS_626, CCS_632, CCS_635, CCS_643,\
            CCS_645, CCS_647, CCS_648, CCS_656, CCS_658,\
            CCS_662, CCS_671, CCS_672, CCS_675, CCS_676
                                
# initialization of the CSSs and Regions
def initialize_CSSs_and_Regions(date, initials_traffic_amount_list):
    region_1_initial_traffic_amount = initials_traffic_amount_list[0]
    region_2_initial_traffic_amount = initials_traffic_amount_list[1]
    region_3_initial_traffic_amount = initials_traffic_amount_list[2]
    region_4_initial_traffic_amount = initials_traffic_amount_list[3]
    region_5_initial_traffic_amount = initials_traffic_amount_list[4]
    region_6_initial_traffic_amount = initials_traffic_amount_list[5]
    region_7_initial_traffic_amount = initials_traffic_amount_list[6]
    region_8_initial_traffic_amount = initials_traffic_amount_list[7]
    CCS_601, CCS_626, CCS_632, CCS_635, CCS_643,\
            CCS_645, CCS_647, CCS_648, CCS_656, CCS_658,\
            CCS_662, CCS_671, CCS_672, CCS_675, CCS_676 = initialize_CSSs(date=date)
    # initialization of Regions
    # Region1 基本可以认为是Highland, UT, USA
    Region_1  = Region(idx=1, name='Region_1', 
                            relatedCSSs=[CCS_601, CCS_643, CCS_656, CCS_675, CCS_676], 
                            initial_traffic_amount=region_1_initial_traffic_amount)

    # Region 2 + Region 3 可以认为是Lehi, UT, USA
    # 因此可以认为两者平分Lehi
    Region_2  = Region(idx=2, name='Region_2', 
                            relatedCSSs=[CCS_635, CCS_643, CCS_648, CCS_658, CCS_662, CCS_672, CCS_675, CCS_676],
                            initial_traffic_amount=region_2_initial_traffic_amount)
    Region_3  = Region(idx=3, name='Region_3', 
                            relatedCSSs=[CCS_626, CCS_632, CCS_648, CCS_662],
                            initial_traffic_amount=region_3_initial_traffic_amount)

    # Region 4 可以认为是 American Fork, UT, USA + Pleasant Grove, UT, USA
    Region_4 = Region(idx=4, name='Region_4', 
                            relatedCSSs=[CCS_632, CCS_645,  CCS_647, CCS_656, CCS_658, CCS_671, CCS_672],
                            initial_traffic_amount=region_4_initial_traffic_amount)

    # Region 5本身是一个山区, 估一个数字
    Region_5 = Region(idx=5, name='Region_5', 
                            relatedCSSs=[CCS_601],
                            initial_traffic_amount=region_5_initial_traffic_amount)

    # Region 6 可以认为是Salt Lake City, UT, USA
    Region_6 = Region(idx=6, name='Region_6', 
                            relatedCSSs=[CCS_635],
                            initial_traffic_amount=region_6_initial_traffic_amount)
    Region_7 = Region(idx=7, name='Region_7', 
                            relatedCSSs=[CCS_626, ],
                            initial_traffic_amount=region_7_initial_traffic_amount)
    Region_8 = Region(idx=8, name='Region_8', 
                            relatedCSSs=[CCS_645,  CCS_647, CCS_671],
                            initial_traffic_amount=region_8_initial_traffic_amount)
    return CCS_601, CCS_626, CCS_632, CCS_635, CCS_643,\
            CCS_645, CCS_647, CCS_648, CCS_656, CCS_658,\
            CCS_662, CCS_671, CCS_672, CCS_675, CCS_676,\
            Region_1, Region_2, Region_3, Region_4, Region_5, Region_6, Region_7, Region_8


# 调用这个函数的契机是在所有的Region都初始化好之后
def initialize_region_transition_amount():
    global region_transition_amount
    # 因此这时候k=0和k=1的region_transition_amount是已经初始化好的
    for _begin_region_idx in range(8):
        for _end_region_idx in range(8):
            for _begin_hour in range(24):
                for _k in range(2, 25):
                    # _begin_hour = 0 , _k max = 24, thus, max(_begin_hour + _k) = 24
                    if _begin_hour + _k >= 25:
                        continue
                    _tmp_sum = 0
                    for _l in range(8):
                        _tmp_sum += \
                            region_transition_amount[_begin_region_idx][_l][_begin_hour][_k-1] * \
                                (region_transition_amount[_l][_end_region_idx][_begin_hour + _k - 1][1] / current_time_traffic_amount[_l][(_begin_hour + _k - 1) ])
                    region_transition_amount[_begin_region_idx][_end_region_idx][_begin_hour][_k] = _tmp_sum

                    
# 调用这个函数的契机是在region_transition_amount已经初始化好之后
def initialize_region_transition_matrix():
    global region_transition_matrix
    for _begin_region_idx in range(8):
        for _end_region_idx in range(8):
            for _begin_hour in range(24):
                for _k in range(25):
                    if _begin_hour + _k >= 25:
                        continue
                    region_transition_matrix[_begin_region_idx][_end_region_idx][_begin_hour][_k] =\
                    region_transition_amount[_begin_region_idx][_end_region_idx][_begin_hour][_k] / current_time_traffic_amount[_begin_region_idx][_begin_hour]


     
# v2 of building region_transition_matrix
def initialize_region_transition_matrix_v2():
    # 根据region_transition_amount, current_time_traffic_amount, 来初始化k=1的情况, 
    # 然后根据k=1的情况, 来推导 k = 2 的情况, 以此类推
    global region_transition_matrix_v2
    for _begin_region_idx in range(8):
        for _begin_hour in range(24):
            region_transition_matrix_v2[_begin_region_idx][_begin_region_idx][_begin_hour][0] = 1

    for _begin_region_idx in range(8):
        for _end_region_idx in range(8):
            for _begin_hour in range(24):
                region_transition_matrix_v2[_begin_region_idx][_end_region_idx][_begin_hour][1] = \
                region_transition_amount[_begin_region_idx][_end_region_idx][_begin_hour][1] /\
                    current_time_traffic_amount[_begin_region_idx][_begin_hour]

    for _begin_region_idx in range(8):
        for _end_region_idx in range(8):
            for _begin_hour in range(24):
                for _k in range(2, 25):
                    if _begin_hour + _k >= 25:
                        continue
                    _tmp_sum = 0
                    for _l in range(8):
                        _tmp_sum += \
                            region_transition_matrix_v2[_begin_region_idx][_l][_begin_hour][_k-1] * \
                                (region_transition_matrix_v2[_l][_end_region_idx][_begin_hour + _k - 1][1])
                    region_transition_matrix_v2[_begin_region_idx][_end_region_idx][_begin_hour][_k] = _tmp_sum
