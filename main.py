import argparse

def main(args):
    import uvicorn
    import subprocess
    
    if args.prisma:
        subprocess.run(["prisma", "generate"])
    
    uvicorn.run(
        app="app.server:app",
        host="0.0.0.0",
        port=args.port,
        reload=args.debug,
        ssl_keyfile=args.keyfile,
        ssl_certfile=args.certfile,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FastAPI with SSL")
    parser.add_argument("--keyfile", type=str, help="Path to SSL private key file")
    parser.add_argument("--certfile", type=str, help="Path to SSL certificate file")
    parser.add_argument("--port", type=int, default=8000, help="Default port is 8000")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--prisma", action="store_true", help="Generate prisma schema")
    args = parser.parse_args()
    main(args)