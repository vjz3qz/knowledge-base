import json
from collections import Counter

def parse_results(results):
    predictions = results['predictions'][0]
    boxes = predictions['output_0']
    confidences = predictions['output_1']
    class_ids = predictions['output_2']

    class_counts = Counter(class_ids)

    # Extract bounding boxes and confidence scores
    bounding_boxes = [
        {'x1': box[0], 'y1': box[1], 'x2': box[2], 'y2': box[3]} for box in boxes
    ]
    confidence_scores = confidences

    return dict(class_counts), bounding_boxes, confidence_scores


def create_text_representation(file_name, class_counts, bounding_boxes, confidence_scores):
    # Sort the classes by count
    sorted_classes = sorted(class_counts.items(), key=lambda item: item[1], reverse=True)
    
    # Create a description for class counts
    class_descriptions = [f"{count} instances of class {cls}" for cls, count in sorted_classes]
    class_text = ", ".join(class_descriptions)
    
    # Add information about bounding boxes
    boxes_text = "Bounding boxes have been identified with confidences: " + ", ".join(f"{score:.2f}" for score in confidence_scores)
    
    # Combine both descriptions
    text_representation = f"The diagram,{file_name}, includes {class_text}. {boxes_text}."
    
    return text_representation

def serialize_to_json(file_name, class_counts, bounding_boxes, confidence_scores, results):
    # Create a dictionary of all the data
    data = {
        "file_name": file_name,
        "class_counts": class_counts,
        "bounding_boxes": bounding_boxes,
        "confidence_scores": confidence_scores,
        "results": results 
    }
    
    # Convert the dictionary to a JSON string
    json_string = json.dumps(data, indent=2)
    return json_string


def deserialize_from_json(json_string):
    # Parse the JSON string back into a Python dictionary
    data = json.loads(json_string)
    
    # Extract the data
    file_name = data["file_name"]
    class_counts = data["class_counts"]
    bounding_boxes = data["bounding_boxes"]
    confidence_scores = data["confidence_scores"]
    results = data["results"] 
    
    return file_name, class_counts, bounding_boxes, confidence_scores, results
