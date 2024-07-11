install:
	pip install -r requirements.txt
login:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 478259563916.dkr.ecr.us-east-1.amazonaws.com
docker:
	docker build -t awsservices .
tag:
	docker tag awsservices:agentebi 478259563916.dkr.ecr.us-east-1.amazonaws.com/awsservices:agentebi
push: 
	docker push 478259563916.dkr.ecr.us-east-1.amazonaws.com/awsservices:agentebi
run: login docker tag push
