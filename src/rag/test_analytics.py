from src.rag.analytics import RAGAnalytics


analytics = RAGAnalytics()


analytics.record(
    question="What is the area of a rectangle?",
    answer="The area is 60 cm².",
    provider="Gemini",
    retrieval_method="similarity",
    retrieval_time=0.42,
    generation_time=1.83,
    confidence={
        "score": 0.87,
        "level": "HIGH",
    },
)


analytics.record(
    question="What is the perimeter?",
    answer="The perimeter is 34 cm.",
    provider="Gemini",
    retrieval_method="mmr",
    retrieval_time=0.51,
    generation_time=2.10,
    confidence={
        "score": 0.62,
        "level": "MEDIUM",
    },
)


print("\n================================")
print("MathMind-AI RAG Analytics Test")
print("================================")


print(
    "\nTotal Queries:",
    analytics.total_queries(),
)


print(
    "Average Retrieval Time:",
    analytics.average_retrieval_time(),
    "seconds",
)


print(
    "Average Generation Time:",
    analytics.average_generation_time(),
    "seconds",
)


print(
    "Average Confidence:",
    analytics.average_confidence(),
)


print(
    "\nConfidence Distribution:"
)

print(
    analytics.confidence_distribution()
)


print(
    "\nProvider Statistics:"
)

print(
    analytics.provider_statistics()
)


print(
    "\nRetrieval Statistics:"
)

print(
    analytics.retrieval_statistics()
)


print(
    "\nComplete Summary:"
)

print(
    analytics.summary()
)


print("\n================================")
print("Analytics Test Complete")
print("================================")