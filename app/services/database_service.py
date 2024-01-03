# database_service.py
from app.utils.id_generator import generate_id
from flask_sqlalchemy import SQLAlchemy
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import Client, create_client
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
import os
import secrets

db = SQLAlchemy()

media_component_association = db.Table('media_component_association',
    db.Column('media_id', db.BIGINT, db.ForeignKey('media.id'), primary_key=True),
    db.Column('component_id', db.BIGINT, db.ForeignKey('component.id'), primary_key=True)
)

def init_db():
    """
    Connect to Supabase project
    """
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
    supabase: Client = create_client(supabase_url, supabase_key)
    return supabase   

supabase = init_db() 

def search_components():
    pass

def search_media(query):
    pass

# get_media_by_id(id)
# get_component_by_id(id)

# create_component(title, description, location)
# create_media(author, title, description, component_ids, document_ids, image_ids, video_ids)

def add_file_to_media(media_id, file, file_type):
    # file_id = generate_id()
    # add file_id to media_id's corresponding file_type array in supabase
    # upload trace-ai bucket at <media_id>/<file_type>/<file_id>
    # create embedding for file
    # add embedding to supabase
    file_id = generate_id()
    original_data = supabase.table('media').select(f'{file_type}_ids').eq('id', media_id).execute().data
    updated_data, count = (supabase.table('media')
    .update({file_type+'_ids': original_data.append(file_id)})
    .eq('id', media_id)
    .execute())

    # create embeddings for the file

    embeddings = OpenAIEmbeddings()
    loader = TextLoader("../../modules/state_of_the_union.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    
    vector_store = SupabaseVectorStore.from_documents(
        docs,
        embeddings,
        client=supabase,
        table_name="documents",
        query_name="match_documents",
        chunk_size=500,
    )
    
    return

def create_media(author, title, description, component_ids):
    id = generate_id()
    text_search_vector = []
    data, count = supabase.table('media').insert({'id': id,
                                                  'author': author,
                                                  'title': title,
                                                  'description': description,
                                                  'image_ids': [],
                                                  'video_ids': [],
                                                  'document_ids': [],
                                                  'text_search_vector':text_search_vector,
                                                  }).execute()
    # update association table which maps component ids to media id
    
def get_media_by_id(id):
    response = supabase.table('media').select('*').eq('id', id).execute()
    return response

def similarity_search(query):
    """
    Semantically searches database for matching text based on embeddings

    Parameters:
    -----------
    query : string
        user query

    Returns:
    --------
    List[Documents]
        Matched docs based on user query
    """
    embeddings = OpenAIEmbeddings()
    vector_store = SupabaseVectorStore(
        embedding=embeddings,
        client=supabase,
        table_name="documents",
        query_name="match_documents",
    )
    matched_docs = vector_store.similarity_search(query)
    return matched_docs

