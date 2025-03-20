ARG BUILD_ENV=no_copy

FROM python:3.12 AS build_no_copy

ADD ../../requirements.txt .
COPY ../.. /work
RUN rm -r /work/dist | true
RUN python -m pip install --user tox
WORKDIR /work
RUN python -m tox -e build

FROM python:3.12 AS build_copy
COPY dist /work/dist

FROM build_${BUILD_ENV} AS build

FROM python:3.12-slim
COPY --from=build /work/dist /dist
RUN python -m pip install /dist/*.whl --extra-index-url https://git.astron.nl/api/v4/projects/395/packages/pypi/simple
