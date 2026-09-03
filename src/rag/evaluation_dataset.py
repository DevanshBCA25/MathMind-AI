"""
MathMind-AI - Retrieval Evaluation Dataset v2
"""

RETRIEVAL_EVALUATION_DATASET_V2 = [
    {"id": 1, "question": "What is the area of the rectangle in the worked example?", "expected_answer": "60 cm²", "topic": "Geometry"},
    {"id": 2, "question": "What is the perimeter of the example rectangle?", "expected_answer": "34 cm", "topic": "Geometry"},
    {"id": 3, "question": "What is the discriminant of ax² + bx + c?", "expected_answer": "b² - 4ac", "topic": "Quadratic Equations"},
    {"id": 4, "question": "How is the median calculated?", "expected_answer": "The median is the middle value after sorting the observations.", "topic": "Statistics"},
    {"id": 5, "question": "What is the range of a valid probability?", "expected_answer": "A probability is between 0 and 1 inclusive.", "topic": "Probability"},
    {"id": 6, "question": "What is a linear equation?", "expected_answer": "A linear equation is an equation in which the highest power of the variable is 1.", "topic": "Algebra"},
    {"id": 7, "question": "What does an algebraic expression combine?", "expected_answer": "Numbers, variables, and mathematical operations.", "topic": "Algebra"},
    {"id": 8, "question": "What does differentiation measure?", "expected_answer": "Differentiation measures the rate at which a function changes.", "topic": "Calculus"},
    {"id": 9, "question": "What is the derivative of f(x) = x²?", "expected_answer": "f'(x) = 2x", "topic": "Calculus"},
    {"id": 10, "question": "What can integration be viewed as?", "expected_answer": "Integration can be viewed as the reverse operation of differentiation.", "topic": "Calculus"},
    {"id": 11, "question": "How is the probability of an event calculated for equally likely outcomes?", "expected_answer": "Number of favorable outcomes divided by the total number of possible outcomes.", "topic": "Probability"},
    {"id": 12, "question": "What is the minimum possible value of a probability?", "expected_answer": "0", "topic": "Probability"},
    {"id": 13, "question": "What is the maximum possible value of a probability?", "expected_answer": "1", "topic": "Probability"},
    {"id": 14, "question": "What is the relationship between differentiation and integration?", "expected_answer": "Integration can be viewed as the reverse operation of differentiation.", "topic": "Calculus"},
    {"id": 15, "question": "What is the highest power of the variable in a linear equation?", "expected_answer": "1", "topic": "Algebra"},
]

# Keep compatibility with the existing RAG evaluation code.
TEST_DATASET = RETRIEVAL_EVALUATION_DATASET_V2


def get_dataset():
    return RETRIEVAL_EVALUATION_DATASET_V2


if __name__ == "__main__":
    print("=" * 60)
    print("MathMind-AI Retrieval Evaluation Dataset v2")
    print("=" * 60)
    print(f"Total questions: {len(RETRIEVAL_EVALUATION_DATASET_V2)}")