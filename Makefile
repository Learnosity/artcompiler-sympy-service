default: run

run:
	python3 flask_app.py

install:
	pip3 install -r requirements.txt --target ./package
	(cd package && zip -r ../function.zip .)

zip:
	zip -g function.zip lambda_function.py
	zip -g function.zip app.py

init: install zip
	aws iam create-role \
		--role-name lambda-sympy-service \
		--assume-role-policy-document file://trust-policy.json || true
	aws iam attach-role-policy \
		--role-name lambda-sympy-service \
		--policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole || true
	aws lambda create-function \
		--function-name sympy-service \
		--runtime python3.8 \
		--handler lambda_function.handler \
		--zip-file fileb://function.zip \
		--role arn:aws:iam::534897478838:role/lambda-sympy-service || true

update-function-code: zip
	aws lambda update-function-code --function-name sympy-service --zip-file fileb://function.zip

deploy: update-function-code

deploy-full: install update-function-code
