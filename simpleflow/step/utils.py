from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import AnyStr, Dict, List, Sequence


def should_force_step(step_name: AnyStr, force_steps: Sequence[AnyStr]) -> bool:
    """
    Check if step_name is in force_steps.
    We support multi-level flags, ex for step_name = "a.b.c",
    we allow : "a", "a.b", "a.b.c".
    If one of force_steps is a wildcard (*), it will also force the step.
    """
    for step in force_steps:
        if step == "*" or step == step_name or step_name.startswith(step + "."):
            return True
    return False


def should_skip_step(step_name: AnyStr, skipped_steps: Sequence[AnyStr]) -> bool:
    return should_force_step(step_name, skipped_steps)


def step_will_run(step_name: AnyStr, force_steps: Sequence[AnyStr], skipped_steps: Sequence[AnyStr], steps_done: Sequence[AnyStr], force: bool = False) -> bool:
    """
    Return True if step will run by checking:
    1/ force is True
    2/ step_name is in force_steps configuration
    3/ step_name is not yet computed
    4/ step_name is not skipped
    """
    # Forced steps has priority on skipped steps
    if force or should_force_step(step_name, force_steps):
        return True
    elif should_skip_step(step_name, skipped_steps):
        return False
    else:
        return step_name not in steps_done


def step_is_forced(step_name: AnyStr, force_steps: Sequence[AnyStr], force: bool) -> bool:
    return force or should_force_step(step_name, force_steps)


def _get_step_reasons(step_name: AnyStr, step_reasons: Dict[AnyStr, Sequence[AnyStr]]) -> List[AnyStr]:
    reasons: List[AnyStr] = []
    for step, step_reasons in step_reasons.items():
        if step == "*" or step == step_name or step_name.startswith(step + "."):
            reasons += step_reasons
    return reasons


def get_step_force_reasons(step_name: AnyStr, step_force_reasons: Dict[AnyStr, Sequence[AnyStr]]) -> List[AnyStr]:
    return _get_step_reasons(step_name, step_force_reasons)


def step_is_skipped_by_force(step_name: AnyStr, skipped_steps: Sequence[AnyStr]) -> bool:
    return should_skip_step(step_name, skipped_steps)


def get_step_skip_reasons(step_name: AnyStr, step_skip_reasons: Dict[AnyStr, Sequence[AnyStr]]) -> List[AnyStr]:
    return _get_step_reasons(step_name, step_skip_reasons)
