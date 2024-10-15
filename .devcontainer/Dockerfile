FROM python:3.11

RUN apt-get update && apt-get install -y \
  git gcc build-essential openssh-client --fix-missing --no-install-recommends \
  && apt-get clean

RUN useradd -ms /bin/bash vscode
USER vscode

WORKDIR /workspace
RUN chown -R vscode:vscode /workspace

RUN pip install --upgrade pip
RUN pip install pre-commit virtualenv

CMD [ "sleep", "infinity" ]
