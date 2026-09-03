from src.rag.relevance import RelevanceAnalyzer


analyzer = RelevanceAnalyzer()


test_scores = [
    0.2,
    0.5,
    0.9,
    1.5,
]


print("\n==============================")
print("MathMind-AI Relevance Test")
print("==============================")

for score in test_scores:

    confidence = analyzer.classify_score(
        score
    )

    print(
        f"Score: {score:.2f} "
        f"→ Confidence: {confidence}"
    )