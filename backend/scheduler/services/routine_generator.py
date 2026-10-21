from scheduler.solver.cp_sat_solver import CPSATSolver


class RoutineGeneratorService:
    def __init__(self) -> None:
        self.solver = CPSATSolver()

    def generate(self, problem):
        return self.solver.solve(problem)

