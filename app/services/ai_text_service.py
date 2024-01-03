from langchain.chat_models import ChatOpenAI
import os

try:
    os.environ['OPENAI_API_KEY']
except KeyError:
    print('[error]: `API_KEY` environment variable required')
    sys.exit(1)


api_key = os.environ.get('OPENAI_API_KEY')
# TODO update to 4
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k",
                 openai_api_key=api_key)

def generate_embedding(text):
    pass

def llm_inference(query, search_results):

    # calls openai endpoint to respond based on context
    pass
