FROM fedora:36

# Add worker user
RUN mkdir /builds && \
    useradd -d /builds/worker -s /bin/bash -m worker && \
    chown worker:worker /builds/worker && \
    mkdir /builds/worker/artifacts && \
    chown worker:worker /builds/worker/artifacts

RUN mkdir -p /builds/worker/artifacts

WORKDIR /builds/worker/

#-------------------------------------------------------------------------------
#-- Configuration --------------------------------------------------------------
#-------------------------------------------------------------------------------

# %include-run-task

ENV SHELL=/bin/bash \
    HOME=/builds/worker \
    PATH="/builds/worker/.local/bin:$PATH"

RUN yum -y install python3 python3-pip python3-yaml git wget zip

# RPM packaging dependencies
RUN yum -y install rpm-build rpmdevtools yum-utils which ccache cargo

#-------------------------------------------------------------------------------
#-- Checkout Cache -------------------------------------------------------------
#-------------------------------------------------------------------------------

VOLUME /builds/worker/checkouts
VOLUME /builds/worker/.cache

USER root
