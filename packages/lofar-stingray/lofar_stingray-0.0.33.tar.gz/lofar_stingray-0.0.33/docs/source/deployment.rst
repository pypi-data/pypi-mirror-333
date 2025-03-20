Deployment / Infrastructure
----------------------------

Stingray is deployed as containers running on the station.
For each statistic type (XST, SST, BST) and each antenna field, one container instance is running.

Each container is receiving the statistics packets for a specific type and antenna field via TCP,
recording them in chunks of up to 5 minutes and writing the result JSON encoded to a S3 bucket.

The bucket is located on the stations MinIO instance and configured to replicate the individual objects
to the central MinIO instance. To reduce the risk of data loss the objects are stored on the station for 24 hours.

.. image:: infrastructure.png

