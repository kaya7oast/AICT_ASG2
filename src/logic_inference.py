"""
Logical Inference Module for ChangiLink AI
Implements resolution-based inference for MRT service rules and advisory consistency checking.
"""

from itertools import combinations
from typing import List, Set, Dict, Tuple, Optional


class Clause:
    """Represents a clause in CNF (Conjunctive Normal Form) - a disjunction of literals."""
    
    def __init__(self, literals: Set[str]):
        self.literals = frozenset(literals)
    
    def __repr__(self):
        return "{" + " OR ".join(sorted(self.literals)) + "}"
    
    def __eq__(self, other):
        return isinstance(other, Clause) and self.literals == other.literals
    
    def __hash__(self):
        return hash(self.literals)
    
    def is_empty(self):
        return len(self.literals) == 0
    
    def is_unit(self):
        return len(self.literals) == 1
    
    def is_tautology(self):
        for lit in self.literals:
            if lit.startswith('~'):
                pos_lit = lit[1:]
            else:
                pos_lit = lit
                neg_lit = '~' + lit
                if neg_lit in self.literals:
                    return True
        return False


class KnowledgeBase:
    """Knowledge base containing MRT operational rules in CNF."""
    
    def __init__(self, mode="TODAY"):
        self.mode = mode
        self.clauses: Set[Clause] = set()
        self.rules_documentation = []
        self._initialize_rules()
    
    def _initialize_rules(self):
        """Initialize the knowledge base with operational rules."""
        
        # Rule 1: Station Operational Integrity
        self.add_rule(
            "~maintenance_TM OR ~operational_TM",
            "RULE-1a: Tanah Merah cannot be both under maintenance and operational"
        )
        self.add_rule(
            "~maintenance_EXPO OR ~operational_EXPO",
            "RULE-1b: Expo cannot be both under maintenance and operational"
        )
        self.add_rule(
            "~maintenance_CGA OR ~operational_CGA",
            "RULE-1c: Changi Airport cannot be both under maintenance and operational"
        )
        
        # Rule 2: Line Operational Dependencies
        self.add_rule(
            "~line_operational_EWL OR operational_TM OR operational_CGA",
            "RULE-2: EWL operational requires Tanah Merah OR Changi Airport operational"
        )
        
        # Rule 3: Transfer Point Requirements
        self.add_rule(
            "~route_uses_transfer_TM OR operational_TM",
            "RULE-3a: Routes transferring at Tanah Merah require it to be operational"
        )
        self.add_rule(
            "~route_uses_transfer_EXPO OR operational_EXPO",
            "RULE-3b: Routes transferring at Expo require it to be operational"
        )
        
        # Rule 4: Systems Integration Work Impact (FUTURE mode specific)
        if self.mode == "FUTURE":
            self.add_rule(
                "~systems_integration_EWL_to_TEL OR maintenance_TM",
                "RULE-4a: EWL-to-TEL integration implies Tanah Merah under maintenance"
            )
            self.add_rule(
                "~systems_integration_EWL_to_TEL OR maintenance_EXPO",
                "RULE-4b: EWL-to-TEL integration implies Expo under maintenance"
            )
            self.add_rule(
                "~systems_integration_EWL_to_TEL OR maintenance_CGA",
                "RULE-4c: EWL-to-TEL integration implies Changi Airport under maintenance"
            )
        
        # Rule 5: Service Adjustment Requirements
        self.add_rule(
            "~maintenance_TM OR service_adjustment_TM",
            "RULE-5a: Maintenance at Tanah Merah requires service adjustments"
        )
        self.add_rule(
            "~maintenance_EXPO OR service_adjustment_EXPO",
            "RULE-5b: Maintenance at Expo requires service adjustments"
        )
        
        # Rule 6: Alternative Route Availability
        self.add_rule(
            "~primary_route_TM_CGA_unavailable OR alternative_route_available",
            "RULE-6: If Tanah Merah-Changi Airport route unavailable, alternative must exist"
        )
        
        # Rule 7: New Station Operational Requirements (FUTURE mode)
        if self.mode == "FUTURE":
            self.add_rule(
                "~operational_T5 OR TEL_extension_complete",
                "RULE-7a: T5 operational requires TEL extension completion"
            )
            self.add_rule(
                "~operational_T5 OR CRL_extension_complete",
                "RULE-7b: T5 operational requires CRL extension completion"
            )
        
        # Rule 8: Line Conversion Constraint (FUTURE mode)
        if self.mode == "FUTURE":
            self.add_rule(
                "~line_operational_EWL_airport OR ~line_operational_TEL_airport",
                "RULE-8: EWL and TEL cannot both operate on airport stretch during conversion"
            )
        
        # Rule 9: Interchange Station Requirements (FUTURE mode)
        if self.mode == "FUTURE":
            self.add_rule(
                "~interchange_T5 OR TEL_serves_T5",
                "RULE-9a: T5 interchange requires TEL service"
            )
            self.add_rule(
                "~interchange_T5 OR CRL_serves_T5",
                "RULE-9b: T5 interchange requires CRL service"
            )
        
        # Rule 10: Route Validity Constraints
        self.add_rule(
            "~valid_route OR ~passes_through_maintenance",
            "RULE-10: Valid routes cannot pass through stations under maintenance"
        )
        
        # Rule 11: Peak Hour Service Requirements
        self.add_rule(
            "~peak_hour OR ~reduced_service_EWL",
            "RULE-11: Peak hours prohibit reduced service on EWL main line"
        )
        
        # Rule 12: Emergency Bypass (TODAY mode)
        if self.mode == "TODAY":
            self.add_rule(
                "operational_EXPO OR route_via_TM",
                "RULE-12: If Expo not operational, route must go via Tanah Merah"
            )
    
    def add_rule(self, clause_str: str, description: str):
        """Add a rule to the knowledge base."""
        literals = set()
        for lit in clause_str.split('OR'):
            lit = lit.strip()
            if lit:
                literals.add(lit)
        
        clause = Clause(literals)
        if not clause.is_tautology():
            self.clauses.add(clause)
            self.rules_documentation.append({
                'clause': clause_str,
                'description': description,
                'cnf': clause
            })
    
    def add_fact(self, fact: str):
        """Add a fact (unit clause) to the knowledge base."""
        clause = Clause({fact})
        self.clauses.add(clause)
    
    def add_clause(self, clause: Clause):
        """Add a clause object directly to the knowledge base."""
        if not clause.is_tautology():
            self.clauses.add(clause)
    
    def get_rules_documentation(self) -> List[Dict]:
        """Return documentation of all rules in the knowledge base."""
        return self.rules_documentation


