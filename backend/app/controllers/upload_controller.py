from app.utils.generate_unique_id import generate_unique_id
from docx import Document
from io import BytesIO
from app.utils.document_processor import chunk_text
import json
from app.utils.document_processor import extract_text_from_stream
from app.utils.summarize_document import summarize_document
from app.utils.vector_database_retriever import add_text_to_chroma
from app.utils.document_retriever import upload_document_to_s3, get_metadata_from_s3, get_url_from_s3, extract_text_from_s3, call_lambda_function
from app.utils.diagram_parser import serialize_to_json, deserialize_from_json, parse_results, create_text_representation
import subprocess
import tempfile
import os






# Path to the LLaVA models. Consider environment variables for production settings.
MODEL_DIR = "/Users/varunpasupuleti/Documents/TraceAI/knowledge-base/backend/models"
LLAVA_BINARY_PATH = '/Users/varunpasupuleti/Desktop/llama.cpp/llava'




def upload_file_handler(uploaded_file, llm, content_type, file_type):
    if file_type == 'text':
        text_file_handler(uploaded_file, llm, content_type)
    elif file_type == 'diagram':
        diagram_file_handler(uploaded_file, llm, content_type)


# 'text':
        
        # for each file type:
        # generate unique id with Document Level Hash
        # generate summary
        # add file to chroma
        # add file to S3 bucket: trace-ai-documents

