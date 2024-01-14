cd train
docker build --no-cache -t fedsp_openai_train .
docker tag fedsp_openai_train:latest %ECR_REGISTRY%/fedsp_openai_train:latest
docker push %ECR_REGISTRY%/fedsp_openai_train:latest
aws lambda update-function-code --function-name fedsp_openai_train --image-uri %ECR_REGISTRY%/fedsp_openai_train:latest

cd ..