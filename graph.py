from typing import Literal

from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from agents import *
from tools import *
from models import *
from flow import *


class State(TypedDict):
    messages: Annotated[list, add_messages]


MAX_ITERATIONS = 5
builder = StateGraph(State)
builder.add_node("draft", first_responder.respond)


builder.add_node("execute_tools", tool_node)
builder.add_node("revise", revisor.respond)
# draft -> execute_tools
builder.add_edge("draft", "execute_tools")
# execute_tools -> revise
builder.add_edge("execute_tools", "revise")

# Define looping logic:


def _get_num_iterations(state: list):
    i = 0
    for m in state[::-1]:
        if m.type not in {"tool", "ai"}:
            break
        i += 1
    return i



def _looks_done(messages) -> bool:
    # find last ai tool call arguments -> ReviseAnswer / AnswerQuestion
    for m in reversed(messages):
        if getattr(m, "type", None) == "ai" and getattr(m, "tool_calls", None):
            tc = m.tool_calls[0]
            args = tc.get("args", {}) or {}
            ans = (args.get("answer") or "").strip()
            refs = args.get("references") or []
            has_refs_section = "References" in ans
            has_citations = "[" in ans and "]" in ans
            short_enough = len(ans.split()) <= 260  #slight buffer
            enough_refs = isinstance(refs, list) and len(refs) >= 2
            #require mitigation + adaptation words to avoid drifting to just one side
            balanced = ("mitigation" in ans.lower()) and ("adaptation" in ans.lower())
            return short_enough and has_citations and has_refs_section and enough_refs and balanced
    return False


def event_loop(state: list):
    messages = state["messages"]

    # stop when answer meets criteria to prevents endless selfrevision drift
    if _looks_done(messages):
        return END

    last = messages[-1]
    if getattr(last, "type", None) == "ai" and not getattr(last, "tool_calls", None):
        return END

    num_iterations = _get_num_iterations(messages)
    if num_iterations > MAX_ITERATIONS:
        return END
    return "execute_tools"

# revise -> execute_tools OR end
builder.add_conditional_edges("revise", event_loop, ["execute_tools", END])
builder.add_edge(START, "draft")
graph = builder.compile()