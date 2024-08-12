class LogicProcessor:
    def __init__(self):
        self.logical_forms = {
            ('all', 'X', 'are', 'Y'): lambda X, Y: f"forall {X} (implies {X} {Y})",
            ('some', 'X', 'are', 'Y'): lambda X, Y: f"exists {X} (and {X} {Y})",
            ('none', 'X', 'are', 'Y'): lambda X, Y: f"forall {X} (not (implies {X} {Y}))",
            ('some', 'X', 'are', 'not', 'Y'): lambda X, Y: f"exists {X} (and {X} (not {Y}))",
            ('all', 'X', 'is', 'Y'): lambda X, Y: f"implies {X} {Y}",
            ('all', 'X', 'is', 'a', 'Y'): lambda X, Y: f"implies {X} {Y}",
            ('X', 'is', 'Y'): lambda X, Y: f"{X} is {Y}",
            ('X', 'is', 'a', 'Y'): lambda X, Y: f"{X} is a {Y}",
        }

    def clean_tokens(self, tokens):
        return [token for token in tokens if token not in ['of', 'the', 'a', 'an']]

    def tokenize(self, statement):
        tokens = statement.lower().split()
        tokens = self.clean_tokens(tokens)

        # Assume "All" if no explicit quantifier is present
        if tokens[0] not in ['all', 'some', 'none']:
            tokens.insert(0, 'all')

        return tokens

    def match_logical_form(self, tokens):
        for form, logic_func in self.logical_forms.items():
            if self.match_pattern(tokens, form):
                X = tokens[1]  # Adjusted for individual statements
                Y = tokens[-1]
                return logic_func(X, Y)
        return None

    def match_pattern(self, tokens, form):
        if len(tokens) != len(form):
            return False
        for token, expected in zip(tokens, form):
            if expected == 'X' or expected == 'Y':
                continue
            if token != expected:
                return False
        return True

    def validate_premise(self, premise):
        tokens = self.tokenize(premise)
        logic = self.match_logical_form(tokens)
        if logic is None:
            print(f"[ERROR] Syntax error in premise: '{premise}'")
        else:
            print(f"[INFO] Validated premise: '{premise}' -> {logic}")
        return logic

    def validate_argument(self, premises, conclusion):
        print(f"Validating premises and conclusion:")
        for premise in premises:
            print(f"Validating premise: {premise}")
            valid_premise = self.validate_premise(premise)
            if valid_premise is None:
                print(f"[ERROR] Failed to validate premise: '{premise}'")
                return "Error in premises parsing."
        valid_conclusion = self.validate_premise(conclusion)
        if valid_conclusion:
            return f"Conclusion is valid: {conclusion}"
        else:
            return f"Invalid conclusion: {conclusion}"

def load_arguments_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
        if len(lines) < 2:
            return None, None, "File must contain at least one premise and one conclusion."
        premises = lines[:-1]  # All lines except the last are premises
        conclusion = lines[-1]  # The last line is the conclusion
        return premises, conclusion, None
    except FileNotFoundError:
        return None, None, f"File not found: {file_path}"
    except Exception as e:
        return None, None, f"Error reading file: {str(e)}"

def main(file_path):
    processor = LogicProcessor()
    premises, conclusion, error = load_arguments_from_file(file_path)
    if error:
        print(error)
    else:
        result = processor.validate_argument(premises, conclusion)
        print(result)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python logic_processor_file.py <file_path>")
    else:
        main(sys.argv[1])
