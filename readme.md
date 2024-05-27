# MATH-4704 MarkovTraffic

This repo is BobHuangC's project homework for MATH-4704.

### Specific model method

对Continous Couting Station主要进行建模.
CCS要确定自己的PLane对应的Region和NLane对应的Region.


现在比较痛苦的一个点就是搞不懂CCS的具体含义. 与具体的车道的关系.

#### vehicles / per person

https://en.wikipedia.org/wiki/List_of_U.S._states_by_vehicles_per_capita
Utah 的人均车辆数量数据来源

#### population

Salt Lake City Population https://datacommons.org/place/geoId/4967000?utm_medium=explore&mprop=count&popt=Person&hl=en

https://www2.census.gov/programs-surveys/popest/tables



https://datacommons.org/place/geoId/4944320

population of Lehi

Lehi的差不多是 2区和3区的重叠
人口 2022: 84373

Highland 差不多是 1区的重叠

19,902

American Fork + Pleasant Grove 差不多是 4区的重叠

American Fork 人口 2022: 37,268
Pleasant Grove 人口 2022: 37,630

5区: Heber City 人口 2022: 17,865
5区相对比较远, 所有转移应该会比较少.

6区: Bluffdale : 19080
Herriman:  59,179 
Draper:  50,731


7区: Eagle Moutain 54,149 

8区: Lindon 11,704 
Orem 95,910 
Vineyard  14,535



# description of the project


上面的数据申请比较麻烦

下面是Utah官网的数据, 数据本身可能不是很好评估, 但是总算是获取比较方便.
https://udot.utah.gov/connect/business/traffic-data/traffic-statistics/

https://drive.google.com/drive/folders/1ZYy-WkICLOp1482vwEbTc5UvLItbWs4y

Station

H0100 Represent the 0-th hour of the day.

1. 可以做相应的预测, 例如可以提取三个小时, 也就是较短的时间, 然后预测马尔科夫稳定的状态的情况.

2. 可以研究道路可能的拥堵情况.

结论: 可以根据状态, 进行马尔科夫链的预测, 从而预测交通拥堵的情况.

节点之间的拓扑序的位置
https://hub.arcgis.com/datasets/017ab39594bc4e37964884ac31e8bff4/explore?location=37.731961%2C-112.725309%2C6.42


(已确认)Station 指的应该是CSS Number.
route 也就是对应的route.

可以选择部分数据来进行处理即可

例如可以选择
Salt Lake City的数据, 也就是Salt Lake City 相关的节点来进行计算即可.

<!-- West Vally City 的数据还是较大, 不是特别方便处理. -->

<!-- 聚焦Salt Lake City的West Valley City的数据.

https://hub.arcgis.com/datasets/017ab39594bc4e37964884ac31e8bff4/explore?location=39.560697%2C-110.484716%2C7.40


<div align="center">
  <img width="700px" height="auto" src="assets/Utah Street.png"></a>
</div>
 -->

聚焦Salt Lake City 东南方向的一个小城的数据.

<!-- https://hub.arcgis.com/datasets/017ab39594bc4e37964884ac31e8bff4/explore?location=39.560697%2C-110.484716%2C7.40 -->


<div align="center">
  <img width="700px" height="auto" src="assets/Small City.png"></a>
</div>



街道建模:

贯穿城市的那条高速路, 可以算作一个整体的状态.

与城市的具体状态之间可以有相应的转换.

可以拓展思路, 不一定要以道路中的车辆的数量作为状态, 可以以区域内部的车辆的数量作为状态.


每个收费站本质上代表的是一个转换, 从某个状态转移到另一个状态, 所以只要收费站能够封闭起来的区域, 基本上就可以看作是一个状态.

划分为8个状态, 4个内部状态, 4个外部状态.



Street: 

横向街道: (从上到下)

Timpanogos Hwy



还可以通过计算transition 的强度来判断当地的工作时间或者相应的交通通勤时间.



### future work

本次实验提出了一种基于区域之间交通流量来对交通运输进行分析的方法.

理想的建模情况应该基于街道来作为state, 相应的数据的采集可以由监控摄像头来进行采集, 但因为数据的保密性, 本次实验只能建模在较高维度的区域上, 因此我们只能建模到区域之间的交通流量.

要证明交通中的稳态基本上是没有意义的, 因为交通的昼夜时效性较强, 

但是在较短的时间内部计算还是有意义的.

用 2023 年的数据来进行建模, 当前缺失了部分数据, 就忽略不计了, 
还有部分收费站的数据, 有相应的数据, 但是数据本身也有缺陷, 例如只有某些时间的数据, 这应该代表只有对应的时间开放相应的道路.

做一定的假设, NLane是向东和向南的道路方向, PLane是向西和向北的道路方向.