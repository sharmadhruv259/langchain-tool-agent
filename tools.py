import operator
import ast

from pydantic import BaseModel, Field
from langchain.tools import tool
from datetime import date, timedelta

class MathInput(BaseModel):
    """
    Define the input schema for the math tool
    Attribute: str (arithematic expression to eval)
    Functions: None 
    """

    expression: str = Field(
        description="Expression to Eval-: "
    )

class TextInput(BaseModel):
    """
    Define the Input schema for the text analyzer
    Args: str
    """

    text: str = Field(
        description= "Text to analyze. "
    )

class DateInput(BaseModel):
    """
    """

    days: int = Field( description= "Number of days to add to today's date-: ")

def safe_calculate(expression: str) -> int | float:
    """Evaluate a basic arithmetic expression safely.
    Args: str (Arithmetic expression containing supported operators)
    Returns: int | float: Calculated numeric result.
    """
    if not expression.strip():
        raise ValueError("Expression cannot be empty.")

    if len(expression) > 200:
        raise ValueError("Expression is too long.")

    allowed_operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Invalid arithmetic expression.") from exc


    def evaluate(node) -> int | float:
        """Evaluate an approved arithmetic syntax-tree node.
        Returns: int | float: The value of the evaluated node.
        Raises: ValueError: If the node contains an unsupported operation.
        """

        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value

        if isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            left = evaluate(node.left)
            right = evaluate(node.right)

            if isinstance(node.op, ast.Pow) and abs(right) > 100:
                raise ValueError("Exponent is too large.")

            if isinstance(node.op, ast.Pow) and abs(left) > 1e6:
                raise ValueError("Base is too large.")

            result = allowed_operators[type(node.op)](left, right)

            if isinstance(result, (int, float)) and abs(result) > 1e100:
                raise ValueError("Result is too large.")

            return result

        if isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
            return allowed_operators[type(node.op)](evaluate(node.operand))

        raise ValueError("Only basic arithmetic is supported.")

    return evaluate(tree)


@tool(args_schema=MathInput)
def math_tool(expression: str) -> str:
    """Calculate a basic arithmetic expression.

    Args: str (Arithmetic expression to calculate)
    Returns: string (result or readable error message)
    """
    try:
        result = safe_calculate(expression)
        return f"Result: {result}"
    except (ValueError, ZeroDivisionError, TypeError) as exc:
        return f"Math error: {exc}"

@tool(args_schema=TextInput)
def text_analyzer_tool(text: str) -> str:
    """Analyze text and report word count, character count, and sentiment.

    Args:
        text (str): Text provided by the user.

    Returns:
        str: Word count, character count, and sentiment.

    Raises:
        None: Expected input errors are returned as text.
    """
    if not text.strip():
        return "Text analysis error: text can't be empty"

    if len(text) > 1000:
        return "Text analysis error: text is too long"

    positive_words = {
        "good", "great", "excellent", "happy", "love",
        "wonderful", "amazing", "helpful", "best", "enjoy"
    }

    negative_words = {
        "bad", "terrible", "awful", "sad", "hate",
        "poor", "worst", "angry", "disappointing", "problem"
    }

    words = text.split()

    normalized_words = {
        word.strip(".,!?;:()[]{}\"'").lower()
        for word in words
    }

    positive_count = len(normalized_words & positive_words)
    negative_count = len(normalized_words & negative_words)

    if positive_count > negative_count:
        sentiment = "Positive"
    elif negative_count > positive_count:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return (
        f"Word count: {len(words)}\n"
        f"Character count: {len(text)}\n"
        f"Sentiment: {sentiment}"
    )

@tool(args_schema=DateInput)
def date_tool(days: int) -> str:
    """
    define the input schema for the date tool
    args: days(int)
    """

    today = date.today()
    future_date = today + timedelta(days=days)
    return future_date.strftime("%Y-%m-%d")
