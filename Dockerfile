FROM python:3.9.7-slim-buster

ENV FLYWHEEL="/flywheel/v0"
WORKDIR ${FLYWHEEL}

RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean

# install main dependenices
RUN pip install histomicstk --find-links https://girder.github.io/large_image_wheels
RUN pip install flywheel_gear_toolkit
RUN pip install fw_core_client
RUN pip install flywheel-sdk

# copy main files into working directory
COPY run.py manifest.json $FLYWHEEL/
COPY fw_gear_tile_wsi ${FLYWHEEL}/fw_gear_tile_wsi 
COPY ./ $FLYWHEEL/

# start the pipeline
RUN chmod a+x $FLYWHEEL/run.py
RUN chmod -R 777 .
ENTRYPOINT ["python","/flywheel/v0/run.py"]
