from fastapi import APIRouter, HTTPException

from src.api.schemas import (
    AgentRequest,
    AgentResponse,
    CalculatorRequest,
    CalculatorResponse,
    HealthResponse,
    RAGRequest,
    RAGResponse,
)

from src.calculator.basic import (
    add,
    subtract,
    multiply,
    divide,
)


router = APIRouter()


# ============================================================
# HEALTH CHECK
# ============================================================

@router.get(
    "/health",
    response_model=HealthResponse,
)
def health_check():

    return HealthResponse(
        status="healthy",
        application="MathMind AI",
        version="1.0.0",
    )


# ============================================================
# BASIC CALCULATOR
# ============================================================

@router.post(
    "/calculator",
    response_model=CalculatorResponse,
)
def calculator(
    request: CalculatorRequest,
):

    operation = (
        request.operation
        .lower()
        .strip()
    )

    num1 = request.num1
    num2 = request.num2

    try:

        # ----------------------------------------------------
        # ADDITION
        # ----------------------------------------------------

        if operation == "add":

            result = add(
                num1,
                num2,
            )

        # ----------------------------------------------------
        # SUBTRACTION
        # ----------------------------------------------------

        elif operation == "subtract":

            result = subtract(
                num1,
                num2,
            )

        # ----------------------------------------------------
        # MULTIPLICATION
        # ----------------------------------------------------

        elif operation == "multiply":

            result = multiply(
                num1,
                num2,
            )

        # ----------------------------------------------------
        # DIVISION
        # ----------------------------------------------------

        elif operation == "divide":

            # IMPORTANT:
            # Check division by zero BEFORE calling divide()

            if num2 == 0:

                raise HTTPException(
                    status_code=400,
                    detail=(
                        "Division by zero "
                        "is not allowed."
                    ),
                )

            result = divide(
                num1,
                num2,
            )

        # ----------------------------------------------------
        # INVALID OPERATION
        # ----------------------------------------------------

        else:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Unsupported operation. "
                    "Use add, subtract, "
                    "multiply or divide."
                ),
            )

        return CalculatorResponse(
            operation=operation,
            num1=num1,
            num2=num2,
            result=float(result),
        )

    except HTTPException:

        # Keep our intended 400 errors
        # unchanged.

        raise

    except ZeroDivisionError:

        raise HTTPException(
            status_code=400,
            detail=(
                "Division by zero "
                "is not allowed."
            ),
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error),
        )


# ============================================================
# RAG ENDPOINT
# ============================================================

@router.post(
    "/rag",
    response_model=RAGResponse,
)
def rag_question(
    request: RAGRequest,
):

    try:

        from src.rag.vector_store import (
            VectorDatabase,
        )

        from src.rag.config import (
            VECTOR_DB_DIR,
        )

        from src.rag.pipeline import (
            RAGPipeline,
        )

        from src.rag.memory import (
            ConversationMemory,
        )

        # ----------------------------------------------------
        # VECTOR DATABASE
        # ----------------------------------------------------

        vector_database = VectorDatabase()

        if not vector_database.exists(
            VECTOR_DB_DIR
        ):

            raise HTTPException(
                status_code=404,
                detail=(
                    "Vector database not found. "
                    "Please build the RAG vector "
                    "database first."
                ),
            )

        vector_db = vector_database.load(
            str(VECTOR_DB_DIR)
        )

        # ----------------------------------------------------
        # MEMORY
        # ----------------------------------------------------

        memory = ConversationMemory(
            max_messages=10
        )

        # ----------------------------------------------------
        # RAG PIPELINE
        # ----------------------------------------------------

        pipeline = RAGPipeline(
            vector_db=vector_db,
            provider=request.provider,
            retrieval_method=request.retrieval_method,
            top_k=request.top_k,
            memory=memory,
        )

        # ----------------------------------------------------
        # ASK QUESTION
        # ----------------------------------------------------

        result = pipeline.ask(
            request.question
        )

        answer = result.get(
            "answer",
            "No answer generated.",
        )

        sources = result.get(
            "sources",
            [],
        )

        return RAGResponse(
            question=request.question,
            answer=answer,
            sources=sources,
        )

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"RAG processing failed: "
                f"{error}"
            ),
        )


# ============================================================
# AGENT ENDPOINT
# ============================================================

@router.post(
    "/agent",
    response_model=AgentResponse,
)
def agent_question(
    request: AgentRequest,
):

    try:

        from src.agents.agent_graph import (
            MathMindAgentGraph,
        )

        # ----------------------------------------------------
        # CREATE AGENT
        # ----------------------------------------------------

        agent_graph = (
            MathMindAgentGraph()
        )

        # ----------------------------------------------------
        # EXECUTE AGENT
        # ----------------------------------------------------

        if hasattr(
            agent_graph,
            "run",
        ):

            result = agent_graph.run(
                request.question
            )

        elif hasattr(
            agent_graph,
            "invoke",
        ):

            result = agent_graph.invoke(
                {
                    "question": request.question,
                }
            )

        else:

            raise RuntimeError(
                "MathMindAgentGraph does not "
                "provide run() or invoke()."
            )

        # ----------------------------------------------------
        # PROCESS RESULT
        # ----------------------------------------------------

        if isinstance(
            result,
            dict,
        ):

            answer = (
                result.get("answer")
                or result.get("final_answer")
                or result.get("response")
                or str(result)
            )

            details = result

        else:

            answer = str(result)

            details = None

        return AgentResponse(
            question=request.question,
            answer=answer,
            status="success",
            details=details,
        )

    except HTTPException:

        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                f"Agent processing failed: "
                f"{error}"
            ),
        )