from model import *
import tqdm

# 在本次研究中, 我们关注的Contentious Count Station, 
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

# load the Continuous Count Station
# CCS: Continuous Count Station
CCS_601 = ContinuousCountStation(idx=601, file_path='data/2023-data/2023-Station-601.csv')
CCS_618 = ContinuousCountStation(idx=618, file_path='data/2023-data/2023-Station-618.csv')
CCS_626 = ContinuousCountStation(idx=626, file_path='data/2023-data/2023-Station-626.csv')
CCS_632 = ContinuousCountStation(idx=632, file_path='data/2023-data/2023-Station-632.csv')
CCS_643 = ContinuousCountStation(idx=643, file_path='data/2023-data/2023-Station-643.csv')
CCS_645 = ContinuousCountStation(idx=645, file_path='data/2023-data/2023-Station-645.csv')
CCS_647 = ContinuousCountStation(idx=647, file_path='data/2023-data/2023-Station-647.csv')
CCS_648 = ContinuousCountStation(idx=648, file_path='data/2023-data/2023-Station-648.csv')
CCS_656 = ContinuousCountStation(idx=656, file_path='data/2023-data/2023-Station-656.csv')
CCS_658 = ContinuousCountStation(idx=658, file_path='data/2023-data/2023-Station-658.csv')
CCS_662 = ContinuousCountStation(idx=662, file_path='data/2023-data/2023-Station-662.csv')
CCS_671 = ContinuousCountStation(idx=671, file_path='data/2023-data/2023-Station-671.csv')
CCS_672 = ContinuousCountStation(idx=672, file_path='data/2023-data/2023-Station-672.csv')
CCS_675 = ContinuousCountStation(idx=675, file_path='data/2023-data/2023-Station-675.csv')
CCS_1673 = ContinuousCountStation(idx=1673, file_path='data/2023-data/2023-Station-1673.csv')

# load the regions
region_1 = Region(idx=1, 
                    name='InnerCityNorthEast',
                    input_CCSs=[CCS_601, CCS_618, CCS_626, CCS_632], 
                    output_CCSs=[CCS_643])

region_2 = Region(idx=2,
                    name='InnerCityNorthWest',
                    input_CCSs=[CCS_643],
                    output_CCSs=[CCS_645, CCS_647])

region_3 = Region(idx=3,
                    name='InnerCitySouthWest',
                    input_CCSs=[CCS_645, CCS_647],
                    output_CCSs=[CCS_648, CCS_656])

region_4 = Region(idx=4,
                    name='InnerCitySouthEast',
                    input_CCSs=[CCS_648, CCS_656],
                    output_CCSs=[CCS_658, CCS_662])

region_5 = Region(idx=5,
                    name='OuterCityNorthEast',
                    input_CCSs=[CCS_662, CCS_658],
                    output_CCSs=[CCS_671])

region_6 = Region(idx=6,
                    name='OuterCityNorthWest',
                    input_CCSs=[CCS_671],
                    output_CCSs=[CCS_675])

region_7 = Region(idx=7,
                    name='OuterCitySouthWest',
                    input_CCSs=[CCS_675],
                    output_CCSs=[CCS_1673])

region_8 = Region(idx=8,
                    name='OuterCitySouthEast',
                    input_CCSs=[CCS_1673],
                    output_CCSs=[])

