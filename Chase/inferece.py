from pgmpy.inference import VariableElimination
from model import model
from bayesian_cpds import cpd_weather, cpd_time, cpd_day, cpd_service, cpd_mode, cpd_demand, cpd_crowding

# Add CPDs to the model
model.add_cpds(cpd_weather, cpd_time, cpd_day, cpd_service, cpd_mode, cpd_demand, cpd_crowding)

# Validate the model
assert model.check_model(), "Model validation failed!"
print("✓ Model validated successfully\n")

# Create inference object
inference = VariableElimination(model)

# Helper function to print results
def print_scenario(scenario_num, description, evidence, result):
    print(f"{'='*80}")
    print(f"SCENARIO {scenario_num}: {description}")
    print(f"{'='*80}")
    print(f"Evidence: {evidence}")
    print(f"\nCrowding Probabilities:")
    for state in ['Low', 'Medium', 'High']:
        prob = result.values[list(result.state_names['Crowding']).index(state)]
        print(f"  {state:8s}: {prob:.4f} ({prob*100:.2f}%)")
    print()

# =============================================================================
# SCENARIO 1: Rainy evening + reduced service (Today Mode)
# =============================================================================
evidence1 = {
    'Weather': 'Rainy',
    'Time': 'Evening',
    'Service': 'Reduced',
    'Mode': 'Today'
}
result1 = inference.query(variables=['Crowding'], evidence=evidence1)
print_scenario(1, "Rainy evening + reduced service (Today)", evidence1, result1)

# =============================================================================
# SCENARIO 2: Clear morning weekday + normal service (Today Mode)
# =============================================================================
evidence2 = {
    'Weather': 'Clear',
    'Time': 'Morning',
    'Day': 'Weekday',
    'Service': 'Normal',
    'Mode': 'Today'
}
result2 = inference.query(variables=['Crowding'], evidence=evidence2)
print_scenario(2, "Clear morning weekday + normal service (Today)", evidence2, result2)

# =============================================================================
# SCENARIO 3: Weekend afternoon + normal service (Today Mode)
# =============================================================================
evidence3 = {
    'Day': 'Weekend',
    'Time': 'Afternoon',
    'Service': 'Normal',
    'Mode': 'Today'
}
result3 = inference.query(variables=['Crowding'], evidence=evidence3)
print_scenario(3, "Weekend afternoon + normal service (Today)", evidence3, result3)

# =============================================================================
# SCENARIO 4: Disrupted service (Today Mode)
# =============================================================================
evidence4 = {
    'Service': 'Disrupted',
    'Mode': 'Today'
}
result4 = inference.query(variables=['Crowding'], evidence=evidence4)
print_scenario(4, "Disrupted service (Today)", evidence4, result4)

# =============================================================================
# SCENARIO 5a: TODAY MODE - Clear evening + normal service (BASELINE)
# =============================================================================
evidence5a = {
    'Weather': 'Clear',
    'Time': 'Evening',
    'Service': 'Normal',
    'Mode': 'Today'
}
result5a = inference.query(variables=['Crowding'], evidence=evidence5a)
print_scenario("5a", "TODAY MODE: Clear evening + normal service (BASELINE)", evidence5a, result5a)

# =============================================================================
# SCENARIO 5b: FUTURE MODE - Clear evening + normal service (TELe+CRL)
# =============================================================================
evidence5b = {
    'Weather': 'Clear',
    'Time': 'Evening',
    'Service': 'Normal',
    'Mode': 'Future'
}
result5b = inference.query(variables=['Crowding'], evidence=evidence5b)
print_scenario("5b", "FUTURE MODE: Clear evening + normal service (TELe+CRL)", evidence5b, result5b)

