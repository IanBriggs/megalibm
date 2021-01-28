

from utils.various import parse_float
from utils.logging import Logger


logger = Logger()




class Domain():

    def __init__(self, lower, upper):
        self.lower = parse_float(lower)
        self.upper = parse_float(upper)
        assert(self.lower <= self.upper)
        self.normals = [(self.lower, self.upper)]
        self.denormals = list()


    def k(self, k):
        difference = self.upper - self.lower
        kdifference = k*difference
        return Domain(self.lower+kdifference, self.upper+kdifference)


    def add_denormal(self, lower, upper):
        lower = parse_float(lower)
        upper = parse_float(upper)
        assert(lower <= upper)
        assert(self.lower <= lower)
        assert(upper <= self.upper)

        # Take this region out of the normals
        old_normals = self.normals
        self.normals = list()
        for l,u in old_normals:
            # Check enclosing
            if lower <= l and u <= upper:
                continue
            # Check half enclosing
            if lower == l and upper < u:
                self.normals.append((upper, u))
                continue
            if upper == u and l < lower:
                self.normals.append((l, lower))
                continue
            # Check half overlaps
            if l <= lower and lower <= u:
                self.normals.append((l,lower))
                continue
            if l <= upper and upper <= u:
                self.normals.append((upper,u))
                continue
            # No overlap
            self.normals.append((l, u))

        # Place the region in denormals
        self.denormals.append((lower, upper))


    def full_domain(self):
        return (self.lower, self.upper)


    def normal_domains(self):
        return self.normals


    def denormal_domains(self):
        return self.denormals
