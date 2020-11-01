FROM continuumio/miniconda3:latest

RUN git clone https://github.com/drg101/watercolor.git
RUN cd /watercolor/backend && conda env create -f environment.yml

SHELL ["conda", "run", "-n", "watercolor", "/bin/bash", "-c"]

ENTRYPOINT ["conda", "run", "-n", "watercolor", "python", "/watercolor/backend/api/app.py"]

EXPOSE 5000
