from ipaddress import ip_address

from flask import abort, jsonify, request

from reciperadar import app
from reciperadar.workers.recipes import crawl_recipe, index_recipe


@app.route('/api/recipes/crawl', methods=['POST'])
def recipe_crawl():
    forwarded_for = request.headers.get('x-forwarded-for')
    if forwarded_for and not ip_address(forwarded_for).is_private:
        return abort(403)

    url = request.form.get('url')
    if not url:
        return abort(400)

    crawl_recipe.delay(url)
    return jsonify({})


@app.route('/api/recipes/index', methods=['POST'])
def recipe_index():
    forwarded_for = request.headers.get('x-forwarded-for')
    if forwarded_for and not ip_address(forwarded_for).is_private:
        return abort(403)

    recipe_id = request.form.get('recipe_id')
    if not recipe_id:
        return abort(400)

    index_recipe.delay(recipe_id)
    return jsonify({})
