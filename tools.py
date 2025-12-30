import json
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import ToolNode

from agents import *
from models import *
from flow import *

def run_queries(search_queries: list[str], **kwargs):
    """
    No web. Convert queries into a structured research brief + authoritative baseline sources
    the reviser can cite. Avoid fabricating recent stats/policy outcomes.
    """
    sources = [
        "https://www.ipcc.ch/",
        "https://unfccc.int/process-and-meetings/the-paris-agreement/the-paris-agreement",
        "https://www.iea.org/",
        "https://climate.nasa.gov/",
        "https://ourworldindata.org/co2-and-greenhouse-gas-emissions",
    ]

    queries = (search_queries or [])[:3]
    prompt = (
        "You can not browse the web, using generally accepted knowledge, produce a compact brief.\n"
        "Rules:\n"
        "- Do NOT invent 2024/2025 policy facts or specific numbers.\n"
        "- Focus on prioritization, trade-offs, barriers, and measurable actions.\n"
        "Return JSON with keys: priorities (list), barriers (list), actions_by_horizon (dict), metrics (list).\n\n"
        f"Queries: {queries}"
    )
    resp = llm.invoke(prompt)
    brief_text = getattr(resp, "content", str(resp))

    return json.dumps({"brief": brief_text, "sources": sources})

tool_node = ToolNode(
    [
        StructuredTool.from_function(run_queries, name=AnswerQuestion.__name__),
        StructuredTool.from_function(run_queries, name=ReviseAnswer.__name__),
    ]
)
