FROM python:3
MAINTAINER l-acs

WORKDIR /usr/src/app

COPY ./pip_requirements pip_requirements
RUN pip install --no-cache-dir -r pip_requirements

COPY . ./
EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["./streamlit.py"]


# docker build -t pytree .
# docker run -p 8501:8501 pytree
