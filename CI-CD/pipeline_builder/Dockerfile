FROM python:3.10.7-slim
ADD pipeline_execution.py /home/pipeline_execution.py
ADD requirements.txt ./
RUN pip install -r requirements.txt
ENTRYPOINT ["python","/home/pipeline_execution.py"]