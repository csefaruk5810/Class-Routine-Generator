from scheduler.domain.models import SchedulingProblem


class CPSATSolver:
    def solve(self, problem: SchedulingProblem) -> dict:
        return {
            "status": "NOT_IMPLEMENTED",
            "section_id": problem.section_id,
            "message": "CP-SAT solver wiring will be added in the next milestone.",
        }

