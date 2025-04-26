ARG UV_VERSION=0.6.17
ARG PYTHON_VERSION=3.13

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install -y \
  git gcc build-essential openssh-client less mandoc jq yq zip locales --fix-missing --no-install-recommends \
  && apt-get clean

RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen
RUN locale-gen

RUN useradd -ms /bin/bash vscode
WORKDIR /workspace

RUN chown -R vscode:vscode /workspace
USER vscode

ENV UV_LINK_MODE=copy
COPY --from=uv /uv /uvx /bin/

RUN pip install --upgrade pip

RUN curl https://github.com/git/git/blob/master/contrib/completion/git-completion.bash -o ~/.git-completion.bash

RUN cat <<EOF >> ~/.bashrc

if [ -f ~/.git-completion.bash ]; then
  . ~/.git-completion.bash
fi
EOF

CMD [ "sleep", "infinity" ]
