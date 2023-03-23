# Use an official Python runtime as a parent image
FROM continuumio/miniconda2

RUN apt-get --allow-releaseinfo-change update
RUN apt-get install -y build-essential 

RUN pip install networkx==1.11
RUN pip install scipy==1.2.3
RUN pip install numpy==1.11.2
RUN pip install smart-open==1.11.1
RUN pip install gensim==0.13.3
RUN pip install pathlib==1.0.1
RUN pip install urllib3==1.26.7
RUN pip install backports-abc==0.5
RUN pip install backports.functools-lru-cache==1.6.4
RUN pip install backports.shutil-get-terminal-size==1.0.0
RUN pip install boto==2.49.0
RUN pip install boto3==1.17.112
RUN pip install botocore==1.20.112
RUN pip install bz2file==0.98
RUN pip install certifi==2020.6.20
RUN pip install chardet==4.0.0
RUN pip install decorator==4.4.2
RUN pip install enum34==1.1.10
RUN pip install futures==3.3.0
RUN pip install gensim==0.13.3
RUN pip install idna==2.10
RUN pip install ipykernel==4.10.1
RUN pip install ipython==5.10.0
RUN pip install ipython-genutils==0.2.0
RUN pip install jmespath==0.10.0
RUN pip install jupyter-client==5.3.5
RUN pip install jupyter-core==4.6.3
RUN pip install networkx==1.11
RUN pip install numpy==1.11.2
RUN pip install pathlib2==2.3.6
RUN pip install pexpect==4.8.0
RUN pip install pickleshare==0.7.5
RUN pip install prompt-toolkit==1.0.18
RUN pip install ptyprocess==0.7.0
RUN pip install Pygments==2.5.2
RUN pip install python-dateutil==2.8.2
RUN pip install pyzmq==19.0.2
RUN pip install requests==2.26.0
RUN pip install s3transfer==0.4.2
RUN pip install scandir==1.10.0
RUN pip install scipy==1.2.3
RUN pip install simplegeneric==0.8.1
RUN pip install singledispatch==3.7.0
RUN pip install six==1.16.0
RUN pip install smart-open==1.10.1
RUN pip install tornado==5.1.1
RUN pip install traitlets==4.3.3
RUN pip install urllib3==1.26.7
RUN pip install wcwidth==0.2.5

RUN mkdir /tmp/cellmaps_network_embedding
COPY ./ /tmp/cellmaps_network_embedding/
RUN pip install /tmp/cellmaps_network_embedding

RUN rm -rf /tmp/cellmaps_network_embedding

RUN cd /opt ;git clone https://github.com/aditya-grover/node2vec.git
RUN cd /opt/node2vec; git checkout 883241e825e1473ef9916ac79f6686f5ef6b1603

ENTRYPOINT ["/opt/conda/bin/cellmaps_network_embeddingcmd.py"]

CMD ["--help"]
