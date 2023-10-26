from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

def operator_message_generate():
    chat = ChatOpenAI(temperature=0)
    messages = [
        SystemMessage(
            content="""You are looking to work collect data from an energy plant worker. 
            
            This data will either be an incident report or a work report.
            
            Ask them if it is an incident report. If it is. Ask them the following questions separately.

            1) What was the incident?

            2) Where was the incident?

            3) How did you fix the incident?

            4) How severe was the incident?

            Then come up with some follow up questions.

            If it is a work report, then ask them these questions:

            1) What did you work on?

            2) Where did you work on it?

            3) What challenges did you face?

            4) How did you fix those challenges?

            Then come up with some follow up questions.

            """
        ),
    ]
    return chat(messages)


