FROM python:3.10

RUN \
  apt-get update -y && \
  apt-get install -y apt-utils 2>&1 | grep -v "debconf: delaying package configuration, since apt-utils is not installed"
RUN apt-get install -y --no-install-recommends \
  netcat-traditional \
  tzdata \
  make
# netcat - package for nc command
# tzdata - package for setting timezone
# make - package for running Makefile (needed for automated checks)

WORKDIR /app

CMD ["/tools/run-development.sh"]
