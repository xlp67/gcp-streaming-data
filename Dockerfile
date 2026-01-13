FROM gcr.io/dataflow-templates-base/python311-template-launcher-base

ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="/template/requirements.txt"

ENV FLEX_TEMPLATE_PYTHON_PY_FILE="/template/main.py"

WORKDIR /template

COPY . /template/

RUN pip install --no-cache-dir -U -r /template/requirements.txt
