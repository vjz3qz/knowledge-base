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
        return
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
        "content_type": content_type
    }
    upload_document_to_s3(text_file, file_id, metadata, content_type, bucket='trace-ai-knowledge-base-documents')


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
        return
    # Read the binary content of the file
    diagram_content = diagram_file.read()
    diagram_file.seek(0)
    # Generate a unique ID for the PDF file or image
    if content_type == 'application/pdf':
        file_id = generate_unique_id(diagram_content, 'binary')
    else:
        file_id = generate_unique_id(diagram_content, 'image')

    # upload temporary file to S3: trace-ai-images/input-images
    upload_document_to_s3(diagram_file, file_id, bucket='trace-ai-images', prefix='input-images')

    # generate summary: call lambda function to get class counts, bounding boxes, and confidence scores
    lambda_response = call_lambda_function(file_id)

    # get results for lambda function response
    results = json.loads(lambda_response['body']).get('results', None)

    # get class counts, bounding boxes, and confidence scores from results
    class_counts, bounding_boxes, confidence_scores = parse_results(results)

    # create descriptive text representation of diagram: based on class counts, bounding boxes, and confidence scores
    text_representation = create_text_representation(diagram_file.filename, class_counts, bounding_boxes, confidence_scores)

    # add file to chroma OR summary to chroma
    add_text_to_chroma(text_representation, file_id)

    classification_data = serialize_to_json(diagram_file.filename, class_counts, bounding_boxes, confidence_scores, results)

    metadata = {
        "name": diagram_file.filename,
        "summary": text_representation,
        "classification_data": classification_data,
        "content_type": content_type
    }
    # add file to S3 bucket: trace-ai-knowledge-base-documents
    upload_document_to_s3(diagram_file, file_id, metadata, content_type, bucket='trace-ai-knowledge-base-documents')

    # TODO delete temporary file from S3: trace-ai-images/input-images





