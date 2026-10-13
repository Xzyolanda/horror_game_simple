from .rule import Rule


class RuleBook:
    def __init__(self) -> None:
        self.rules = {}

    def add_rule(self, rule: Rule) -> None:
        if rule.rule_id not in self.rules:
            self.rules[rule.rule_id] = rule
        else:
            raise ValueError("Rule already exists")

    def get_rule(self, rule_id: str) -> Rule | None:
        return self.rules.get(rule_id)

    def display_all_rules(self) -> None:
        print("Rules:")
        for rule in self.rules.values():
            print(f"{rule.rule_id}: {rule.text}")

    def display_rule(self, rule_id: str) -> None:
        rule = self.get_rule(rule_id)
        if rule:
            print(f"{rule.rule_id}: {rule.text}")
        else:
            print("Rule not found.")