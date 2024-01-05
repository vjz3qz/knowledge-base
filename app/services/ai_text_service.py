from langchain.chat_models import ChatOpenAI
import os
from openai import OpenAI 
import whisper

client = OpenAI()

try:
    os.environ['OPENAI_API_KEY']
except KeyError:
    print('[error]: `API_KEY` environment variable required')
    sys.exit(1)

api_key = os.environ.get('OPENAI_API_KEY')
llm = ChatOpenAI(temperature=0, model_name="gpt-4-1106-preview",
                 openai_api_key=api_key)

def generate_text(file, file_type):
    if file_type == 'video':
        return generate_video_transcript(file)
    elif file_type == 'image':
        return generate_image_summary(file)
    return ""

def generate_image_summary(image):
    """Generates a summary from an image file with the GPT-4V API.

    Args:
        image (png, jpg): The image file.

    Returns:
        str: The summary of the image.
    """
    return ""

def generate_video_transcript(video):
    """Generates a transcript from a video file with the Whisper API.

    Args:
        video (mp4): The video file.

    Returns:
        str: The transcript of the video.
    """
    return ""

def llm_inference(query, search_results=[]):
    """Generates a response from the LLM based on the query and search results.

    Args:
        video (str): The user's query.
        search_results (list, optional): The results from the search. Defaults to [].

    Returns:
        str: The response from the LLM.
    """

    # calls openai endpoint to respond based on context
    return ""

# def summarize_image(image_url, prompt="Describe the image in detail. Be specific about symbols and connections."):
#     response = client.chat.completions.create(
#         model="gpt-4-vision-preview",
#         messages=[
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": prompt},
#                     {
#                         "type": "image_url",
#                         "image_url": image_url,
#                     },
#                 ],
#             }
#         ],
#         max_tokens=300,
#     )

#     return response.choices[0].message.content

# def whisper_transcribe(video_file):
#     model = whisper.load_model("base")
#     with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp_file:
#         tmp_file.write(video_file.read())
#         temp_file_path = tmp_file.name
#     try:
#         numpy_audio = whisper.load_audio(temp_file_path)
#         result = model.transcribe(numpy_audio, fp16=False)  # Set fp16 to False since we're using CPU

#         # print the recognized text
#         transcript = result['text']
#         segments = result['segments']
#         # language = result['language']
#         # time_stamps = [(segment['start'], segment['end']) for segment in segments]
#         time_stamps = [segment['start'] for segment in segments]
#         texts = [segment['text'] for segment in segments]
#         return transcript 
#     except Exception as e:
#         print(e)
#         return None