

from utils.logging import Logger


logger = Logger()




class Error():

    def __init__(self, analysis_program, normal_errors=None, denormal_errors=None):
        self.analysis_program = analysis_program
        self.normal_errors = normal_errors or dict()
        self.denormal_errors = denormal_errors or dict()


    def __repr__(self):
        return 'Error(analysis_program={}, normal_errors={}, denormal_errors={})'.format(self.analysis_program, self.normal_errors, self.denormal_errors)

    def add_normal_error(self, domain, absolute_error, relative_error):
        self.normal_errors[domain] = (absolute_error, relative_error)


    def add_denormal_error(self, domain, absolute_error, relative_error):
        self.denormal_errors[domain] = (absolute_error, relative_error)
