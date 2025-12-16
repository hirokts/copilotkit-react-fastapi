def main() -> None:
    print("Hello from backend!")


def dev() -> None:
    import uvicorn
    uvicorn.run("backend.main:app", reload=True)
