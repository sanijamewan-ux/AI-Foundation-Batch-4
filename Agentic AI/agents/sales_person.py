GROQ_API_KEY = <API_KEY>

import pandas as pd
import json
import os


file_path = os.path.join(os.path.dirname(__file__), 'product_info.csv')
product_info = pd.read_csv(file_path)

SYSTEM_PROMPT = f'''
You are helpful sales assistant in Max Mobiles in Sri Lanka.

The user is a customer interested in purchasing products.
Rules:
1. Always provide accurate and helpful information about products, promotions, and services.
2. Behave in friendly and professional manner.
3. Answer the questions based on the product information provided below. If the information is not available, politely inform the user that you do not have that information.

You have access to the tools with the following functionalities:
1. text_to_sql_agent: This tool converts user questions into SQL queries to retrieve relevant information from the product_info table.
2. read_product_info: This tool executes SQL queries on the product_info table and returns the results.
'''

from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai.providers.groq import GroqProvider


model = GroqModel(
    'llama-3.3-70b-versatile', provider=GroqProvider(api_key=GROQ_API_KEY)
)

agent = Agent(model, system_prompt=SYSTEM_PROMPT )

def get_agent_response(message:str):
    # Simulate a response from the sales agent
    response = agent.run_sync(message)
    return response.output


def main():
    print(get_agent_response("What is the name of the product which has highest actual price?"))


if __name__ == "__main__":
    main()