def text_file_handler(text_file, llm, content_type):
    if content_type not in ['text/plain', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
        return 400
    elif content_type == 'text/plain':
        text, chunked_text = extract_txt_text(text_file)
    elif content_type == 'application/pdf':
        text, chunked_text = extract_pdf_text(text_file)
    elif content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        text, chunked_text = extract_docx_text(text_file)
    
    # generate unique id with Document Level Hash
    file_id = generate_unique_id(text, 'text')
    # generate summary
    summary = summarize_document(chunked_text, llm)
    # add text to chroma OR summary to chroma
    add_text_to_chroma(chunked_text, file_id)
    # add file to S3 bucket: trace-ai-documents

    metadata = {
        "name": text_file.filename,
        "summary": summary,
        "content_type": content_type,
        "file_type": "text"
    }
    upload_document_to_s3(text_file, file_id, metadata, content_type, bucket='trace-ai-knowledge-base-documents')
    return 200

def extract_txt_text(txt_file):
    # Read the text directly from the text file
    text = txt_file.read().decode('utf-8')  # assuming the text file is encoded in utf-8
    txt_file.seek(0)
    chunked_text = chunk_text(text)
    return text, chunked_text

def extract_pdf_text(pdf_file):
    # extract text from text file
    buffer = BytesIO(pdf_file.read())
    pdf_file.seek(0)
    text = extract_text_from_stream(buffer)
    chunked_text = chunk_text(text)
    return text, chunked_text

def extract_docx_text(docx_file):
    # Load the DOCX file and extract text
    doc = Document(docx_file)
    text = " ".join([p.text for p in doc.paragraphs])
    chunked_text = chunk_text(text)
    return text, chunked_text

# 'diagram':
        # for each file type:
        # generate unique id with Document Level Hash
        # generate summary: call lambda function to get class counts, bounding boxes, and confidence scores
        # create descriptive text representation of diagram: based on class counts, bounding boxes, and confidence scores
        # add text representation to chroma
        # add file to S3 bucket: trace-ai-documents




def diagram_file_handler(diagram_file, llm, content_type):
    if content_type not in ['application/pdf', 'image/jpeg', 'image/png']:
        return 400

    # Read the binary content of the file
    diagram_content = diagram_file.read()

    # Create an in-memory file-like object from the original content
    diagram_file_copy1 = BytesIO(diagram_content)
    diagram_file_copy2 = BytesIO(diagram_content)
    diagram_file_copy1.seek(0)
    diagram_file_copy2.seek(0)
    # Generate a unique ID for the PDF file or image
    if content_type == 'application/pdf':
        file_id = generate_unique_id(diagram_content, 'binary')
    else:
        file_id = generate_unique_id(diagram_content, 'image')

    # upload temporary file to S3: trace-ai-images/input-images
    upload_document_to_s3(diagram_file_copy1, file_id, content_type = content_type, bucket='trace-ai-images', prefix='input-images')

    # call lambda function to get class counts, bounding boxes, and confidence scores
    lambda_response = call_lambda_function(file_id)

    # get s3 url for image
    image_url = get_url_from_s3(file_id, bucket='trace-ai-images', prefix='input-images')

    # generate image summary
    image_summary = summarize_image(image_url)

    # get results for lambda function response
    results = json.loads(lambda_response['body']).get('results', None)

    # get class counts, bounding boxes, and confidence scores from results
    class_counts, bounding_boxes, confidence_scores = parse_results(results)

    # create descriptive text representation of diagram: based on class counts, bounding boxes, and confidence scores
    text_representation = create_text_representation(diagram_file.filename, class_counts, bounding_boxes, confidence_scores)

    # add file to chroma OR summary to chroma
    chunked_text = chunk_text(text_representation)
    add_text_to_chroma(chunked_text, file_id)

    classification_data = serialize_to_json(diagram_file.filename, class_counts, bounding_boxes, confidence_scores, results)

    metadata = {
        "name": diagram_file.filename,
        "summary": text_representation,
        "content_type": content_type,
        "file_type": "diagram"
    }

    # Convert the dictionary to a JSON string
    classification_data_string = json.dumps(classification_data)

    # Convert the JSON string to bytes
    classification_data_bytes = classification_data_string.encode('utf-8')

    # Create a file-like object from the JSON bytes
    classification_dataobj = BytesIO(classification_data_bytes)
    upload_document_to_s3(classification_dataobj, file_id, content_type='application/json', bucket='trace-ai-classification-data')
    # # add file to S3 bucket: trace-ai-knowledge-base-documents
    upload_document_to_s3(diagram_file_copy2, file_id, metadata, content_type, bucket='trace-ai-knowledge-base-documents')

    # TODO delete temporary file from S3: trace-ai-images/input-images
    # TODO upload processed image to S3: trace-ai-images/processed-images

    return 200



def draw_boxes(image, results):
    predictions = results['predictions'][0]
    boxes = predictions['output_0']
    confidences = predictions['output_1']
    class_ids = predictions['output_2']
    labels = [str(int(class_id)) for class_id in class_ids]  # Convert class IDs to string labels; adjust as needed

    for box, confidence, label in zip(boxes, confidences, labels):
        if all(v == 0.0 for v in box):  # skip boxes with all zeros
            continue
        x1, y1, x2, y2 = map(int, [box[0] * image.shape[1], box[1] * image.shape[0], box[2] * image.shape[1],
                                   box[3] * image.shape[0]])
        label_with_confidence = f"{label} ({confidence:.2f})"
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, label_with_confidence, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image



def summarize_image(image_url):
    return 0

def summarize_image_llava(diagram_file):

    extension = os.path.splitext(diagram_file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp_file:
        diagram_file.save(temp_file.name)

        # Prepare the LLaVA command
        llava_command = [
            LLAVA_BINARY_PATH,
            '-m', os.path.join(MODEL_DIR, 'ggml-model-q5_k.gguf'),
            '--mmproj', os.path.join(MODEL_DIR, 'mmproj-model-f16.gguf'),
            '--temp', '0.1',
            '-p', 'Describe the image in detail. Be specific about symbols and connections.',
            '--image', "/Users/varunpasupuleti/Documents/TraceAI/test_documents/image.jpeg"
        ]
        summary = ""
        try:
            # Run the LLaVA command
            output = subprocess.check_output(llava_command, text=True)

            # Extract the summary from the output
            summary = output.strip()
            os.unlink(temp_file.name)
        except subprocess.CalledProcessError as e:
            os.unlink(temp_file.name)
            # Handle errors in LLaVA inference
            print(f"LLaVA error: {e}")
            return 400


    return summary