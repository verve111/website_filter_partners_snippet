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
        zip_where = ''
        if zip:
            arr = [x.strip() for x in zip.split(',')]
            zip_where = ', '.join('\'{0}\''.format(w) for w in arr)
            zip_where = ' AND p.zip IN (%s) ' % zip_where
        count_query = """SELECT COUNT(*) FROM res_partner p, crm_lead l  
            WHERE l.partner_assigned_id = p.id AND p.is_published = TRUE AND p.grade_id IS NOT NULL {0}"""\
            .format(zip_where)
        request.env.cr.execute(count_query)
        total = request.env.cr.fetchone()[0]

        query = """SELECT p.id FROM res_partner p, crm_lead l  
            WHERE l.partner_assigned_id = p.id AND p.is_published = TRUE AND p.grade_id IS NOT NULL {0}
            ORDER BY p.name ASC
            LIMIT {1} OFFSET {2}"""\
            .format(zip_where, limit, (page - 1) * limit)
        request.env.cr.execute(query)
        partner_ids = [row[0] for row in request.env.cr.fetchall()]
        records = request.env["res.partner"].sudo().browse(partner_ids) if partner_ids else []

        # _logger.info('total: ' + str(total))
        return request.website.viewref("website_filter_partners_snippet.s_partners_by_zip_items").render({
            "objects": records,
            "pager": request.website.pager(
                url="/c/partners", page=page, step=limit,
                total=total, scope=7, url_args=kwargs
            ),
        })
