import os
import base64
import uuid
from langchain_openai import ChatOpenAI

# Initialize OpenAI
llm = ChatOpenAI(
    temperature=0.7,
    model="gpt-4o-mini",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

def save_uploaded_image(image_file):
    """
    Saves the uploaded image to the 'uploads' directory and returns the file path.
    """
    try:
        uploads_dir = os.path.join(os.getcwd(), "uploads")
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)

        image_filename = f"{uuid.uuid4()}-{image_file.filename}"
        image_path = os.path.join(uploads_dir, image_filename)
        image_file.save(image_path)
        return image_path
    except Exception as e:
        print(f"Error saving uploaded image: {e}")
        return None

def encode_image_to_base64(image_path):
    """
    Encodes the image located at the given path into a base64 string.
    """
    try:
        with open(image_path, "rb") as img_file:
            encoded_image = base64.b64encode(img_file.read()).decode("utf-8")
        return encoded_image
    except Exception as e:
        print(f"Error encoding image to base64: {e}")
        return None



def handle_fraud_detection(description, image_file, order_id):
    """
    Handles the fraud detection process by analyzing the provided description, image, and order ID.
    :param description: Text description of the issue.
    :param image_file: The uploaded image file object.
    :param order_id: The order ID provided by the user.
    :return: A JSON response with the decision or an error message.
    """
    try:
        # Step 1: Save the uploaded image
        image_path = save_uploaded_image(image_file)
        if not image_path:
            return {"error": "Failed to save the uploaded image."}

        # Step 2: Encode the image to base64
        base64_image = encode_image_to_base64(image_path)
        if not base64_image:
            return {"error": "Failed to encode the image."}

        # Truncate base64 to avoid token overload
        base64_image = base64_image[:10000]

        # Truncate description to reduce token usage
        description = description[:100]

        # Prepare the OpenAI prompt
        system_prompt = (
            "You are a customer service AI. Analyze the issue described below and the image provided. "
            "Determine if the product qualifies for:\n"
            "1. Refund Order\n"
            "2. Replace Order\n"
            "3. Escalate to Human Agent\n"
            "Provide only one of these responses."
        )

        # Prepare messages for the OpenAI API call
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Order ID: {order_id}"},
            {"role": "user", "content": f"Description: {description}"},
            {"role": "user", "content": f"Image Data (truncated): {base64_image}"}
        ]

        # Call OpenAI API
        response = llm.invoke(messages)

        # Extract and clean up the decision
        raw_decision = response.content.strip() if hasattr(response, "content") else response["content"]

        # Attempt to extract decision from longer explanation
        # Using basic pattern matching to find valid decision
        valid_decisions = ["Refund Order", "Replace Order", "Escalate to Human Agent"]
        decision = None
        for valid_decision in valid_decisions:
            if valid_decision in raw_decision:
                decision = valid_decision
                break

        # If no valid decision is found, raise an error
        if not decision:
            raise ValueError(f"Invalid decision received from OpenAI: {raw_decision}")

        return {"decision": decision}

    except Exception as e:
        print(f"Error in handle_fraud_detection: {e}")
        return {"error": "Internal server error. Please try again later."}



#
# def handle_fraud_detection(description, image_file, order_id):
#     """
#     Handles the fraud detection process by analyzing the provided description, image, and order ID.
#     :param description: Text description of the issue.
#     :param image_file: The uploaded image file object.
#     :param order_id: The order ID provided by the user.
#     :return: A JSON response with the decision or an error message.
#     """
#     try:
#         # Step 1: Save the uploaded image
#         image_path = save_uploaded_image(image_file)
#         if not image_path:
#             return {"error": "Failed to save the uploaded image."}
#
#         # Step 2: Encode the image to base64
#         base64_image = encode_image_to_base64(image_path)
#         if not base64_image:
#             return {"error": "Failed to encode the image."}
#
#         # Truncate base64 size to 300 characters to minimize token usage
#         base64_image = base64_image[:10000]
#
#         # Truncate description to reduce token usage
#         description = description[:100]  # Limit description to 100 characters
#
#         # Prepare the OpenAI prompt
#         system_prompt = (
#             "You are a customer service AI. Analyze the issue described below and the image provided. "
#             "Determine if the product qualifies for:\n"
#             "1. Refund Order\n"
#             "2. Replace Order\n"
#             "3. Escalate to Human Agent\n"
#             "Provide only one of these responses."
#         )
#
#         # Prepare messages for the OpenAI API call
#         messages = [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": f"Order ID: {order_id}"},
#             {"role": "user", "content": f"Description: {description}"},
#             {"role": "user", "content": f"Image Data (truncated): {base64_image}"}
#         ]
#
#         # Call OpenAI API
#         response = llm.invoke(messages)
#
#         # Extract decision
#         decision = response.content.strip() if hasattr(response, "content") else response.get("content", "").strip()
#
#         # Validate and extract a valid decision
#         valid_decisions = ["Refund Order", "Replace Order", "Escalate to Human Agent"]
#         for valid_decision in valid_decisions:
#             if valid_decision in decision:
#                 return {"decision": valid_decision}
#
#         # If no valid decision is found
#         raise ValueError(f"Invalid decision received from OpenAI: {decision}")
#
#     except Exception as e:
#         print(f"Error in handle_fraud_detection: {e}")
#         return {"error": "Internal server error. Please try again later."}