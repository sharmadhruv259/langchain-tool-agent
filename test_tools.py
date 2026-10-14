from tools import math_tool, text_analyzer_tool, date_tool

tools = [
    math_tool,
    text_analyzer_tool,
    date_tool,
]

def test_math_tool() -> None:
    """
    Test the arithematic logic
    args: str
    """
    expression = input("Enter the expression: ")
    result = math_tool.invoke({
        "expression": expression
    })
    print("Calculation result:", result)
    print("\nAll tests passed!")

def test_text_analyzer_tool() -> None:
    """
    Test text analysis with user provided input
    args: none
    """
    user_text = input("Enter the text for analysis: ")

    result = text_analyzer_tool.invoke({
        "text": user_text
    })

    print("\n Text analysis result: ")
    print(result)

def test_date_tool() -> None:
    """
    """

    days = int(input("Enter the number of days-: "))
    result = date_tool.invoke({
        "days": days
    })
    print("\n Date Utility result: ")
    print(result)
    

if __name__ == "__main__":

    print("Available Tools: ")
    for tool in tools:
        print(f"- {tool.name}")
    # while True:
    #     print("\nChoose a tool to run:")
    #     print("1. Math Calculator")
    #     print("2. Text Analyzer")
    #     print("3. Date")
    #     print("4. Exit")
    #     choice = input("Enter your choice: ")

    #     if choice =='1':
    #         test_math_tool()
    #     elif choice =='2':
    #         test_text_analyzer_tool()
    #     elif choice =='3':
    #         test_date_tool()
    #     elif choice =='4':
    #         print("Exiting the program!")
    #         break
    #     else:
    #         print("Invalid option")