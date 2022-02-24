FROM python:3
MAINTAINER l-acs

WORKDIR /usr/src/app

COPY ./config/pip_requirements pip_requirements
RUN pip install --no-cache-dir -r pip_requirements

COPY . ./
RUN mkdir -p .streamlit
COPY config/config.toml .streamlit/

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["--server.port", "8501", "./streamlit.py"]


# docker build -t pytree .
# docker run -d -p 8501:8501 --restart always pytree
