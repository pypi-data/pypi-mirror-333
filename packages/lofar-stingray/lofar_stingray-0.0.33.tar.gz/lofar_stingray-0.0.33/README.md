# Stingray

![Build status](git.astron.nl/lofar2.0/stingray/badges/main/pipeline.svg)
![Test coverage](git.astron.nl/lofar2.0/stingray/badges/main/coverage.svg)
<!-- ![Latest release](https://git.astron.nl/templates/python-package/badges/main/release.svg) -->

Station statistics gather and dump utility, writes station statistics contiously to the local S3 based object storage.
## Installation

```
pip install .
```

## Usage

To forward (copy) statistics packets, metadata, or matrices from one place to another, use the following command:

```bash
l2ss-stingray-forward <source> <destination> --datatype=packet|json
```

These locations are supported for ``source`` and ``destionation``:

* ``file:<path>``: read/write from a file on disk,
* ``tcp://<host>:<port>``: receive from/write to a TCP server,
* ``udp://<host>:<port>``: receive on/write to a UDP server,
* ``s3://<host>/<bucket>/<path>``: write to an S3 store as JSON (destination only),
* ``zmq+tcp://<host>:<port>/<topic>``: subscribe to ZMQ server and topic (source only),

The ``packet`` datatype is used to process (binary) statistics packets from SDP, and the ``json`` datatype
is used to process lines of JSON, the encoding used for metadata and matrices.

To convert statistics packets into matrices and publish those using ZMQ, use the following command:

```bash
l2ss-stingray-publish <station> <antennafield> <type> <source>
```

To extract a set of matrices from disk, annotate them with metadata, and write them as HDF5 files, use:

```bash
l2ss-stingray-extract <station> <antennafield> <type> <from> <to> <source> <destination>
```

## Example

The following commands, when started in parallel in the order listed, will convert the XST packets in ``tests/xst-packets.bin`` to JSON matrices in ``xst-matrices.txt``:

```bash
# start converter & publisher
l2ss-stingray-publish cs123 hba xst udp://0:5000

# catch output of publisher
l2ss-stingray-forward -d json 'zmq+tcp://localhost:6001/xst?content_type=application/json' file:xst-matrices.txt

# provide input to converter
l2ss-stingray-forward file:tests/xst-packets.bin udp://127.0.0.1:5000
```

## Contributing

To contribute, please create a feature branch and a "Draft" merge request.
Upon completion, the merge request should be marked as ready and a reviewer
should be assigned.

Verify your changes locally and be sure to add tests. Verifying local
changes is done through `tox`.

```pip install tox```

With tox the same jobs as run on the CI/CD pipeline can be run. These
include unit tests and linting.

```tox```

To automatically apply most suggested linting changes execute:

```tox -e format```

## License
This project is licensed under the Apache License Version 2.0
