# Web Minio Upload

Upload files to MinIO using a web interface.


```
> web-upload -h
usage: web-upload [-h] [--serve SERVE] [--port PORT] [--debug DEBUG] [--host HOST] [--verbose VERBOSE]

Minio Web upload

options:
  -h, --help         show this help message and exit
  --serve SERVE      Serve the app
  --port PORT        Port to serve on
  --debug DEBUG      Debug mode
  --host HOST        Host to serve on
  --verbose VERBOSE  Verbose mode
```


Environment variables, or create a.env file with the following:
```
MINIO_ENDPOINT = 
MINIO_ACCESS_KEY =
MINIO_SECRET_KEY = 
MINIO_BUCKET_NAME = 
```

