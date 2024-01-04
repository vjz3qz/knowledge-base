from langchain.chat_models import ChatOpenAI
import os

try:
    os.environ['OPENAI_API_KEY']
except KeyError:
    print('[error]: `API_KEY` environment variable required')
    sys.exit(1)


api_key = os.environ.get('OPENAI_API_KEY')
llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview",
                 openai_api_key=api_key)

def generate_image_summary(image):
    pass

def generate_video_transcript(video):
    pass

def llm_inference(query, search_results):

    # calls openai endpoint to respond based on context
    pass

