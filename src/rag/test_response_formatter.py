from langchain_core.documents import Document

from src.rag.response_formatter import (
    RAGResponseFormatter,
)


print("\n===================================")
print("MathMind-AI Response Formatter Test")
print("===================================")


documents = [

    Document(
        page_content=(
            "A rectangle with length 12 cm "
            "and width 5 cm has area 60 cm²."
        ),
        metadata={
            "source": "MathMind_RAG_Test_Document.pdf",
            "page": 0,
        },
    ),

    Document(
        page_content=(
            "The perimeter of the rectangle "
            "is 34 cm."
        ),
        metadata={
            "source": "MathMind_RAG_Test_Document.pdf",
            "page": 1,
        },
    ),

]


formatter = RAGResponseFormatter()


print("\n1. Formatting sources...")

sources = formatter.format_sources(
    documents
)

for source in sources:

    print(
        f"Source [{source['citation_id']}]: "
        f"{source['source']} "
        f"| Page: {source['page']}"
    )


print("\n2. Testing safe answer...")

answer = formatter.safe_answer(
    "The area of the rectangle is 60 cm².",
    documents,
)

print(answer)


print("\n3. Testing citations...")

final_answer = formatter.add_citations(
    answer,
    sources,
)

print("\nFinal Answer:")
print(final_answer)


print("\n===================================")
print("Response Formatter Test Complete")
print("===================================")