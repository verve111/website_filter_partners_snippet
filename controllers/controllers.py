# -*- coding: utf-8 -*-
from odoo import http

# class WebsiteFilterPartnersSnippet(http.Controller):
#     @http.route('/website_filter_partners_snippet/website_filter_partners_snippet/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_filter_partners_snippet/website_filter_partners_snippet/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_filter_partners_snippet.listing', {
#             'root': '/website_filter_partners_snippet/website_filter_partners_snippet',
#             'objects': http.request.env['website_filter_partners_snippet.website_filter_partners_snippet'].search([]),
#         })

#     @http.route('/website_filter_partners_snippet/website_filter_partners_snippet/objects/<model("website_filter_partners_snippet.website_filter_partners_snippet"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_filter_partners_snippet.object', {
#             'object': obj
#         })