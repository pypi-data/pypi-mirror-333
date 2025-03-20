ARG BUILD_ENV=no_copy
ARG PIP_EXTRA_INDEX_URL=https://git.astron.nl/api/v4/projects/772/packages/pypi/simple
FROM python:3.13 AS build_no_copy

ADD ../../requirements.txt .
COPY ../.. /work
RUN rm -r /work/dist | true

RUN python -m pip install --user tox
WORKDIR /work
ENV PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL}
RUN python -m tox -e build

FROM python:3.13 AS build_copy
COPY dist /work/dist

FROM build_${BUILD_ENV} AS build

FROM python:3.13-slim
COPY --from=build /work/dist /dist

ARG PIP_EXTRA_INDEX_URL
ENV PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL}
RUN python -m pip install /dist/*.whl
