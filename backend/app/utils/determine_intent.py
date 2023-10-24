def determine_intent(message):
    # Check for question
    if message.endswith('?'):
        return 'question'
    
    # Check for common terms related to summarization
    summarization_terms = ['summarize', 'overview', 'brief me', 'tell me about']
    if any(term in message.lower() for term in summarization_terms):
        return 'summarize'
    
    # Default to question if no clear intent is determined
    return 'question'