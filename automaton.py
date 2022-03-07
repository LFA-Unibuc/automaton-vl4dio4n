class Automaton():

    def __init__(self, config_file):
        self.config_file = config_file
        print("Hi, I'm an automaton!")

    def validate(self):
        """Return a Boolean

        Returns true if the config file is valid,
        and raises a ValidationException if the config is invalid.
        """
        with open(self.config_file, "r") as f:
            text = f.read()
        config = self.read_input(text)
        initial_state = False
        for state in config["States"]:
            if not self.accepts_input("States", state, config, initial_state):
                raise Exception("ValidationException: states")
            if "S" in state:
                initial_state = True
        for transition in config["Transitions"]:
            if not self.accepts_input("Transitions", transition, config, initial_state):
                print(transition)
                raise Exception("ValidationException: transitions")
        return True

    def accepts_input(self, input_str, key, config, initial_state):
        """Return a Boolean

        Returns True if the input is accepted,
        and it returns False if the input is rejected.
        """
        if input_str == "States":
            if "S" in config["States"][key] and initial_state:
                return False
            return True
        elif input_str == "Transitions":
            if key[0] in config["States"] and key[2] in config["States"] and key[1] in config["Sigma"]:
                return True
            return False 


    def read_input(self, input_str):
        """Return the automaton's final configuration
        
        If the input is rejected, the method raises a
        RejectionException.
        """
        config = {"Sigma": [], "States": {}, "Transitions":[]}
        stages = {"Sigma": False, "States": False, "Transitions": False}
        stage = None
        for i, line in enumerate(input_str.split("\n")):
            if line[0] == '#':    # comment line (skip it)
                continue
            tokens = self.get_tokens(line)
            if len(tokens) == 0:
                continue

            if stage == None:
                if len(tokens) != 2 or tokens[1] != ':' or tokens[0] not in stages.keys() or stages[tokens[0]]:
                    raise Exception(f"RejectionException: line {i + 1}")
                stage = tokens[0]
                stages[tokens[0]] = True
            elif tokens[0] == "End":
                if len(tokens) > 1:
                    raise Exception(f"RejectionException: line {i + 1}")
                stage = None
            else:
                if stage == "Sigma":
                    if len(tokens) > 1:
                        raise Exception(f"RejectionException: line {i + 1}")
                    config[stage].append(tokens[0])
                elif stage == "States":
                    if len(tokens) == 1 and tokens[0] not in config[stage]:
                        config[stage][tokens[0]] = (None, None)
                    elif len(tokens) == 3 and tokens[1] == ',' and tokens[2] in "SF" and tokens[0] not in config[stage]:
                        config[stage][tokens[0]] = (tokens[2], None)
                    elif len(tokens) == 5 and tokens[1] == ',' and tokens[3] == ',' and tokens[2] in "SF" and tokens[4] in 'SF' and tokens[2] != tokens[4] and tokens[0] not in config[stage]:
                        config[stage][tokens[0]] = (tokens[2], tokens[4])
                    else:
                        raise Exception(f"RejectionException: line {i + 1}")
                else:
                    if len(tokens) == 5 and  tokens[1] == ',' and tokens[3] == ',':
                        config[stage].append((tokens[0], tokens[2], tokens[4]))
                    else:
                        raise Exception(f"RejectionException: line {i + 1}")
        return config


    def get_tokens(self, s):
        """
        Return a tuple with tokens found in string s
        """
        tokens = []
        token = []
        for char in s:
            if char.isalnum():
                token.append(char)
            elif not char.isalnum() and len(token) > 0:
                tokens.append("".join(token))
                token = []
            if not char.isalnum() and char != ' ':
                tokens.append(char)
        if len(token) > 0:
            tokens.append("".join(token))
        return tuple(tokens)

if __name__ == "__main__":
    a = Automaton('input.txt')
    print(a.validate())
