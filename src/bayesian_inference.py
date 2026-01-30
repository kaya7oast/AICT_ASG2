from pgmpy.inference import VariableElimination
from src.model import model
from src.bayesian_cpds import cpd_weather, cpd_time, cpd_day, cpd_service, cpd_mode, cpd_demand, cpd_crowding

def run_bayesian_analysis():
    print("\n" + "="*80 + "\nPART 2: BAYESIAN NETWORK ANALYSIS (Chase's Work)\n" + "="*80)
    if not model.get_cpds():
        model.add_cpds(cpd_weather, cpd_time, cpd_day, cpd_service, cpd_mode, cpd_demand, cpd_crowding)
    try:
        assert model.check_model()
        print("✓ Model validated.")
    except Exception as e:
        print(f"Model Error: {e}")
        return

    inference = VariableElimination(model)
    
    scenarios = [
        (1, "Rainy Evening (Today)", {'Weather': 'Rainy', 'Time': 'Evening', 'Service': 'Reduced', 'Mode': 'Today'}),
        (2, "Disrupted Service (Today)", {'Service': 'Disrupted', 'Mode': 'Today'})
    ]
    
    for num, desc, ev in scenarios:
        print(f"\nScenario {num}: {desc}")
        res = inference.query(variables=['Crowding'], evidence=ev)
        print(res)