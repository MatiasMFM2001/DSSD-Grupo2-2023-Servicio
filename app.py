# app.py
from flask import Flask
from src.web import create_app
from pathlib import Path

app = create_app(static_folder=Path(__file__).parent.joinpath("public"))

if __name__ == "__main__":
    app.run()
