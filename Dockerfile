FROM alpine:3.20
RUN apk update
RUN apk add python3
RUN apk add py3-pip
WORKDIR /transportal
COPY requirements.txt .
COPY Transfer_Portal.py .
COPY static static/
RUN python3 -m venv portalenv
ENV PATH="/transportal/portalenv/bin:$PATH"
RUN pip install -r requirements.txt
CMD ["python3", "Transfer_Portal.py"]