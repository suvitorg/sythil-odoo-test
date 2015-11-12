$(document).ready(function() {
    "use strict";

    var website = openerp.website;
    var _t = openerp._t;

        get_mods: function() {
website.prompt({
                id: "rpoms_mod_list",
                window_title: _t("Modifiers"),

            }).then(function (cat_id) {
                document.location = '/blogpost/new?blog_id=' + cat_id;
            });
},

});