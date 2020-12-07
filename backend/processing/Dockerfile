FROM continuumio/miniconda3:latest

COPY . /watercolor-processing
RUN cd /watercolor-processing && conda env create -f test/environment.yml

RUN echo "conda activate watercolor-processing" > ~/.bashrc
ENV PATH /opt/conda/envs/watercolor-processing/bin:$PATH

ENTRYPOINT [ "/opt/conda/envs/watercolor-processing/bin/python", "-u", "/watercolor-processing/process.py" ]

