from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from dotenv import load_dotenv

load_dotenv()

@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmetic operations."""
    print("Tool has been called")
    return f"The sum of {a} and {b} is {a + b}"

@tool
def say_hello(name:str) -> str:
    """Useful for greeting a user."""
    print("Tool has been called")
    return f"Hello, {name}! How can I assist you today?"


def main():
    model = ChatOpenAI(temperature=0)

    tools=[calculator, say_hello]
    agent_executor = create_react_agent(model,tools)

    print("Welcome to the AI Agent!.Type 'quit' to exit.")
    print("You can ask me to perform calculations or chat with me, and I will do my best to assist you.")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'quit':
            print("Exiting the AI Agent. Goodbye!")
            break
        print("\nAssistant: ",end="")
        for chunk in agent_executor.stream({"messages":[HumanMessage(content=user_input)]}):
            if "agent" in chunk and "message" in chunk["agent"]:
                for message in chunk["agent"]["message"]:
                    print(message.content, end="")
        print()
if __name__ == "__main__":
    main()
                                           
            
        