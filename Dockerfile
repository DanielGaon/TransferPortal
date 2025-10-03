FROM alpine:3.20
RUN apk update
RUN apk add python3
RUN apk add py3-pip
WORKDIR /transferportal
COPY requirements.txt .
COPY Transfer_Portal.py .
COPY static static/
RUN python3 -m venv portalenv
ENV PATH="/transferportal/portalenv/bin:$PATH"
RUN pip install -r requirements.txt
EXPOSE 8080
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8080 || exit 1
CMD ["python3", "Transfer_Portal.py"]
