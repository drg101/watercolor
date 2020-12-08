FROM continuumio/miniconda3:latest

COPY . /watercolor-processing
RUN cd /watercolor-processing && conda env create -f environment.yml
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN echo "conda activate watercolor-processing" > ~/.bashrc
ENV PATH /opt/conda/envs/watercolor-processing/bin:$PATH

ENTRYPOINT [ "/opt/conda/envs/watercolor-processing/bin/python", "-u", "/watercolor-processing/process.py" ]

