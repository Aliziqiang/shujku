"""Load the portable dashboard from structured data and bundled product photos."""
import json
import base64
import mimetypes
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def build_dashboard():
    payload = json.loads((ROOT / 'data.json').read_text(encoding='utf-8'))
    products = payload['products']
    for product in products.values():
        # Keep images self-contained so missing static-serving configuration
        # or iframe URL resolution cannot leave product cards blank.
        candidates = [product.get('full_image_file'), product.get('image_file')]
        image = None
        for relative in candidates:
            if not relative:
                continue
            candidate = (ROOT / relative).resolve()
            if candidate.is_relative_to(ROOT) and candidate.is_file():
                image = candidate
                break
        if image is None:
            raise ValueError('Product image file is missing: ' + str(product.get('title', '')))
        mime = mimetypes.guess_type(image.name)[0]
        if mime not in ('image/png', 'image/jpeg', 'image/webp', 'image/gif'):
            raise ValueError('Unsupported product image format')
        product['image'] = 'data:' + mime + ';base64,' + base64.b64encode(image.read_bytes()).decode('ascii')
        # The lightbox uses the same original image; avoid embedding it twice.
        product['fullImage'] = ''
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
