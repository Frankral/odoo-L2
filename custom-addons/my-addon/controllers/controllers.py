# -*- coding: utf-8 -*-
# from odoo import http


# class ./custom-addons/my-addon(http.Controller):
#     @http.route('/./custom-addons/my-addon/./custom-addons/my-addon', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/./custom-addons/my-addon/./custom-addons/my-addon/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('./custom-addons/my-addon.listing', {
#             'root': '/./custom-addons/my-addon/./custom-addons/my-addon',
#             'objects': http.request.env['./custom-addons/my-addon../custom-addons/my-addon'].search([]),
#         })

#     @http.route('/./custom-addons/my-addon/./custom-addons/my-addon/objects/<model("./custom-addons/my-addon../custom-addons/my-addon"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('./custom-addons/my-addon.object', {
#             'object': obj
#         })

