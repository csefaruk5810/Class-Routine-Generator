from scheduler.domain.models import WeightConfig


def describe_objective(weights: WeightConfig) -> dict[str, int]:
    return {
        "theory_after_1310": weights.theory_after_1310,
        "senior_teacher_morning": weights.senior_teacher_morning,
    }

