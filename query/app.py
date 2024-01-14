import json
from llama_index import StorageContext, load_index_from_storage
from llama_index import StorageContext, load_index_from_storage
import boto3
import os

query_engine = {}
for folder_number in ['1', '2', '3']:
    BUCKET_NAME = 'fedsp-openai-train'
    LOCAL_EMBEDDING_DIRECTORY = '/tmp/embeddings/'
    s3 = boto3.client('s3')
    
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix='storage')
    objects = response['Contents']
    objects = [item['Key'] for item in objects if item['Key'][-1] != '/']
    
    os.makedirs(LOCAL_EMBEDDING_DIRECTORY, exist_ok=True)
    
    for obj in objects:
        local_file_path = os.path.join(LOCAL_EMBEDDING_DIRECTORY, obj)
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        s3.download_file(BUCKET_NAME, obj, local_file_path)

    storage_context = StorageContext.from_defaults(persist_dir=f"{LOCAL_EMBEDDING_DIRECTORY}storage{folder_number}") 
    index = load_index_from_storage(storage_context)
    query_engine[f'content{folder_number}'] = index.as_query_engine()

def lambda_handler(event, context):
    print(event)
    error_response =  {
        "statusCode": 400,
        "body": json.dumps({"message": "Invalid Request"}),
        "headers": {
            "Content-Type": "application/json"
        }
    }
    try:
        method = event['requestContext']['http']['method']
        if method != 'POST':
            raise('NOT POST')
        body = json.loads(event['body'])
        folder_number = body['FolderNumber']
        query_text = body['Query']
    except Exception as e:
        err = {
            "statusCode": 400,
            "body": "Invalid request",
            "headers": {
                "Content-Type": "application/json"
            }
        }
        return err

    query_response = query_engine[f'content{folder_number}'].query(query_text).response
    success_response =  {
        "statusCode": 200,
        "body": json.dumps({"message": query_response}),
        "headers": {
            "Content-Type": "application/json"
        }
    }
    return success_response