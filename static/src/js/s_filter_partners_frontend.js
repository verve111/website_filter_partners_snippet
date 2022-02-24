odoo.define("website_filter_partners_snippet.s_partners_by_zip", function (require) {
    "use strict";

    var core = require("web.core");
    var sAnimation = require("website.content.snippets.animation");

    var _t = core._t;

    sAnimation.registry.js_partners_by_zip = sAnimation.Class.extend({
        selector: ".js_partners_by_zip",
        limit: 3,
        domain: [],

        start: function () {
            var self = this;
            //var limit = Number(this.$target.attr("data-products-limit")) || 12;
            self.domain = this.$target.attr("data-domain") || "[]";
            // Prevent user edition
            self.$target.attr("contenteditable", "False");

            // Loading Indicator
            self.$target.html(
                $("<div/>", {class: "text-center p-5 my-5 text-muted"})
                .append($("<i/>", {
                    class: "fa fa-circle-o-notch fa-spin fa-3x fa-fwg mr-1"
                }))
            );

            var def = self._getPartners(1);
            return $.when(this._super.apply(this, arguments), def);
        },

        _getPartners: function (pageNum) {
            var self = this;
            var def = this._rpc({
                route: "/c/partners/page/" + pageNum,
                params: {
                    limit: self.limit,
                    domain: JSON.parse(self.domain),
                },
            }).then(function (object_html) {
                    var $object_html = $(object_html);
                    var count = $object_html
                        .find("input[name='partner_count']")
                        .val();
                    if (!count) {
                        self.$target.append(
                            $("<div/>", {class: "col-md-6 offset-md-3"}).append(
                                $("<div/>", {
                                    class:
                                        "alert alert-warning" +
                                        " alert-dismissible text-center",
                                    text: _t(
                                        "No partners was found." +
                                        " Make sure you have partners" +
                                        " published on the website."
                                    ),
                                })
                            )
                        );
                        return;
                    }
                    self.$target.html($object_html);

                    // attach ajax on paginator (pager)
                    self.$target.find('.pagination a[data-pagenum]').click(function (e) {
                        e.preventDefault();
                        let pageNum = $(e.currentTarget).data('pagenum');
                        if (Number(pageNum) > 0) {
                            self._getPartners(pageNum);
                        }
                    });

                    // Initialize 'animations' for the product card.
                    // This is necessary because the snippet is asynchonously
                    // rendered on the server.
                    // self.trigger_up('animation_start_demand', {
                    //     $target: self.$target.find('.oe_website_sale'),
                    // });
                },
                function () {
                    if (self.editableMode) {
                        self.$target.append(
                            $("<p/>", {
                                class: "text-danger",
                                text: _t(
                                    "An error occured with get partners" +
                                    " block. If the problem" +
                                    " persists, please consider deleting" +
                                    " it and adding a new one"
                                ),
                            })
                        );
                    }
                }
            );
            return def;
        },

        /**
         * @override
         */
        destroy: function () {
            this.$target.empty();
            this._super.apply(this, arguments);
        },
    });
});
