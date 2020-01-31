default: run

run:
	python3 app.py

install:
	pip3 install -r requirements.txt --target ./package

zip:
	(cd package && zip -r ../function.zip .)
	zip -g function.zip lambda_function.py

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

deploy: install zip
	aws lambda update-function-code \
		--function-name sympy-service \
		--zip-file fileb://function.zip
