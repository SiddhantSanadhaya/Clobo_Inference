import db

def mock_image_classification(image_data: bytes) -> str:
    """Mock image classification model function."""
    # Simulate model inference (this is a placeholder)
    # In a real scenario, load the model and process the image data here
    return "cat"  # Mock result, replace with actual model inference result

def process_image(image_data: bytes, image_id: str):
    """Process the image and update the result in the database."""
    # Call the image classification model
    result = mock_image_classification(image_data)
    
    # Save the result in the database
    db.update_result(image_id, result)
