from flask import Flask, request, jsonify
import fitz
import os

app = Flask(__name__)
API_KEY = os.environ.get("API_KEY", "thesis-review-2024")


@app.route("/parse", methods=["POST"])
def parse_pdf():
    if request.headers.get("X-API-Key") != API_KEY:
        return jsonify({"error": "unauthorized"}), 401

    file = request.files.get("file")
    if not file:
        return jsonify({"error": "no file"}), 400

    doc = fitz.open(stream=file.read(), filetype="pdf")
    pages = [
        {"page_num": i + 1, "text": doc[i].get_text()}
        for i in range(doc.page_count)
    ]
    doc.close()
    return jsonify({"success": True, "total_pages": len(pages), "pages": pages})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))