class ResolutionEngine:
    """Resolution-based inference engine for propositional logic."""
    
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
    
    def resolve(self, c1: Clause, c2: Clause) -> Optional[Clause]:
        """Perform resolution between two clauses."""
        for lit1 in c1.literals:
            if lit1.startswith('~'):
                comp_lit = lit1[1:]
            else:
                comp_lit = '~' + lit1
            
            if comp_lit in c2.literals:
                new_literals = (c1.literals | c2.literals) - {lit1, comp_lit}
                resolvent = Clause(new_literals)
                
                if not resolvent.is_tautology():
                    return resolvent
        
        return None
    
    def resolution_refutation(self, query_clauses: Set[Clause], max_iterations=1000) -> Tuple[bool, List[str]]:
        """Perform resolution refutation to check if query is entailed by KB."""
        clauses = self.kb.clauses | query_clauses
        new = set()
        trace = []
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            clause_list = list(clauses)
            pairs = combinations(clause_list, 2)
            
            for c1, c2 in pairs:
                resolvent = self.resolve(c1, c2)
                
                if resolvent is not None:
                    if resolvent.is_empty():
                        trace.append(f"Iteration {iteration}: Empty clause derived - CONTRADICTION")
                        return True, trace
                    
                    if resolvent not in clauses and resolvent not in new:
                        new.add(resolvent)
                        trace.append(f"Iteration {iteration}: Derived {resolvent}")
            
            if not new:
                trace.append(f"Iteration {iteration}: No new clauses - Cannot prove query")
                return False, trace
            
            clauses |= new
            new = set()
        
        trace.append(f"Max iterations ({max_iterations}) reached")
        return False, trace
    
    def check_route_validity(self, route_facts: List[str]) -> Tuple[bool, List[str], List[str]]:
        """Check if a proposed route is valid under current KB rules."""
        temp_kb = KnowledgeBase(self.kb.mode)
        temp_kb.clauses = self.kb.clauses.copy()
        
        for fact in route_facts:
            temp_kb.add_fact(fact)
        
        engine = ResolutionEngine(temp_kb)
        is_inconsistent, trace = engine.resolution_refutation(set(), max_iterations=500)
        
        violations = []
        if is_inconsistent:
            violations = self._identify_violations(route_facts)
        
        return not is_inconsistent, violations, trace
    
    def check_advisory_consistency(self, advisories: List[str]) -> Tuple[bool, List[str]]:
        """Check if a set of service advisories is internally consistent with KB."""
        temp_kb = KnowledgeBase(self.kb.mode)
        temp_kb.clauses = self.kb.clauses.copy()
        
        for advisory in advisories:
            temp_kb.add_fact(advisory)
        
        engine = ResolutionEngine(temp_kb)
        is_inconsistent, trace = engine.resolution_refutation(set(), max_iterations=500)
        
        return not is_inconsistent, trace
    
    def _identify_violations(self, facts: List[str]) -> List[str]:
        """Identify which rules are violated by given facts."""
        violations = []
        
        for rule_doc in self.kb.get_rules_documentation():
            clause = rule_doc['cnf']
            
            all_falsified = True
            for lit in clause.literals:
                if lit.startswith('~'):
                    pos_lit = lit[1:]
                    if pos_lit not in facts:
                        all_falsified = False
                        break
                else:
                    neg_lit = '~' + lit
                    if neg_lit not in facts:
                        all_falsified = False
                        break
            
            if all_falsified:
                violations.append(rule_doc['description'])
        
        return violations


