image_name=360844283138.dkr.ecr.us-east-1.amazonaws.com/create-branch-from-issue:latest

dev:
	docker-compose up app

deploy:
	docker build -t $(image_name) .
	`aws ecr get-login --no-include-email`
	docker push $(image_name)
	python deploy.py
