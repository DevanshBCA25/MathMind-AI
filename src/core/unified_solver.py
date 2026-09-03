from typing import Any, Dict, Optional
import re


class UnifiedSolver:
    """
    Unified entry point for MathMind-AI.

    Routes questions to:
        - Calculator
        - Symbolic Mathematics
        - RAG
        - Multi-Agent reasoning

    API/provider failures are handled gracefully.
    """

    def __init__(
        self,
        provider: str = "Gemini",
        vector_db: Optional[Any] = None,
        top_k: int = 4,
        retrieval_method: str = "similarity",
    ) -> None:

        self.provider = provider
        self.vector_db = vector_db
        self.top_k = top_k
        self.retrieval_method = retrieval_method

        self.pipeline = None
        self.agent_graph = None

        self._initialize_components()

    # ==========================================================
    # INITIALIZE COMPONENTS
    # ==========================================================

    def _initialize_components(self) -> None:

        # ------------------------------------------------------
        # RAG
        # ------------------------------------------------------

        if self.vector_db is not None:

            try:

                from src.rag.pipeline import RAGPipeline

                self.pipeline = RAGPipeline(
                    vector_db=self.vector_db,
                    provider=self.provider,
                    retrieval_method=self.retrieval_method,
                    top_k=self.top_k,
                )

            except Exception:

                self.pipeline = None

        # ------------------------------------------------------
        # MULTI AGENT
        # ------------------------------------------------------

        try:

            from src.agents.agent_graph import (
                MathMindAgentGraph,
            )

            self.agent_graph = MathMindAgentGraph(
                provider=self.provider
            )

        except Exception:

            self.agent_graph = None

    # ==========================================================
    # PROVIDER
    # ==========================================================

    def set_provider(
        self,
        provider: str,
    ) -> None:

        self.provider = provider

        if self.pipeline is not None:

            try:

                self.pipeline.change_provider(
                    provider
                )

            except Exception:

                pass

        if self.agent_graph is not None:

            try:

                self.agent_graph.set_provider(
                    provider
                )

            except Exception:

                pass

    # ==========================================================
    # QUESTION CLASSIFICATION
    # ==========================================================

    @staticmethod
    def classify_question(
        question: str,
    ) -> str:

        if not question or not question.strip():

            return "unknown"

        q = question.lower().strip()

        # ======================================================
        # RAG
        # ======================================================

        rag_keywords = [
            "according to the document",
            "according to the pdf",
            "according to my document",
            "according to my pdf",
            "uploaded document",
            "uploaded pdf",
            "uploaded file",
            "in the document",
            "in the pdf",
            "in my document",
            "in my pdf",
            "from the document",
            "from the pdf",
            "from my document",
            "from my pdf",
            "what does the document",
            "what does the pdf",
            "what does my document",
            "what does my pdf",
        ]

        if any(
            keyword in q
            for keyword in rag_keywords
        ):

            return "rag"

        # ======================================================
        # MATRIX
        # ======================================================

        matrix_keywords = [
            "matrix",
            "matrices",
            "determinant",
            "inverse matrix",
            "matrix inverse",
            "eigenvalue",
            "eigenvalues",
            "eigenvector",
            "eigenvectors",
            "transpose",
        ]

        if any(
            keyword in q
            for keyword in matrix_keywords
        ):

            return "matrix"

        # ======================================================
        # STATISTICS
        # ======================================================

        statistics_keywords = [
            "mean",
            "median",
            "mode",
            "standard deviation",
            "variance",
            "correlation",
            "regression",
            "statistics",
            "statistical",
            "percentile",
            "quartile",
            "average",
        ]

        if any(
            keyword in q
            for keyword in statistics_keywords
        ):

            return "statistics"

        # ======================================================
        # SYMBOLIC
        # ======================================================

        symbolic_keywords = [
            "differentiate",
            "differentiation",
            "derivative",
            "derive",
            "integrate",
            "integration",
            "integral",
            "factor",
            "factorize",
            "factorise",
            "simplify",
            "simplification",
            "solve equation",
            "symbolic",
            "limit",
            "limits",
            "quadratic equation",
            "polynomial",
        ]

        # Equation detection
        if "=" in q:

            return "symbolic"

        # "solve x..." / "solve equation..."
        if (
            q.startswith("solve ")
            or q.startswith("solve:")
            or q.startswith("find x")
            or q.startswith("find the value of x")
        ):

            return "symbolic"

        if any(
            keyword in q
            for keyword in symbolic_keywords
        ):

            return "symbolic"

        # ======================================================
        # GRAPH
        # ======================================================

        graph_keywords = [
            "plot",
            "graph",
            "graph of",
            "plot the function",
            "plot function",
            "visualize function",
            "draw graph",
            "coordinate graph",
        ]

        if any(
            keyword in q
            for keyword in graph_keywords
        ):

            return "graph"

        # ======================================================
        # CALCULATOR
        # ======================================================

        calculator_keywords = [
            "calculate",
            "calculation",
            "add",
            "addition",
            "subtract",
            "subtraction",
            "multiply",
            "multiplication",
            "divide",
            "division",
            "plus",
            "minus",
            "times",
        ]

        if any(
            keyword in q
            for keyword in calculator_keywords
        ):

            return "calculator"

        # ======================================================
        # PURE ARITHMETIC
        # ======================================================

        expression_pattern = (
            r"^[0-9\s\+\-\*\/\(\)\.\^]+$"
        )

        if re.fullmatch(
            expression_pattern,
            q,
        ):

            return "calculator"

        # ======================================================
        # AGENT REASONING
        # ======================================================

        reasoning_keywords = [
            "explain",
            "explain why",
            "step by step",
            "prove",
            "proof",
            "reason",
            "why",
            "how",
            "teach",
            "understand",
        ]

        if any(
            keyword in q
            for keyword in reasoning_keywords
        ):

            return "agent"

        # ======================================================
        # DEFAULT
        # ======================================================

        return "agent"

    # ==========================================================
    # CALCULATOR
    # ==========================================================

    def _calculator(
        self,
        question: str,
    ) -> Dict[str, Any]:

        try:

            from src.calculator.basic import (
                add,
                subtract,
                multiply,
                divide,
            )

            expression = (
                question
                .lower()
                .replace(
                    "calculate",
                    "",
                )
                .strip()
            )

            # Remove common words
            expression = re.sub(
                r"^(what is|what's|calculate)\s+",
                "",
                expression,
                flags=re.IGNORECASE,
            ).strip()

            # --------------------------------------------------
            # Normalize word operators
            # --------------------------------------------------

            replacements = {
                " plus ": "+",
                " minus ": "-",
                " times ": "*",
                " multiplied by ": "*",
                " divided by ": "/",
            }

            for word, symbol in replacements.items():

                expression = expression.replace(
                    word,
                    symbol,
                )

            # --------------------------------------------------
            # Parse simple arithmetic
            # --------------------------------------------------

            match = re.fullmatch(
                r"\s*(-?\d+(?:\.\d+)?)\s*"
                r"([\+\-\*\/])\s*"
                r"(-?\d+(?:\.\d+)?)\s*",
                expression,
            )

            if not match:

                return {
                    "status": "FALLBACK",
                    "module": "calculator",
                    "answer": "",
                    "message": (
                        "I could not parse "
                        "this arithmetic expression."
                    ),
                }

            num1 = float(
                match.group(1)
            )

            operator = match.group(2)

            num2 = float(
                match.group(3)
            )

            # --------------------------------------------------
            # Execute operation
            # --------------------------------------------------

            if operator == "+":

                result = add(
                    num1,
                    num2,
                )

            elif operator == "-":

                result = subtract(
                    num1,
                    num2,
                )

            elif operator == "*":

                result = multiply(
                    num1,
                    num2,
                )

            else:

                result = divide(
                    num1,
                    num2,
                )

            # Make 50.0 -> 50
            if isinstance(
                result,
                float,
            ) and result.is_integer():

                result = int(result)

            return {
                "status": "SUCCESS",
                "module": "calculator",
                "answer": str(result),
            }

        except Exception as error:

            return {
                "status": "ERROR",
                "module": "calculator",
                "answer": "",
                "message": str(error),
            }

    # ==========================================================
    # SYMBOLIC
    # ==========================================================

    def _symbolic(
        self,
        question: str,
    ) -> Dict[str, Any]:

        try:

            import sympy as sp

            text = question.strip()

            # --------------------------------------------------
            # Remove common command words
            # --------------------------------------------------

            text = re.sub(
                r"^(solve|calculate|find)\s+",
                "",
                text,
                flags=re.IGNORECASE,
            ).strip()

            # --------------------------------------------------
            # Equation
            # --------------------------------------------------

            if "=" in text:

                left, right = text.split(
                    "=",
                    1,
                )

                left_expr = sp.sympify(
                    left.strip()
                )

                right_expr = sp.sympify(
                    right.strip()
                )

                symbols = sorted(
                    left_expr.free_symbols
                    | right_expr.free_symbols,
                    key=lambda symbol: symbol.name,
                )

                if not symbols:

                    result = sp.simplify(
                        left_expr - right_expr
                    )

                    answer = str(
                        result == 0
                    )

                else:

                    solutions = sp.solve(
                        sp.Eq(
                            left_expr,
                            right_expr,
                        ),
                        symbols,
                    )

                    answer = str(
                        solutions
                    )

                return {
                    "status": "SUCCESS",
                    "module": "symbolic",
                    "answer": answer,
                }

            # --------------------------------------------------
            # Expression
            # --------------------------------------------------

            # Basic natural-language symbolic commands
            expression_text = text

            expression_text = re.sub(
                r"^(differentiate|derivative of|derive)\s+",
                "",
                expression_text,
                flags=re.IGNORECASE,
            )

            expression_text = re.sub(
                r"^(integrate|integral of)\s+",
                "",
                expression_text,
                flags=re.IGNORECASE,
            )

            expression_text = re.sub(
                r"^(factor|factorize|factorise)\s+",
                "",
                expression_text,
                flags=re.IGNORECASE,
            )

            expression = sp.sympify(
                expression_text
            )

            # --------------------------------------------------
            # Differentiation
            # --------------------------------------------------

            if re.search(
                r"(differentiate|derivative|derive)",
                question,
                flags=re.IGNORECASE,
            ):

                symbol = sorted(
                    expression.free_symbols,
                    key=lambda s: s.name,
                )

                if symbol:

                    simplified = sp.diff(
                        expression,
                        symbol[0],
                    )

                else:

                    simplified = sp.diff(
                        expression
                    )

            # --------------------------------------------------
            # Integration
            # --------------------------------------------------

            elif re.search(
                r"(integrate|integration|integral)",
                question,
                flags=re.IGNORECASE,
            ):

                symbol = sorted(
                    expression.free_symbols,
                    key=lambda s: s.name,
                )

                if symbol:

                    simplified = sp.integrate(
                        expression,
                        symbol[0],
                    )

                else:

                    simplified = sp.integrate(
                        expression
                    )

            # --------------------------------------------------
            # Factorization
            # --------------------------------------------------

            elif re.search(
                r"(factor|factorize|factorise)",
                question,
                flags=re.IGNORECASE,
            ):

                simplified = sp.factor(
                    expression
                )

            # --------------------------------------------------
            # Default symbolic simplify
            # --------------------------------------------------

            else:

                simplified = sp.simplify(
                    expression
                )

            return {
                "status": "SUCCESS",
                "module": "symbolic",
                "answer": str(
                    simplified
                ),
            }

        except Exception as error:

            return {
                "status": "FALLBACK",
                "module": "symbolic",
                "answer": "",
                "message": str(error),
            }

    # ==========================================================
    # RAG
    # ==========================================================

    def _rag(
        self,
        question: str,
    ) -> Dict[str, Any]:

        if self.pipeline is None:

            return {
                "status": "UNAVAILABLE",
                "module": "rag",
                "answer": "",
                "message": (
                    "RAG pipeline is not initialized. "
                    "Load or build the vector database first."
                ),
            }

        try:

            result = self.pipeline.ask(
                question
            )

            if not isinstance(
                result,
                dict,
            ):

                return {
                    "status": "SUCCESS",
                    "module": "rag",
                    "answer": str(result),
                }

            return {
                "status": "SUCCESS",
                "module": "rag",
                **result,
            }

        except Exception as error:

            return {
                "status": "API_ERROR",
                "module": "rag",
                "answer": "",
                "message": str(error),
            }

    # ==========================================================
    # MULTI AGENT
    # ==========================================================

    def _agent(
        self,
        question: str,
    ) -> Dict[str, Any]:

        if self.agent_graph is None:

            return {
                "status": "UNAVAILABLE",
                "module": "agents",
                "answer": "",
                "message": (
                    "Multi-Agent graph is "
                    "not available."
                ),
            }

        try:

            result = self.agent_graph.run(
                question
            )

            if not isinstance(
                result,
                dict,
            ):

                return {
                    "status": "SUCCESS",
                    "module": "agents",
                    "answer": str(result),
                }

            answer = (
                result.get("explanation")
                or result.get("solution")
                or result.get("answer")
                or ""
            )

            return {
                "status": result.get(
                    "status",
                    "SUCCESS",
                ),
                "module": "agents",
                "answer": str(answer),
                **result,
            }

        except Exception as error:

            return {
                "status": "API_ERROR",
                "module": "agents",
                "answer": "",
                "message": str(error),
            }

    # ==========================================================
    # MAIN SOLVE METHOD
    # ==========================================================

    def solve(
        self,
        question: str,
        force_module: Optional[str] = None,
    ) -> Dict[str, Any]:

        # ------------------------------------------------------
        # Empty question
        # ------------------------------------------------------

        if not question or not question.strip():

            return {
                "status": "ERROR",
                "module": "unknown",
                "question": question,
                "answer": (
                    "Please enter a question."
                ),
            }

        # ------------------------------------------------------
        # Provider
        # ------------------------------------------------------

        # Keep provider state consistent.
        if self.provider:

            self.set_provider(
                self.provider
            )

        # ------------------------------------------------------
        # Determine module
        # ------------------------------------------------------

        if force_module:

            module = (
                str(force_module)
                .strip()
                .lower()
            )

        else:

            module = self.classify_question(
                question
            )

        # ------------------------------------------------------
        # Routing
        # ------------------------------------------------------

        if module == "calculator":

            result = self._calculator(
                question
            )

        elif module == "symbolic":

            result = self._symbolic(
                question
            )

        elif module == "rag":

            result = self._rag(
                question
            )

        elif module in (
            "agent",
            "agents",
        ):

            module = "agent"

            result = self._agent(
                question
            )

        elif module in (
            "matrix",
            "statistics",
            "graph",
        ):

            result = self._agent(
                question
            )

            if result.get(
                "status"
            ) == "UNAVAILABLE":

                result = {
                    "status": "FALLBACK",
                    "module": module,
                    "answer": (
                        f"The {module} module "
                        "should be handled through "
                        "its dedicated interface."
                    ),
                }

        else:

            module = "agent"

            result = self._agent(
                question
            )

        # ------------------------------------------------------
        # Final answer
        # ------------------------------------------------------

        answer = (
            result.get("answer")
            or result.get("explanation")
            or result.get("solution")
            or result.get("message")
            or ""
        )

        return {
            "status": result.get(
                "status",
                "SUCCESS",
            ),
            "module": module,
            "question": question,
            "answer": str(answer),
            "result": result,
            "provider": self.provider,
        }