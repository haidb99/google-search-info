from . import api
from flask import jsonify, request, send_file

from ..services.search_by_keyword import GoogleSearchInfo


@api.route("/search/get", methods=["GET"])
def search_key_word():
    key_word = request.args.get('key_word')
    limit = int(request.args.get("limit", 20))
    page = int(request.args.get("page", 1))
    if key_word is None:
        return jsonify({"error": "Missing 'key_word' parameter"}), 400

    try:
        output = GoogleSearchInfo(key_word).get_data_by_page(page=page, limit=limit)
    except Exception as e:
        return jsonify({"error": f"{str(e)}"}), 500

    output["message"] = "success"
    return jsonify(output)


@api.route("/search/export", methods=["GET"])
def export_data():
    key_word = request.args.get('key_word')
    if key_word is None:
        return jsonify({"error": "Missing 'key_word' parameter"}), 400

    try:
        output = GoogleSearchInfo(key_word).export_excel()
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            download_name="data.xlsx",
            as_attachment=True
        )
    except Exception as e:
        return jsonify({"error": f"{str(e)}"}), 500
