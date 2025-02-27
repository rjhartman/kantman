# Base Image
FROM ubuntu:24.04

# Copy project to working directory and CD to it
COPY . /kantman
WORKDIR /kantman

# Setup noninteractive env vars for dependencies
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Chicago
ENV READTHEDOCS=true

# Run scripts/init.sh
RUN "scripts/init.sh"

CMD [ "make", "python-deps" ]