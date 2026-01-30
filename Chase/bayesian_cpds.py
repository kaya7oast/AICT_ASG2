from pgmpy.factors.discrete import TabularCPD

# Define all Conditional Probability Distributions (CPDs)

# Weather
cpd_weather = TabularCPD(
    variable='Weather',
    variable_card=3,
    values=[[0.6], [0.3], [0.1]],
    state_names={'Weather': ['Clear', 'Rainy', 'Thunderstorms']}
)

# Time of Day
cpd_time = TabularCPD(
    variable='Time',
    variable_card=3,
    values=[[0.33], [0.33], [0.34]],
    state_names={'Time': ['Morning', 'Afternoon', 'Evening']}
)

# Day Type
cpd_day = TabularCPD(
    variable='Day',
    variable_card=2,
    values=[[0.7], [0.3]],
    state_names={'Day': ['Weekday', 'Weekend']}
)

# Service Status
cpd_service = TabularCPD(
    variable='Service',
    variable_card=3,
    values=[[0.6], [0.3], [0.1]],
    state_names={'Service': ['Normal', 'Reduced', 'Disrupted']}
)

# Network Mode
cpd_mode = TabularCPD(
    variable='Mode',
    variable_card=2,
    values=[[0.5], [0.5]],
    state_names={'Mode': ['Today', 'Future']}
)


cpd_demand = TabularCPD(
    variable='Demand',
    variable_card=3,
    values=[
        # Low
        [0.6, 0.4, 0.3, 0.4, 0.2, 0.1, 0.3, 0.2, 0.1,
         0.7, 0.5, 0.4, 0.5, 0.3, 0.2, 0.4, 0.3, 0.2],
        # Medium
        [0.3, 0.4, 0.4, 0.4, 0.4, 0.3, 0.4, 0.4, 0.3,
         0.2, 0.3, 0.4, 0.3, 0.4, 0.4, 0.4, 0.4, 0.4],
        # High
        [0.1, 0.2, 0.3, 0.2, 0.4, 0.6, 0.3, 0.4, 0.6,
         0.1, 0.2, 0.2, 0.2, 0.3, 0.4, 0.2, 0.3, 0.4]
    ],
    evidence=['Weather', 'Time', 'Day'],
    evidence_card=[3, 3, 2],
    state_names={
        'Demand': ['Low', 'Medium', 'High'],
        'Weather': ['Clear', 'Rainy', 'Thunderstorms'],
        'Time': ['Morning', 'Afternoon', 'Evening'],
        'Day': ['Weekday', 'Weekend']
    }
)

cpd_crowding = TabularCPD(
    variable='Crowding',
    variable_card=3,
    values=[
        # Low crowding: Mode changes fastest, then Service, then Demand
        [0.80, 0.85, 0.60, 0.70, 0.40, 0.50, 0.60, 0.70, 0.40, 0.50, 0.20, 0.30, 0.30, 0.40, 0.15, 0.25, 0.05, 0.15],
        # Medium crowding
        [0.15, 0.10, 0.30, 0.20, 0.40, 0.30, 0.30, 0.20, 0.40, 0.30, 0.50, 0.40, 0.40, 0.35, 0.45, 0.40, 0.35, 0.30],
        # High crowding
        [0.05, 0.05, 0.10, 0.10, 0.20, 0.20, 0.10, 0.10, 0.20, 0.20, 0.30, 0.30, 0.30, 0.25, 0.40, 0.35, 0.60, 0.55]
    ],
    evidence=['Demand', 'Service', 'Mode'],
    evidence_card=[3, 3, 2],
    state_names={
        'Crowding': ['Low', 'Medium', 'High'],
        'Demand': ['Low', 'Medium', 'High'],
        'Service': ['Normal', 'Reduced', 'Disrupted'],
        'Mode': ['Today', 'Future']
    }
)

if __name__ == "__main__":
    print("Total elements per crowding state:", cpd_crowding.values[0].size)
    print("Shape of CPD values:", cpd_crowding.values.shape)
