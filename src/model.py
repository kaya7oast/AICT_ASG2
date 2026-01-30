from pgmpy.models import BayesianNetwork  

model = BayesianNetwork([               
    ('Weather', 'Demand'),     # W -> P
    ('Time', 'Demand'),        # T -> P
    ('Day', 'Demand'),         # D -> P
    ('Demand', 'Crowding'),    # P -> C
    ('Service', 'Crowding'),   # S -> C
    ('Mode', 'Crowding')       # M -> C
])