def run_inference_scenarios(mode="TODAY"):
    """Run predefined test scenarios for the inference engine."""
    kb = KnowledgeBase(mode)
    engine = ResolutionEngine(kb)
    
    scenarios = []
    
    print(f"\n{'='*80}")
    print(f"KNOWLEDGE BASE RULES - {mode} MODE")
    print(f"{'='*80}\n")
    for i, rule in enumerate(kb.get_rules_documentation(), 1):
        print(f"{i}. {rule['description']}")
        print(f"   CNF: {rule['clause']}\n")
    
    if mode == "TODAY":
        scenarios = _get_today_scenarios()
    else:
        scenarios = _get_future_scenarios()
    
    results = []
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*80}")
        print(f"SCENARIO {i} ({mode} MODE): {scenario['name']}")
        print(f"{'='*80}")
        print(f"Description: {scenario['description']}\n")
        
        if scenario['type'] == 'route_validity':
            is_valid, violations, trace = engine.check_route_validity(scenario['facts'])
            
            print(f"Route Facts: {', '.join(scenario['facts'])}")
            print(f"\nResult: {'VALID' if is_valid else 'INVALID'}")
            
            if violations:
                print(f"\nViolations Detected:")
                for v in violations:
                    print(f"  - {v}")
            
            results.append({
                'scenario': scenario['name'],
                'type': 'Route Validity',
                'mode': mode,
                'valid': is_valid,
                'violations': violations
            })
        
        elif scenario['type'] == 'advisory_consistency':
            is_consistent, trace = engine.check_advisory_consistency(scenario['advisories'])
            
            print(f"Advisories: {', '.join(scenario['advisories'])}")
            print(f"\nResult: {'CONSISTENT' if is_consistent else 'INCONSISTENT'}")
            
            results.append({
                'scenario': scenario['name'],
                'type': 'Advisory Consistency',
                'mode': mode,
                'consistent': is_consistent
            })
    
    return results


