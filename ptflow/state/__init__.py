class InvalidOutput(Exception):
    pass

class InvalidInput(Exception):
    pass

class GuardFail(Exception):
    pass

class StateMachine(object):

    def __str__(self):
        """ dump state machine rules """
        return {
            "places": self.places,
            "transitions": self.transitions
        }.__str__()

    def guard_test(self, label, state, guard):
        """
        a guard is valid given that an inhibitor arc
        has targeted a place with zero tokens
        """

        for _, attr in self.places.items():
            i = attr['offset']
            if (state[i] + guard[i]) < 0:
                return

        raise GuardFail(label)

    def inital_vector(self):
        """ bulid the default state """
        return [ p["initial"] for _, p in self.places.items() ]

    def transform(self, state, action, multiple=1):
        """ perform state transformation with vector addition """

        if multiple < 0:
            raise InvalidInput('invalid multiple %s' % multiple)

        if action not in self.transitions:
            raise InvalidInput('unknown action')

        t = self.transitions[action]

        for label, guard in t['guards'].items():
            self.guard_test(label, state, guard)

        out = []
        for p, attr in self.places.items():
            i = attr['offset']
            n = state[i] + t['delta'][i]*multiple 

            if n < 0:
                raise InvalidOutput("underflow state[%i] %s => %i" % (i, p, n))

            if attr["capacity"] > 0 and n > attr["capacity"]:
                raise InvalidOutput("overflow state[%i] %s => %i" % (i, p, n))

            out.append(n)

        return out, t['role']
