FROM continuumio/miniconda3:latest

COPY . /watercolor-api
RUN cd /watercolor-api && conda env create -f environment.yml

RUN echo "conda activate watercolor-api" > ~/.bashrc
ENV PATH /opt/conda/envs/watercolor-api/bin:$PATH

ENTRYPOINT [ "/opt/conda/envs/watercolor-api/bin/gunicorn", "--log-level", "debug", "-t", "500", "-w", "4", "-b", "0.0.0.0:5000", "--chdir", "/watercolor-api/", "app:app" ]

EXPOSE 5000

