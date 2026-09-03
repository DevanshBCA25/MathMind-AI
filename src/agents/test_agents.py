from src.agents.planner import MathPlanner
from src.agents.solver import MathSolver
from src.agents.reviewer import MathReviewer
from src.agents.teacher import MathTeacher


def main():

    print("\n" + "=" * 60)
    print("MathMind-AI Agent Layer Test")
    print("=" * 60)

    question = (
        "What is the area of a rectangle "
        "with length 12 cm and width 5 cm?"
    )

    # ----------------------------------------
    # 1. PLANNER
    # ----------------------------------------

    print("\n[1/4] Testing Planner...")

    planner = MathPlanner()

    plan = planner.plan(
        question
    )

    print(
        "Problem Type:",
        plan["problem_type"],
    )

    print(
        "Total Steps:",
        plan["total_steps"],
    )

    print("✅ Planner working.")

    # ----------------------------------------
    # 2. SOLVER
    # ----------------------------------------

    print("\n[2/4] Testing Solver...")

    solver = MathSolver()

    solution = solver.solve(
        question,
        plan,
    )

    print(
        "Method:",
        solution["method"],
    )

    print(
        "Solution:",
        solution["solution"],
    )

    print("✅ Solver working.")

    # ----------------------------------------
    # 3. REVIEWER
    # ----------------------------------------

    print("\n[3/4] Testing Reviewer...")

    reviewer = MathReviewer()

    review = reviewer.review(
        question,
        solution,
    )

    print(
        "Review Status:",
        review["status"],
    )

    print(
        "Review Score:",
        review["score"],
    )

    print("✅ Reviewer working.")

    # ----------------------------------------
    # 4. TEACHER
    # ----------------------------------------

    print("\n[4/4] Testing Teacher...")

    teacher = MathTeacher()

    teaching = teacher.teach(
        question,
        solution,
        review,
    )

    print(
        "Teaching Mode:",
        teaching["teaching_mode"],
    )

    print("\nExplanation:")
    print(
        teaching["explanation"]
    )

    print("\n" + "=" * 60)
    print("Agent Layer Test Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()