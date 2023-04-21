from io import BytesIO
import os
from flask import render_template, redirect, url_for, request, send_from_directory, Response
import pandas as pd
from app import app
from app.models.product import Product


@app.route('/')
def index():
    """Return the "index.html.jinja" template. Render the index page."""
    return render_template("index.html.jinja")


@app.route('/extract', methods=["POST", "GET"])
def extract():
    """Return the "extract.html.jinja" template. Render the opinion extraction page."""
    if request.method == "POST":
        product_id = request.form.get("product_id")
        product = Product(product_id)
        product.extract_name()
        if product.product_name:
            product.extract_opinions().calculate_stats().draw_charts()
            product.export_opinions()
            product.export_product()
        else:
            error = "Darn it! This product ID does not exist, bucko!"
            return render_template("extract.html.jinja", error=error)
        return redirect(url_for('product', product_id=product_id))
    else:
        return render_template("extract.html.jinja")


@app.route('/products')
def products():
    """Return the "products.html.jinja" template. Render the product list page."""
    products = []

    if os.path.exists("app/opinions"):
        for product_id in [filename.split(".")[0] for filename in os.listdir("app/opinions")]:
            product = Product(product_id)
            product.import_product(import_opinions=False)
            products.append(product.stats_to_dict())

    return render_template("products.html.jinja", products=products)


@app.route('/author')
def author():
    """Return the "author.html.jinja" template. Render the about author page."""
    return render_template("author.html.jinja")


@app.route('/product/<product_id>')
def product(product_id):
    """Return the "product.html.jinja" template. Render a page about a specific product."""
    product = Product(product_id)
    product.import_product()
    product_dictionary = product.to_dict()

    return render_template("product.html.jinja", product=product_dictionary)


@app.route('/graphs/<product_id>')
def graphs(product_id):
    """
    Return the "graphs.html.jinja" template.
    Render a page with graphs related to a specific product.
    """
    return render_template("graphs.html.jinja", product_id=product_id)


@app.route('/opinions/<product_id>.<extension>')
def download_opinions(product_id, extension):
    """Return a downloadable file containing opinions in the JSON, CSV or XLSX format."""
    match extension:
        case "json":
            return send_from_directory("opinions/", f"{product_id}.{extension}", as_attachment=True)
        case "csv":
            return Response(
                pd.read_json(
                    f'app/opinions/{product_id}.json').to_csv(encoding="UTF-8", index=False),
                mimetype='text/csv',
                headers={'Content-disposition': f'attachment; filename={product_id}.{extension}'})
        case "xlsx":
            buffer = BytesIO()
            pd.read_json(
                f'app/opinions/{product_id}.json').to_excel(buffer, index=False)
            buffer.seek(0)

            return Response(
                buffer,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                headers={'Content-disposition': f'attachment; filename={product_id}.{extension}'})
