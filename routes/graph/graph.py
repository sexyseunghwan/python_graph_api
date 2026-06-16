from flask import Blueprint

from routes.graph.graph_service import (
    test_response,
    category_image_response,
    consume_detail_response,
    asset_pie_image_response,
)

graph_bp = Blueprint('graph', __name__)

@graph_bp.route('/api/test', methods=['GET'])
def test_app():
    return test_response()

@graph_bp.route('/api/category', methods=['POST'])
def category_app():
    return category_image_response()

@graph_bp.route('/api/consume_detail', methods=['POST'])
def consume_detail_app():
    return consume_detail_response()

@graph_bp.route('/api/asset_pie_image_app', methods=['POST'])
def asset_pie_image_app():
    return asset_pie_image_response()
