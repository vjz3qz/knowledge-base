

def add_new_file(file_data, file_type, media_id):
    # generate a unique id
    file_id = generate_id()
    # if video or image, generate transcript or summary
    text = generate_text(file_data, file_type)
    # upload trace-ai bucket at <media_id>/<file_type>/<file_id>
    add_file(file_data, file_id, file_type, media_id, text)
    # add file_id to media_id's corresponding file_type array in supabase
    add_file_to_media(file_id, file_type, media_id)