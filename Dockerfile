FROM continuumio/miniconda3:latest

RUN git clone https://github.com/drg101/watercolor.git
RUN cd /watercolor/backend && conda env create -f environment.yml

RUN echo "conda activate watercolor" > ~/.bashrc
ENV PATH /opt/conda/envs/watercolor/bin:$PATH

ENTRYPOINT [ "python", "-u", "/watercolor/backend/api/app.py"]

EXPOSE 5000