# =============================================================================
# COMPARISON: Scenario 5a vs 5b
# =============================================================================
print(f"{'='*80}")
print(f"COMPARISON: Today vs Future Mode (Clear evening + normal service)")
print(f"{'='*80}")
print(f"{'State':<15} {'Today Mode':>15} {'Future Mode':>15} {'Change':>15}")
print(f"{'-'*80}")
for state in ['Low', 'Medium', 'High']:
    idx = list(result5a.state_names['Crowding']).index(state)
    today_prob = result5a.values[idx]
    future_prob = result5b.values[idx]
    change = future_prob - today_prob
    print(f"{state:<15} {today_prob:>14.4f} {future_prob:>14.4f} {change:>+14.4f}")
print()

# =============================================================================
# SCENARIO 6a: TODAY MODE - Rainy evening + reduced service (BASELINE)
# =============================================================================
evidence6a = {
    'Weather': 'Rainy',
    'Time': 'Evening',
    'Service': 'Reduced',
    'Mode': 'Today'
}
result6a = inference.query(variables=['Crowding'], evidence=evidence6a)
print_scenario("6a", "TODAY MODE: Rainy evening + reduced service (BASELINE)", evidence6a, result6a)

# =============================================================================
# SCENARIO 6b: FUTURE MODE - Rainy evening + reduced service (TELe+CRL)
# =============================================================================
evidence6b = {
    'Weather': 'Rainy',
    'Time': 'Evening',
    'Service': 'Reduced',
    'Mode': 'Future'
}
result6b = inference.query(variables=['Crowding'], evidence=evidence6b)
print_scenario("6b", "FUTURE MODE: Rainy evening + reduced service (TELe+CRL)", evidence6b, result6b)

# =============================================================================
# COMPARISON: Scenario 6a vs 6b
# =============================================================================
print(f"{'='*80}")
print(f"COMPARISON: Today vs Future Mode (Rainy evening + reduced service)")
print(f"{'='*80}")
print(f"{'State':<15} {'Today Mode':>15} {'Future Mode':>15} {'Change':>15}")
print(f"{'-'*80}")
for state in ['Low', 'Medium', 'High']:
    idx = list(result6a.state_names['Crowding']).index(state)
    today_prob = result6a.values[idx]
    future_prob = result6b.values[idx]
    change = future_prob - today_prob
    print(f"{state:<15} {today_prob:>14.4f} {future_prob:>14.4f} {change:>+14.4f}")
print()

# =============================================================================
# SCENARIO 7a: TODAY MODE - Clear morning weekday + disrupted service
# =============================================================================
evidence7a = {
    'Weather': 'Clear',
    'Time': 'Morning',
    'Day': 'Weekday',
    'Service': 'Disrupted',
    'Mode': 'Today'
}
result7a = inference.query(variables=['Crowding'], evidence=evidence7a)
print_scenario("7a", "TODAY MODE: Clear morning weekday + disrupted service", evidence7a, result7a)

# =============================================================================
# SCENARIO 7b: FUTURE MODE - Clear morning weekday + disrupted service
# =============================================================================
evidence7b = {
    'Weather': 'Clear',
    'Time': 'Morning',
    'Day': 'Weekday',
    'Service': 'Disrupted',
    'Mode': 'Future'
}
result7b = inference.query(variables=['Crowding'], evidence=evidence7b)
print_scenario("7b", "FUTURE MODE: Clear morning weekday + disrupted service", evidence7b, result7b)

# =============================================================================
# COMPARISON: Scenario 7a vs 7b
# =============================================================================
print(f"{'='*80}")
print(f"COMPARISON: Today vs Future Mode (Clear morning weekday + disrupted service)")
print(f"{'='*80}")
print(f"{'State':<15} {'Today Mode':>15} {'Future Mode':>15} {'Change':>15}")
print(f"{'-'*80}")
for state in ['Low', 'Medium', 'High']:
    idx = list(result7a.state_names['Crowding']).index(state)
    today_prob = result7a.values[idx]
    future_prob = result7b.values[idx]
    change = future_prob - today_prob
    print(f"{state:<15} {today_prob:>14.4f} {future_prob:>14.4f} {change:>+14.4f}")
print()

