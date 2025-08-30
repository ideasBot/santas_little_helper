from agno.models.google.gemini import Gemini
from agno.agent import Agent
from agno.memory.v2 import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from src.tools.flight import search_flights
from textwrap import dedent
import datetime


model = Gemini(
    id="gemini-2.5-flash",
    thinking_budget=-1,
)
model_lite = Gemini(
    id="gemini-2.5-flash-lite",
    thinking_budget=-1,
)

agent = Agent(
    model=model,
    memory=Memory(
        model=model_lite, db=SqliteMemoryDb(db_file="/tmp/18927891274897897.db")
    ),
    enable_agentic_memory=True,
    add_history_to_messages=True,
    search_previous_sessions_history=True,
    num_history_responses=10,
    tools=[search_flights],
    system_message=dedent(
        f"""今天的日期是 {datetime.datetime.now().isoformat()}"""
    ).strip(),
)

if __name__ == "__main__":
    # agent.print_response("每个人有多少根头发")
    initial_message = (
        "帮我看一下今年圣诞节期间从新加坡到冲绳的单程机票，告诉我有哪些选择，哪个好？"
    )
    while True:
        message = input("User: ")
        if message.lower() in {"exit", "quit"}:
            break
        agent.print_response(message)
