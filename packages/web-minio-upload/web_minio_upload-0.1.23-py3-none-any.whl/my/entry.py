import argparse
import web.app


def main():
    parser = argparse.ArgumentParser(description="Minio Web upload")
    parser.add_argument("--serve", action="store", default=False, help="Serve the app")
    parser.add_argument("--port", type=int, default=5000, help="Port to serve on")
    parser.add_argument("--debug", action="store", default=False, help="Debug mode")
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Host to serve on"
    )
    parser.add_argument("--verbose", action="store", default=False, help="Verbose mode")

    args = parser.parse_args()
    web.app.main(args.host, args.port, debug=args.debug)


if __name__ == "__main__":
    main()
