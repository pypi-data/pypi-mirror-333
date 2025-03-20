import asyncio
from .server import SketchupMCPServer

async def main():
    server = SketchupMCPServer()
    try:
        await server.start()
    except KeyboardInterrupt:
        print("\nShutting down server...")

if __name__ == "__main__":
    asyncio.run(main()) 