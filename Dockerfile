FROM public.ecr.aws/lambda/python:3.11

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

COPY ./src ${LAMBDA_TASK_ROOT}/src

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY api.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "api.handler" ]