def _get_today_scenarios():
    """Define test scenarios for TODAY mode."""
    return [
        {
            'name': 'Valid Route via Operational Stations',
            'type': 'route_validity',
            'description': 'Route using Tanah Merah and Changi Airport, both operational',
            'facts': [
                'operational_TM',
                'operational_CGA',
                'route_uses_transfer_TM',
                'valid_route',
                'line_operational_EWL'
            ]
        },
        {
            'name': 'Invalid Route - Station Under Maintenance',
            'type': 'route_validity',
            'description': 'Route tries to use Tanah Merah which is under maintenance',
            'facts': [
                'maintenance_TM',
                'route_uses_transfer_TM',
                'valid_route'
            ]
        },
        {
            'name': 'Consistent Advisory - Maintenance with Service Adjustment',
            'type': 'advisory_consistency',
            'description': 'Expo under maintenance with proper service adjustments',
            'advisories': [
                'maintenance_EXPO',
                'service_adjustment_EXPO',
                '~operational_EXPO'
            ]
        },
        {
            'name': 'Inconsistent Advisory - Missing Service Adjustment',
            'type': 'advisory_consistency',
            'description': 'Station under maintenance but no service adjustment announced',
            'advisories': [
                'maintenance_TM',
                '~service_adjustment_TM'
            ]
        },
        {
            'name': 'Valid Route - Expo Down, Using TM Bypass',
            'type': 'route_validity',
            'description': 'When Expo is not operational, route correctly uses Tanah Merah',
            'facts': [
                '~operational_EXPO',
                'route_via_TM',
                'operational_TM'
            ]
        },
        {
            'name': 'Invalid Route - Peak Hour with Reduced Service',
            'type': 'route_validity',
            'description': 'Attempting reduced service during peak hours (not allowed)',
            'facts': [
                'peak_hour',
                'reduced_service_EWL'
            ]
        }
    ]


def _get_future_scenarios():
    """Define test scenarios for FUTURE mode."""
    return [
        {
            'name': 'Valid - T5 Operational with Extensions Complete',
            'type': 'route_validity',
            'description': 'T5 station operational after both TEL and CRL extensions complete',
            'facts': [
                'operational_T5',
                'TEL_extension_complete',
                'CRL_extension_complete',
                'interchange_T5',
                'TEL_serves_T5',
                'CRL_serves_T5'
            ]
        },
        {
            'name': 'Invalid - T5 Operational Without TEL Extension',
            'type': 'route_validity',
            'description': 'T5 cannot be operational if TEL extension not complete',
            'facts': [
                'operational_T5',
                '~TEL_extension_complete',
                'CRL_extension_complete'
            ]
        },
        {
            'name': 'Consistent - Systems Integration Active',
            'type': 'advisory_consistency',
            'description': 'EWL-to-TEL conversion with all affected stations under maintenance',
            'advisories': [
                'systems_integration_EWL_to_TEL',
                'maintenance_TM',
                'maintenance_EXPO',
                'maintenance_CGA',
                'service_adjustment_TM',
                'service_adjustment_EXPO'
            ]
        },
        {
            'name': 'Inconsistent - Integration Without Maintenance',
            'type': 'advisory_consistency',
            'description': 'Systems integration active but station not under maintenance',
            'advisories': [
                'systems_integration_EWL_to_TEL',
                'operational_TM',
                'maintenance_EXPO'
            ]
        },
        {
            'name': 'Invalid - Both Lines Operating During Conversion',
            'type': 'route_validity',
            'description': 'Cannot have both EWL and TEL on airport stretch simultaneously',
            'facts': [
                'line_operational_EWL_airport',
                'line_operational_TEL_airport'
            ]
        },
        {
            'name': 'Invalid - T5 Interchange Missing CRL',
            'type': 'route_validity',
            'description': 'T5 as interchange requires both TEL and CRL',
            'facts': [
                'interchange_T5',
                'TEL_serves_T5',
                '~CRL_serves_T5'
            ]
        }
    ]


if __name__ == "__main__":
    print("="*80)
    print("CHANGILINK AI - LOGICAL INFERENCE SYSTEM")
    print("Resolution-Based Service Advisory Consistency Checker")
    print("="*80)
    
    today_results = run_inference_scenarios("TODAY")
    future_results = run_inference_scenarios("FUTURE")
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"\nTODAY Mode: {len(today_results)} scenarios tested")
    print(f"FUTURE Mode: {len(future_results)} scenarios tested")
    print(f"\nTotal scenarios: {len(today_results) + len(future_results)}")
