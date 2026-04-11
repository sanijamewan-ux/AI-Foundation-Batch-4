from groq import Groq
API_KEY = ""
client = Groq(api_key=API_KEY)

bank_database:list[dict] = [
    {"account_number": "1234", "account_holder": "John Doe", "balance": 5000},
    {"account_number": "9876", "account_holder": "Jane Smith", "balance": 3000},
    {"account_number": "5555", "account_holder": "Alice Johnson", "balance": 7000}
]

def chat_with_bank_agent(message:str , previous_messages:list , account_number:str):
    # Simulate a response from the bank agent
    
    account_details = None
    
    for bank_info in bank_database:
        if bank_info["account_number"] == account_number:
            account_details = bank_info
            break
    
    if account_details is None:
        return "Account not found."
    
    system_message = f'''
    You are a helpful bank assistant. 
    The user has an account with the following details: {account_details}. 
    Answer the user's query based on this information.
    '''
   
    return chat_with_agent(message , previous_messages , system_message)

def chat_with_agent(message:str , previous_messages:list , system_message:str = "You are a helpful assistant."):
    # Simulate a response from the agent
    completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages= [{
         "role": "system",
        "content": system_message
        }] 
    + previous_messages + [
      {
        "role": "user",
        "content": message
      }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=False,
    stop=None
    )
    result = completion.choices[0].message.content
    return result