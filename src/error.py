

class Error():

    def __init__(self, analysis_program, errors=None):
        self.analysis_program = analysis_program
        if errors is None:
            self.errors = dict()
            self.errors["relative"] = dict()
            self.errors["absolute"] = dict()
        else:
            self.errors = errors

    def __repr__(self):
        return 'Error(analysis_program={}, errors={})'.format(self.analysis_program, self.errors)

    def add_relative_error(self, domain, value):
        self.errors["relative"][domain] = value

    def add_absolute_error(self, domain, value):
        self.errors["absolute"][domain] = value
