from src import biprop as bp
import numpy as np


votes = [[123,  45, 815],
         [912, 714, 414],
         [312, 255, 215],]
party_names  = ['A', 'B' , 'C'  ]
region_names = ['I', 'II', 'III']
e = bp.Election(votes, party_names=party_names, region_names=region_names)
party_seats  = e.upper_apportionment(total_seats=20, which='parties')
region_seats = e.upper_apportionment(total_seats=20, which='regions')

if np.any(party_seats!=[5, 11, 4]):
    raise ValueError(f'Expected party_seats to be [5, 11, 4] but received {party_seats}.')
if np.any(region_seats!=[7, 5, 8]):
    raise ValueError(f'Expected region_seats to be [7, 5, 8] bur received {region_seats}.')

seats = e.lower_apportionment()

if np.any(seats != [[1, 0, 4],
                    [4, 4, 3],
                    [2, 1, 1]]):
    raise ValueError(f'Calculated seats array does not match expected value.')

e2 = bp.Election(votes, party_names=party_names, region_names=region_names, total_seats=20)

try:
    seats2 = e2.biproportional_apportionment()
    raise RuntimeError('Expected a ValueError but did not trigger any errors.')
except ValueError:
    pass

seats2 = e2.biproportional_apportionment(party_seats=np.round, region_seats=np.round)

if np.any(seats2 != [[1, 0, 4],
                     [4, 4, 3],
                     [2, 1, 1]]):
    raise ValueError(f'Calculated seats array does not match expected value.')


if __name__=='__main__':


    print('\nend')