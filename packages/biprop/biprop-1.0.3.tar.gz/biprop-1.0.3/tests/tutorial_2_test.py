import src.biprop as bp
import numpy as np

parties = ['Thrushes',
           'Blackbirds',
           'Sparrowhawks',
           'Starlings',
           'Geese',
           'Ducks',
           'Sparrows',
           'Owls',
           'Cuckoos',
           'Waxwings',
           'Sperrlinge']
regions = ['Mercury', 'Venus', 'Earth', 'Mars', 'Jupyter',
           'Saturn', 'Uranus', 'Neptune', 'Pluto']
votes = [[    8,     0,   162,   150,   300,     7,   113,   173],
         [ 1977,  3834,  2392,  5379,   675,  3305,  2626,  4700],
         [  439,  2467,  1620,  5454,  6596,    42,  8359,  3257],
         [    0,    40,   135,  1500,  1026,   458,  3536,  2321],
         [  751,  3525,  3373,  1407,  3328,  1704,  7256,  4163],
         [    1,     4,     0,     8,    10,     4,    13,     0],
         [ 1153,  1886,  3988,    13,   134,  1171,  7834,  6980],
         [  461,  6836,  1664,  6686,  5911,   401,  7010,  7036],
         [  106,   330,   420,   213,  1165,   284,   405,  1029],
         [  425,  8269,   265,  3813,  7055,  2857,  9659,  6160],
         [   50,  8250,   517,  7910,  7583,  2601,  5305, 114040000]]

e = bp.Election(votes)
e.total_seats = 100
e.party_names = parties
try:
    e.region_names = regions
    raise RuntimeError('Expected a ValueError but did not trigger any errors.')
except ValueError:
    pass

regions.remove('Pluto')
e.region_names = regions
e.votes[-1,-1] = 11404


###############################################################################
#                                                                             #
#   Pre-apportionment phase                                                   #
#                                                                             #
###############################################################################
votes_before = e.votes[6].sum() + e.votes[-1].sum()
e.merge(party_mergers=[['Sparrows', 'Sperrlinge']])
votes_after = e.votes[6].sum()
if votes_before != votes_after:
    raise ValueError(f'Votes before merger ({votes_before}) does not match votes after ({votes_after}) merger.')
if e.parties != ['Thrushes', 'Blackbirds', 'Sparrowhawks', 'Starlings', 'Geese', 'Ducks', 'Sparrows', 'Owls', 'Cuckoos', 'Waxwings']:
    raise ValueError('party_order does match expected value.')
e.merge(party_mergers=[['Sperrlinge', 'Sparrows']])
if e.parties != ['Thrushes', 'Blackbirds', 'Sparrowhawks', 'Starlings', 'Geese', 'Ducks', 'Sperrlinge', 'Owls', 'Cuckoos', 'Waxwings']:
    raise ValueError('party_order does match expected value.')
e.merge(party_mergers=[['CAPTAIN Jack Sparrow', 'Sparrows', 'Sperrlinge']])
if e.parties != ['Thrushes', 'Blackbirds', 'Sparrowhawks', 'Starlings', 'Geese', 'Ducks', 'CAPTAIN Jack Sparrow', 'Owls', 'Cuckoos', 'Waxwings']:
    raise ValueError('party_order does match expected value.')
e.merge_parties([['Sparrows', 'Sperrlinge', 'CAPTAIN Jack Sparrow']])
if e.parties != ['Thrushes', 'Blackbirds', 'Sparrowhawks', 'Starlings', 'Geese', 'Ducks', 'Sparrows', 'Owls', 'Cuckoos', 'Waxwings']:
    raise ValueError('party_order does match expected value.')
votes_after = e.votes[6].sum()
if votes_before != votes_after:
    raise ValueError(f'Votes before merger ({votes_before}) does not match votes after ({votes_after}) merger.')


###############################################################################
#                                                                             #
#   Apportionment phase                                                       #
#                                                                             #
###############################################################################
expected_seats = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [1, 2, 1, 2, 0, 2, 1, 2],
                           [0, 1, 1, 2, 3, 0, 4, 1],
                           [0, 0, 0, 1, 0, 0, 2, 1],
                           [0, 1, 1, 1, 2, 1, 3, 2],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [1, 4, 2, 3, 4, 2, 5, 8],
                           [0, 3, 1, 3, 2, 0, 3, 3],
                           [0, 0, 0, 0, 1, 0, 0, 1],
                           [0, 4, 0, 2, 3, 1, 4, 2]])
e.biproportional_apportionment(party_seats=np.round, region_seats=np.round)
try:
    e.merge_parties(['Sparrows', 'Sperrlinge'])
    raise RuntimeError('Expected an InvalidOrderError but received none.')
except bp.InvalidOrderError:
    pass
if np.any(e.seats != expected_seats):
    raise ValueError('Calculated seats does not match expected value.')
e.reorder(party_order='seats')
if e.parties != ['Sparrows', 'Waxwings', 'Owls', 'Sparrowhawks', 'Blackbirds', 'Geese', 'Starlings', 'Cuckoos', 'Thrushes', 'Ducks']:
    raise ValueError('Reordered parties are not in the expected order.')
e.reorder(region_order='alphabetical')
if e.regions != ['Earth', 'Jupyter', 'Mars', 'Mercury', 'Neptune', 'Saturn', 'Uranus', 'Venus']:
    raise ValueError('Reordered regions are not in the expected order.')




if __name__=='__main__':
    


    print('\nend')