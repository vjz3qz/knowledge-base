# database_service.py
from flask_sqlalchemy import SQLAlchemy
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase.client import Client, create_client
import os


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
    data, count = (
        supabase.table("components")
        .select("*")
        .text_search("text_search_vector", query)
        .execute()
    )
    results = data[1]
    return results


def search_media(query, component_id):
    data, count = (
        supabase.table("media")
        .select("*")
        .join(
            "component_media_association",
            "media.id",
            "component_media_association.media_id",
        )
        .eq("component-media-association.component_id", component_id)
        .text_search("text_search_vector", query)
        .execute()
    )
    results = data[1]
    return results


def create_component(component_id, title, description, location):
    data, count = (
        supabase.table("components")
        .insert(
            {
                "id": component_id,
                "title": title,
                "description": description,
                "location": location,
            }
        )
        .execute()
    )


def create_media(media_id, author, title, description, component_ids):
    data, count = (
        supabase.table("media")
        .insert(
            {
                "id": media_id,
                "author": author,
                "title": title,
                "description": description,
                "image_ids": [],
                "video_ids": [],
                "document_ids": [],
            }
        )
        .execute()
    )
    for component_id in component_ids:
        data, count = (
            supabase.table("component_media_association")
            .insert(
                {
                    "media_id": media_id,
                    "component_id": component_id,
                }
            )
            .execute()
        )


def add_file_to_media(file_id, file_type, media_id):
    # add file_id to media_id's corresponding file_type array in supabase
    original_data = (
        supabase.table("media")
        .select(f"{file_type}_ids")
        .eq("id", media_id)
        .execute()
        .data
    )
    updated_data, count = (
        supabase.table("media")
        .update({file_type + "_ids": original_data.append(file_id)})
        .eq("id", media_id)
        .execute()
    )
    # split file into chunks
    docs = load_and_split(file_id, media_id, file_type)
    # set appropriate metadata for each chunk
    for doc in docs:
        doc.metadata = {
            "file_id": file_id,
            "file_type": file_type,
            "media_id": media_id,
        }
    # create embedding for file and add to supabase
    vector_store = SupabaseVectorStore.from_documents(
        docs,
        OpenAIEmbeddings(),
        client=supabase,
        table_name="embeddings",
        query_name="match_embeddings",
        chunk_size=500,
    )
    return


def get_component_by_id(component_id):
    response = supabase.table("components").select("*").eq("id", component_id).execute()
    return response


def get_media_by_id(media_id):
    response = supabase.table("media").select("*").eq("id", media_id).execute()
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
        table_name="embeddings",
        query_name="match_embeddings",
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
