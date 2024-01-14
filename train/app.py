from llama_index import VectorStoreIndex, SimpleDirectoryReader
import boto3
import os

def lambda_handler(event, context):
    BUCKET_NAME = 'fedsp-openai-train'
    key = event['Records'][0]['s3']['object']['key']
    folder_number = key.split('/')[0].replace('document','')
    LOCAL_INPUT_DIRECTORY = f'/tmp/document{folder_number}'
    LOCAL_OUTPUT_DIRECTORY = f'/tmp/storage{folder_number}'
    input_folder = f'document{folder_number}/'
    output_folder = f'storage{folder_number}/'
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=input_folder)
    os.makedirs(LOCAL_INPUT_DIRECTORY, exist_ok=True)
    objs = response['Contents']
    objs = [item['Key'] for item in objs if item['Key'][-1] != '/']
    for obj in objs:
        local_file_path = os.path.join(LOCAL_INPUT_DIRECTORY, os.path.basename(obj))
        print(BUCKET_NAME)
        print(obj)
        print(local_file_path)
        s3.download_file(BUCKET_NAME, obj, local_file_path)

    documents = SimpleDirectoryReader(LOCAL_INPUT_DIRECTORY).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(LOCAL_OUTPUT_DIRECTORY)

    for root, dirs, files in os.walk(LOCAL_OUTPUT_DIRECTORY):
        for file in files:
            local_file_path = os.path.join(root, file)
            s3.upload_file(local_file_path, BUCKET_NAME, f'{output_folder}{file}')