from tracemalloc import start


class Automaton():

    def __init__(self, config_file):
        self.config_file = config_file   
        self.graph = {} 
        self.start_state = ""
        self.final_states = [] 
            
    def validate(self):
        """Return a Boolean

        Returns true if the config file is valid,
        and raises a ValidationException if the config is invalid.
        """
        with open(self.config_file, "r") as f:
            text = f.read()
        
        try:
            config = self.parse(text)
        except:
            raise Exception("ValidationException")
        
        start_state = ""
        final_states = []
        for state in config["States"]:
            if "S" in config["States"][state] and start_state != "":
                raise Exception("ValidationException: states")
            if "S" in config["States"][state]:
                start_state = state
            if "F" in config["States"][state]:
                final_states.append(state)

        for transition in config["Transitions"]:
            if transition[0] not in config["States"] or transition[2] not in config["States"] or transition[1] not in config["Sigma"]:
                raise Exception("ValidationException: transitions")

        self.start_state = start_state
        self.final_states = final_states
        self.graph = self.create_graph(config)

        return True

    def accepts_input(self, input_str):
        """Return a Boolean

        Returns True if the input is accepted,
        and it returns False if the input is rejected.
        """
        pass


    def read_input(self, input_str):
        """Return the automaton's final configuration
        
        If the input is rejected, the method raises a
        RejectionException.
        """
        pass

    def parse(self, input_str):
        """
        Parse the input string and returns the tokens in a dictionary
        If there is any invalid syntax an exception occurs.
        """
        config = {"Sigma": [], "States": {}, "Transitions":[]}
        stages = {"Sigma": False, "States": False, "Transitions": False}
        stage = None
        for i, line in enumerate(input_str.split("\n")):
            
            # line = line.replace(" ", "")
            if line[0] == '#':    # comment line (skip it)
                continue

            try:
                tokens = self.get_tokens(line)
            except:
                raise Exception(f"InvalidInput: line {i + 1}")
               
            if len(tokens) == 0:
                continue

            if stage == None:
                if len(tokens) != 2 or tokens[1] != ':' or tokens[0] not in stages.keys() or stages[tokens[0]]:
                    raise Exception(f"InvalidInput: line {i + 1}")
                stage = tokens[0]
                stages[tokens[0]] = True
            elif tokens[0] == "End":
                if len(tokens) > 1:
                    raise Exception(f"InvalidInput: line {i + 1}")
                stage = None
            else:
                if stage == "Sigma":
                    if len(tokens) > 1:
                        raise Exception(f"InvalidInput: line {i + 1}")
                    config[stage].append(tokens[0])
                elif stage == "States":
                    if tokens[0] == ",":
                         raise Exception(f"InvalidInput: line {i + 1}")
                    if len(tokens) == 1 and tokens[0] not in config[stage]:
                        config[stage][tokens[0]] = (None, None)
                    elif len(tokens) == 3 and tokens[1] == ',' and tokens[2] in "SF" and tokens[0] not in config[stage]:
                        config[stage][tokens[0]] = (tokens[2], None)
                    elif len(tokens) == 5 and tokens[1] == ',' and tokens[3] == ',' and tokens[2] in "SF" and tokens[4] in 'SF' and tokens[2] != tokens[4] and tokens[0] not in config[stage]:
                        config[stage][tokens[0]] = (tokens[2], tokens[4])
                    else:
                        raise Exception(f"InvalidInput: line {i + 1}")
                else:
                    if len(tokens) == 5 and tokens[0] != ',' and tokens[2] != ',' and tokens[1] == ',' and tokens[3] == ',':
                        config[stage].append((tokens[0], tokens[2], tokens[4]))
                    else:
                        raise Exception(f"InvalidInput: line {i + 1}")
        return config


    def get_tokens(self, s):
        """
        Return a tuple with tokens found in string s
        """
        tokens = []
        token = []
        for char in s:
            if char.isalnum() or char == "_":
                token.append(char)
            elif not char.isalnum() and char != "_" and len(token) > 0:
                tokens.append("".join(token))
                token = []
            if char == ":" or char == ",":
                tokens.append(char)
            if not char.isalnum() and char != "_" and char not in ",: ":
                raise Exception(f"InvalidSyntax")
        if len(token) > 0:
            tokens.append("".join(token))
        return tuple(tokens)

    def create_graph(self, config):
        graph = {}
        for transition in config["Transitions"]:
            edge = (transition[2], transition[1])
            try:
                if edge not in graph[transition[0]]:
                    graph[transition[0]].append(edge)
            except:
                graph[transition[0]] = [edge]
        return graph
    

if __name__ == "__main__":
    a = Automaton('input.txt')
    print(a.validate())
