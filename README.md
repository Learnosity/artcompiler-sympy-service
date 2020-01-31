# sympy-artcompiler

This repository contains a simple web API for Sympy.

# Development
This runs a local flask server
```bash
make
```

# AWS Lambda

## Intialize
This installs `flask` and `sympy` into the `./package` directory and creates the lambda function
```bash
make init
# You may have to run twice if you get this error:
# "An error occurred (InvalidParameterValueException) when calling the CreateFunction operation: The role defined for the function cannot be assumed by Lambda."
```

## Update
This updates the AWS Lambda function code
```bash
make deploy
```
