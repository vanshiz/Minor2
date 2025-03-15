import os
import boto3
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image

load_dotenv()

def aws_textract_ocr(image_path: str) -> str:
    """
    Extract text from an image using AWS Textract.
    This function ensures the image is in a supported JPEG format.
    
    :param image_path: The local path to the image file.
    :return: A string containing the extracted text.
    """
  
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_default_region = os.environ.get("AWS_DEFAULT_REGION")

  
    client = boto3.client(
        'textract',
        region_name=aws_default_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

  
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

  
    try:
        with Image.open(image_path) as image:
           
            if image.format != "JPEG":
                with BytesIO() as output:
                    image.convert("RGB").save(output, format="JPEG")
                    image_bytes = output.getvalue()
            else:
                
                with open(image_path, 'rb') as f:
                    image_bytes = f.read()
    except Exception as e:
        raise Exception(f"Error processing image: {e}")

  
    response = client.detect_document_text(Document={'Bytes': image_bytes})

   
    extracted_text = []
    for item in response.get("Blocks", []):
        if item["BlockType"] == "LINE":
            extracted_text.append(item["Text"])

    return "\n".join(extracted_text)


if __name__ == "__main__": 
    image_path = r"E:\Minor2\prescription_reader\data\1.jpg"
    try:
        text = aws_textract_ocr(image_path)
        print("Extracted Text:")
        print(text)
    except Exception as e:
        print(f"An error occurred: {e}")
