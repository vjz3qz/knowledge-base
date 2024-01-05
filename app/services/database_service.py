# database_service.py
from app.utils.id_generator import generate_id
from flask_sqlalchemy import SQLAlchemy
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import Client, create_client
import os
import secrets
from app.services.blob_storage_service import add_file

# TODO check if all supabase logic is correct
def init_db():
    """
    Connect to Supabase project
    """
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
    supabase: Client = create_client(supabase_url, supabase_key)
    return supabase   

supabase = init_db() 

def search_components(query):
    # TODO create combined text search vector column with title, description, and location
    data, count = supabase.table('component').select('*').text_search('text_search_vector', query).execute()
    results = data[1]
    return results

def search_media(query):
    # TODO create combined text search vector column with title, description
    data, count = supabase.table('media').select('*').text_search('text_search_vector', query).execute()
    results = data[1]
    return results

def add_file_to_media(media_id, file, file_type):
    # file_id = generate_id()
    file_id = generate_id()
    # upload trace-ai bucket at <media_id>/<file_type>/<file_id>
    add_file(file, file_id, media_id, file_type)
    # add file_id to media_id's corresponding file_type array in supabase
    original_data = supabase.table('media').select(f'{file_type}_ids').eq('id', media_id).execute().data
    updated_data, count = (supabase.table('media')
    .update({file_type+'_ids': original_data.append(file_id)})
    .eq('id', media_id)
    .execute())
    # split file into chunks
    docs = load_and_split(file_id, media_id, file_type)
    # TODO set appropriate metadata for each chunk 

    # create embedding for file and add to supabase
    vector_store = SupabaseVectorStore.from_documents(
        docs,
        OpenAIEmbeddings(),
        client=supabase,
        table_name="documents",
        query_name="match_documents",
        chunk_size=500,
    )
    return

def create_media(author, title, description, component_ids):
    media_id = generate_id()
    data, count = supabase.table('media').insert({'id': media_id,
                                                  'author': author,
                                                  'title': title,
                                                  'description': description,
                                                  'image_ids': [],
                                                  'video_ids': [],
                                                  'document_ids': [],
                                                  }).execute()
    for component_id in component_ids:
        data, count = supabase.table('component_media_association').insert({'media_id': media_id,
                                                                            'component_id': component_id,
                                                                            }).execute()
    

def create_component(title, description, location):
    component_id = generate_id()
    data, count = supabase.table('component').insert({'id': component_id,
                                                      'title': title,
                                                      'description': description,
                                                      'location': location,
                                                      }).execute()



def get_media_by_id(id):
    response = supabase.table('media').select('*').eq('id', id).execute()
    return response

def get_component_by_id(id):
    response = supabase.table('component').select('*').eq('id', id).execute()
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


# FUTURE
# list_components()
# list_media()
# update_user
# update_component
# update_media
# delete_user
# delete_component
# delete_media
