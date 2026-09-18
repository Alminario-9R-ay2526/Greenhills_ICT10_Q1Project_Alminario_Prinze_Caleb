from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)


# -----------------------------
# HOME PAGE
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# SKU GENERATOR
# -----------------------------
@app.route("/generate-sku", methods=["POST"])
def generate_sku():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No data received."
        }), 400

    category = data.get("category", "").strip()
    product_name = data.get("product_name", "").strip()
    quantity = data.get("quantity")

    # Check product name
    if not product_name:
        return jsonify({
            "error": "Product name is required."
        }), 400

    # Check quantity
    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        return jsonify({
            "error": "Quantity must be a number."
        }), 400

    if quantity < 1:
        return jsonify({
            "error": "Quantity must be at least 1."
        }), 400

    # Check category
    valid_categories = {
        "PER",
        "NON",
        "BEV",
        "SNK",
        "OTH"
    }

    if category not in valid_categories:
        return jsonify({
            "error": "Invalid category."
        }), 400

    # --------------------------------
    # Create product abbreviation
    # --------------------------------

    # Remove special characters
    clean_name = re.sub(
        r"[^A-Za-z0-9\s]",
        "",
        product_name
    )

    words = clean_name.upper().split()

    if len(words) >= 2:
        # Example:
        # Bottled Water -> BW
        product_code = "".join(
            word[0] for word in words
        )[:3]

    else:
        # Example:
        # Water -> WAT
        product_code = clean_name.upper()[:3]

    # Make sure code isn't empty
    if not product_code:
        return jsonify({
            "error": "Invalid product name."
        }), 400

    # --------------------------------
    # Format quantity
    # --------------------------------

    quantity_code = f"{quantity:03d}"

    # --------------------------------
    # Final SKU
    # --------------------------------

    sku = f"{category}-{product_code}-{quantity_code}"

    return jsonify({
        "sku": sku
    })


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
