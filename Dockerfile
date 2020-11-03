FROM continuumio/miniconda3:latest

COPY ./backend /watercolor
RUN cd /watercolor && conda env create -f environment.yml

RUN echo "conda activate watercolor" > ~/.bashrc
ENV PATH /opt/conda/envs/watercolor/bin:$PATH

ENTRYPOINT [ "/opt/conda/envs/watercolor/bin/gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--chdir", "/watercolor/api/", "app:app" ]

EXPOSE 5000
