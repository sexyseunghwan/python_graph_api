from decimal import Decimal, InvalidOperation
from io import BytesIO

from flask import request, jsonify, send_file

from config import logger
from models.assets import Assets, AssetResp
from models.consume import ConsumeInfo
from utils.matplot_util import (
    visualize_consume_res_by_category,
    draw_line_graph_single,
    draw_line_graph_dual,
    draw_asset_pie_graph,
)


def test_response():
    try:
        data = _get_json_object()
        test = _get_required_field(data, "test")
    except ValueError as e:
        return _bad_request(str(e))

    logger.info(f"test: {test}")
    return "test", 200


def category_image_response():
    try:
        data = _get_json_object()
        category_labels = _get_required_field(data, "prodt_type_vec")
        category_size_labels = _get_required_field(data, "prodt_type_cost_per_vec")
        start_dt = _get_required_field(data, "start_dt")
        end_dt = _get_required_field(data, "end_dt")
        total_cost = _get_required_field(data, "total_cost")
    except ValueError as e:
        return _bad_request(str(e))

    image_buffer = BytesIO()
    visualize_consume_res_by_category(
        category_labels,
        category_size_labels,
        start_dt,
        end_dt,
        total_cost,
        image_buffer,
    )
    return _send_png(image_buffer, 'category_img.png')


def consume_detail_response():
    data = request.get_json(silent=True)

    if not isinstance(data, list) or len(data) > 2:
        return _bad_request('Request body must be a JSON array of at most 2 items.')

    cur_consume_info: ConsumeInfo | None = None
    pre_consume_info: ConsumeInfo | None = None

    for elem in data:
        if not isinstance(elem, dict):
            return _bad_request('Each consume detail item must be a JSON object.')

        try:
            consume_info = ConsumeInfo(
                total_cost=_get_required_field(elem, 'total_cost'),
                start_date=_get_required_field(elem, 'start_dt'),
                end_date=_get_required_field(elem, 'end_dt'),
                consume_res_list=_get_required_field(elem, 'consume_accumulate_list'),
            )
            line_type = _get_required_field(elem, 'line_type')
        except ValueError as e:
            return _bad_request(str(e))

        if line_type == "cur":
            cur_consume_info = consume_info
        else:
            pre_consume_info = consume_info

    if cur_consume_info is None:
        return _bad_request('Missing required item with line_type "cur".')

    image_buffer = BytesIO()

    if pre_consume_info is None:
        draw_line_graph_single(cur_consume_info, image_buffer)
    else:
        draw_line_graph_dual(cur_consume_info, pre_consume_info, image_buffer)

    return _send_png(image_buffer, 'consume_detail.png')


def asset_pie_image_response():
    try:
        data = _get_json_object()
        assets = _to_assets(data)
    except ValueError as e:
        return _bad_request(str(e))

    category_amounts = _sum_asset_amounts_by_category(assets)
    if not category_amounts:
        return jsonify({'message': 'No asset data to visualize.'}), 200

    image_buffer = BytesIO()
    draw_asset_pie_graph(
        list(category_amounts.keys()),
        [float(amount) for amount in category_amounts.values()],
        assets.total_asset_amount_krw,
        image_buffer,
    )
    return _send_png(image_buffer, 'asset_pie.png')


def _bad_request(message: str):
    return jsonify({'error': message}), 400


def _send_png(image_buffer: BytesIO, download_name: str):
    image_buffer.seek(0)
    return send_file(
        image_buffer,
        mimetype='image/png',
        as_attachment=False,
        download_name=download_name,
    )


def _get_json_object() -> dict:
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError('Request body must be a JSON object.')
    return data


def _get_required_field(data: dict, field_name: str):
    if field_name not in data:
        raise ValueError(f'Missing required field: {field_name}.')
    return data[field_name]


def _to_decimal(value, field_name: str) -> Decimal:
    if value is None:
        return Decimal("0")

    try:
        return Decimal(str(value))
    except InvalidOperation as e:
        raise ValueError(f'Invalid decimal field: {field_name}.') from e


def _to_asset_resp(data: dict) -> AssetResp:
    if not isinstance(data, dict):
        raise ValueError('AssetResp item must be a JSON object.')

    return AssetResp(
        asset_type=_get_required_field(data, "asset_type"),
        asset_name=_get_required_field(data, "asset_name"),
        asset_krw=_to_decimal(_get_required_field(data, "asset_krw"), "asset_krw"),
        asset_usd=_to_decimal(_get_required_field(data, "asset_usd"), "asset_usd"),
    )


def _to_asset_resp_map(data: dict) -> dict[str, list[AssetResp]]:
    if not isinstance(data, dict):
        raise ValueError('Field asset_map must be a JSON object.')

    asset_resp_map: dict[str, list[AssetResp]] = {}
    for asset_type, asset_resps in data.items():
        if asset_resps is None:
            continue

        if not isinstance(asset_resps, list):
            raise ValueError(f'Field asset_map.{asset_type} must be a JSON array.')

        asset_resp_map[asset_type] = [_to_asset_resp(asset_resp) for asset_resp in asset_resps]

    return asset_resp_map


def _to_assets(data: dict) -> Assets:
    asset_map = data.get("asset_map", data.get("asset_resps"))
    if asset_map is None:
        raise ValueError("Missing required field: asset_map.")

    if "total_asset_amount_krw" not in data:
        raise ValueError("Missing required field: total_asset_amount_krw.")

    return Assets(
        total_asset_amount_krw=_to_decimal(data["total_asset_amount_krw"], "total_asset_amount_krw"),
        asset_map=_to_asset_resp_map(asset_map),
    )


def _sum_asset_amounts_by_category(assets: Assets) -> dict[str, Decimal]:
    category_amounts: dict[str, Decimal] = {}

    for category, asset_resps in assets.asset_map.items():
        total_amount = Decimal("0")
        for asset_resp in asset_resps:
            total_amount += asset_resp.asset_krw or Decimal("0")

        if total_amount > 0:
            category_amounts[category] = total_amount

    return category_amounts
