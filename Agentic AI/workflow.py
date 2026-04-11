from typing import Annotated, Any
from typing_extensions import TypedDict
from datetime import datetime
from langgraph.graph import StateGraph, START, END
from agents.text_to_sql import get_agent_response as text_to_sql_agent
from agents.tools import read_product_info
from agents.sales_person import get_agent_response as sales_person_agent


class WorkFlowState(TypedDict):
    question: str
    query: str
    query_output : list[tuple[Any]]
    final_answer: str


def get_query_from_question(state: WorkFlowState) -> WorkFlowState:
    question = state['question']
    query = text_to_sql_agent(question)
    state['query'] = query
    return state



def get_query_output(state: WorkFlowState) -> WorkFlowState:
    query = state['query']
    query_output = read_product_info(query)
    state['query_output'] = query_output
    return state


def generate_final_answer(state: WorkFlowState) -> WorkFlowState:
    message = f'''
    Context:
    ---
        Question : {state['question']}
        SQL Query : {state['query']}
        Query Output : {state['query_output']}
    --

    Question: {state['question']}
    '''
    state['final_answer'] = sales_person_agent(message)

    return state



def create_workflow():
    graph = StateGraph(WorkFlowState)

    graph.add_node(get_query_from_question)
    graph.add_node(get_query_output)
    graph.add_node(generate_final_answer)

    graph.add_edge(START, "get_query_from_question")
    graph.add_edge("get_query_from_question", "get_query_output")
    graph.add_edge("get_query_output", "generate_final_answer")
    graph.add_edge("generate_final_answer", END)

    graph = graph.compile()
    return graph

    

if __name__ == "__main__":
    workflow = create_workflow()
    initial_state: WorkFlowState = {
        "question": "I have 200000 LKR budget. What is the best product I can buy within this budget?",
        "query": "",
        "query_output": [],
        "final_answer": ""
    }
    final_state = workflow.invoke(initial_state)
    print(final_state['final_answer'])
   



