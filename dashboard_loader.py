"""Load the portable dashboard from structured data and bundled product photos."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def build_dashboard():
    payload = json.loads((ROOT / 'data.json').read_text(encoding='utf-8'))
    products = payload['products']
    for product in products.values():
        for field, target in [('thumbnail_file', 'image'), ('full_image_file', 'fullImage')]:
            image = (ROOT / product[field]).resolve()
            if not image.is_relative_to(ROOT / 'static') or not image.is_file():
                raise ValueError('Image must exist inside static/')
            product[target] = '/app/static/' + image.relative_to(ROOT / 'static').as_posix()
    for sku in payload['skus']:
        if sku['id'] not in products or not isinstance(sku['price'], (int, float)) or sku['price'] < 0:
            raise ValueError('Invalid SKU data')
    scripts = 'const productMetadata=' + json.dumps(products, ensure_ascii=False) + ';\nconst skuData=' + json.dumps(payload['skus'], ensure_ascii=False) + ';'
    scripts = scripts.replace('</', '<\\/')
    html = (ROOT / 'dashboard/index.html').read_text(encoding='utf-8')
    html = html.replace('<link rel="stylesheet" href="style.css">', '<style>' + (ROOT / 'dashboard/style.css').read_text(encoding='utf-8') + '</style>')
    html = html.replace('<script src="products.js"></script>', '<script>' + scripts + '</script>')
    html = html.replace('<script src="app.js"></script>', '<script>' + (ROOT / 'dashboard/app.js').read_text(encoding='utf-8') + '</script>')
    return html
