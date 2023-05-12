# Use an official Python runtime as a parent image
FROM continuumio/miniconda3

RUN apt-get --allow-releaseinfo-change update
RUN apt-get install -y build-essential 

RUN mkdir /tmp/cellmaps_ppi_embedding
COPY ./ /tmp/cellmaps_ppi_embedding/
RUN pip install /tmp/cellmaps_ppi_embedding

RUN rm -rf /tmp/cellmaps_ppi_embedding

ENTRYPOINT ["/opt/conda/bin/cellmaps_ppi_embeddingcmd.py"]

CMD ["--help"]
