import argparse

def main(args):
    import uvicorn
    import subprocess
    
    subprocess.run(["prisma", "generate"])
    subprocess.run(["prisma", "migrate", "deploy"])
    
    uvicorn.run(
        app="app.server:app",
        host="0.0.0.0",
        port=args.port,
        reload=args.debug,
        ssl_keyfile=args.keyfile,
        ssl_certfile=args.certfile,
        workers=args.workers
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FastAPI with SSL")
    parser.add_argument("-k", "--keyfile", type=str, help="Path to SSL private key file")
    parser.add_argument("-c", "--certfile", type=str, help="Path to SSL certificate file")
    parser.add_argument("-w", "--workers", type=int, default=1, help="Number of worker processes (default: 1)")
    parser.add_argument("-p", "--port", type=int, default=8000, help="Port number (default: 8000")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode (reload on file changes)")
    args = parser.parse_args()
    main(args)