import weaviate
import json
import os 

from dotenv import load_dotenv
load_dotenv()

# create a .env file in this dir and change to your keys
# WEAVIATE_CLUSTER_URL=https://dummy-weaviate.network
# YOUR-WEAVIATE-API-KEY=dummyweaviateapikey12345
# X-HuggingFace-Api-Key=dummyhuggingfaceapikey12345



client = weaviate.Client(
    url = os.getenv('WEAVIATE_CLUSTER_URL'),  # Replace with your endpoint
    auth_client_secret=weaviate.AuthApiKey(api_key=os.getenv('YOUR-WEAVIATE-API-KEY')),  # Replace w/ your Weaviate instance API key
    additional_headers = {
        "X-HuggingFace-Api-Key": os.getenv('X-HuggingFace-Api-Key')  # Replace with your inference API key
    }
)


nearText = {"concepts": ["biology"]}

response = (
    client.query
    .get("Question", ["question", "answer", "category"])
    .with_near_text(nearText)
    .with_limit(2)
    .do()
)

print(json.dumps(response, indent=4))