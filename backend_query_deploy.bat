cd query
docker build --no-cache -t fedsp_openai_query .
docker tag fedsp_openai_query:latest %ECR_REGISTRY%/fedsp_openai_query:latest
docker push %ECR_REGISTRY%/fedsp_openai_query:latest
aws lambda update-function-code --function-name fedsp_openai_query --image-uri %ECR_REGISTRY%/fedsp_openai_query:latest

cd ..