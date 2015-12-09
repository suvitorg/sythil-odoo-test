(function() {
    'use strict';
    var website = openerp.website;
    website.openerp_website = {};

    website.snippet.options.snippet_ehtml_options = website.snippet.Option.extend({
        drop_and_build_snippet: function() {
            alert("On focus!");
        }
    })
})();