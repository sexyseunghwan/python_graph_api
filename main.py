"""
Author      : Seunghwan Shin
Create date : 2023-05-01
Description : Code that can perform various functions through Telegram

History     : 2026-06-16 Seunghwan Shin       # [v.1.0.0] first create
"""

import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask
from matplotlib import font_manager
import matplotlib.pyplot as plt

from routes.graph import graph_bp


def create_app() -> Flask:
    app = Flask(__name__)

    font_prop = font_manager.FontProperties(fname="./data/font/BMDOHYEON_ttf.ttf").get_name()
    plt.rc('font', family=font_prop)

    app.register_blueprint(graph_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv('RUNNING_PORT', '5000'))
    app.run(debug=True, port=port)
