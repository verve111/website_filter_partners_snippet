# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
# from odoo.addons.website.controllers.main import QueryURL
import logging

_logger = logging.getLogger(__name__)


class WebsiteFilterPartnersSnippet(http.Controller):
    @http.route('/website_filter_partners_snippet/website_filter_partners_snippet/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route(['/c/partners/', '/c/partners/page/<int:page>'], auth='public', type="json", website=True, csrf=False)
    def list(self, page=1, zip=False, limit=10, **kwargs):
        domain = [('zip', '=', zip)] if zip else []
        records = request.env["res.partner"].sudo().search(domain, offset=(page - 1) * limit, limit=limit)
        total = request.env["res.partner"].sudo().search_count(domain)
        _logger.error('total' + str(total))
        return request.website.viewref("website_filter_partners_snippet.s_partners_by_zip_items").render({
            "objects": records,
            "pager": request.website.pager(
                url="/c/partners", page=page, step=limit,
                total=total, scope=7, url_args=kwargs
            ),
        })
