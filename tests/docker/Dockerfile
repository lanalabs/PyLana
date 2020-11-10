FROM python:3.8-slim

RUN useradd -m -s /bin/bash  pylana-tester
USER pylana-tester
WORKDIR /home/pylana-tester/
ENV PATH="/home/pylana-tester/.local/bin:${PATH}"
RUN pip install pylana==0.2.1

RUN pip install pytest

COPY --chown=pylana-tester ./tests ./tests/
COPY --chown=pylana-tester ["pytest.ini", "./tests/docker/entrypoint.sh", "./"]

ENV SCHEME https
ENV HOST cloud-backend.lanalabs.com
ENV PORT 443

ENV TOKEN_USER ""
ENV TOKEN_USERADMIN ""

ENTRYPOINT ["./entrypoint.sh"]
