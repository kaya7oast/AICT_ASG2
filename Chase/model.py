# If not installed:
# pip install pgmpy

from pgmpy.models import DiscreteBayesianNetwork

# Construct the Bayesian Network structure
model = DiscreteBayesianNetwork([
    ('Weather', 'Demand'),     # W → P
    ('Time', 'Demand'),        # T → P
    ('Day', 'Demand'),         # D → P
    ('Demand', 'Crowding'),    # P → C
    ('Service', 'Crowding'),   # S → C
    ('Mode', 'Crowding')       # M → C
])

if __name__ == "__main__":
    print("Nodes in the model:")
    print(model.nodes())
    
    print("\nEdges in the model:")
    print(model.edges())
