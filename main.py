from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
@tool(description="Get the current weather for given city")
def get_weather(city):
    return f'it is always sunny in {city}'

model = ChatOllama(model="llama3.2")
agent = create_agent(
    model = model,
    tools=[get_weather],
    system_prompt = 'you are a helpfull assistant'
)

result  = agent.invoke(
    {"messages":[{"role":"user","content":"what is the weather in philladelphia"}]}
)

print(result["messages"][-1].content_blocks)
