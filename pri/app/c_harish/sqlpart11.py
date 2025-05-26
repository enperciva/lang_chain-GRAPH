
import getpass
import os


def _set_env(var: str):
    if not os.environ.get(var):
        os.environ[var] = getpass.getpass(f"{var}: ")


_set_env("ANTHROPIC_API_KEY")
_set_env("TAVILY_API_KEY")

# ## Base LLM

from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(temperature=0, model="claude-3-5-sonnet-20240620")

# ## Tavily Search Tool

tavily_search_tool = TavilySearchResults(
    max_results=5,
    include_answer=True,
    include_raw_content=True,
    include_images=True,
    # search_depth="advanced",
    # include_domains = []
    # exclude_domains = []
)


tools = [tavily_search_tool]

tavily_search_tool.invoke({"query": "Any latest news in sports"})

# ## Chain

from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

builder = StateGraph(MessagesState)

llm_with_tools = llm.bind_tools(tools)

def assistant(state: MessagesState):
  return {'messages': llm_with_tools.invoke(state['messages'])}


builder.add_node('assistant', assistant)

builder.add_edge(START, 'assistant')
builder.add_edge('assistant', END)

graph = builder.compile()



from IPython.display import Image, display

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass

from pprint import pprint

result = graph.invoke({'messages': ['hello']})

for m in result['messages']:
  m.pretty_print()

result = graph.invoke({'messages': ['Is it raining in bangalore?']})

for m in result['messages']:
  m.pretty_print()

# ## Router

from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

builder = StateGraph(MessagesState)

def assistant(state: MessagesState):
  return {'messages': llm_with_tools.invoke(state['messages'])}


builder.add_node('assistant', assistant)
builder.add_node('tools', ToolNode(tools))

builder.add_edge(START, 'assistant')
builder.add_conditional_edges('assistant',
                              # if latest message from assistant is a tool call -> tools condition routes to tools node
                              # if latest message from assistant is not a tool call -> routes to END
                              tools_condition)

builder.add_edge('tools', END)

graph = builder.compile()



from IPython.display import Image, display

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass


result = graph.invoke({'messages': ['Search how is the weather today in Bangalore?']})

for m in result['messages']:
  m.pretty_print()

import json

tool_output = json.loads(result['messages'][-1].content)

for m in tool_output:
  print(m['url'])
  print(m['content'])
  print()


result = graph.invoke({'messages': ['What is 9 multiplied by 5']})


for m in result['messages']:
  m.pretty_print()

# ## TOOL LLM LOOP

# %%
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

builder = StateGraph(MessagesState)

def assistant(state: MessagesState):
  return {'messages': llm_with_tools.invoke(state['messages'])}


builder.add_node('assistant', assistant)
builder.add_node('tools', ToolNode(tools))

builder.add_edge(START, 'assistant')
builder.add_conditional_edges('assistant',
                              # if latest message from assistant is a tool call -> tools condition routes to tools
                              # if latest message from assistant is not a tool call -> routes to END
                              tools_condition)

builder.add_edge('tools', "assistant")
builder.add_edge('tools', END)

graph = builder.compile()



from IPython.display import Image, display

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass

result = graph.invoke({'messages': ['Search how is the weather today in Bangalore? Collect temperature, condition, humidity. If temperature greater than 30 then call it a hot day']})

from pprint import pprint


for m in result['messages']:
  m.pretty_print()


