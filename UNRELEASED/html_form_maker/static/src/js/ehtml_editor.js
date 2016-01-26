(function() {
    'use strict';
    var website = openerp.website;
    website.openerp_website = {};

    website.add_template_file('/html_form_maker/static/src/xml/html_form_modal5.xml');

    website.snippet.options.html_form_settings = website.snippet.Option.extend({
        drop_and_build_snippet: function() {

        }

    })


    website.snippet.options.html_form_field_settings = website.snippet.Option.extend({
        drop_and_build_snippet: function() {
            var self = this;
            self.change_field_settings();
        },

        on_remove: function () {
			var self = this;
	        var s = new openerp.Session();
			s.rpc('/form/deletefield', {'html_field_id': self.$target.attr('data-field-id') }).then(function(result) {

			});
        },

        change_field_settings: function() {
            var self = this;

            self.$modal = $(openerp.qweb.render("html_form_maker.html_form_field_config_modal"));
            self.$modal.appendTo('body');
            self.$modal.modal();

            var field_id = 0;

            $(document).ready(function() {
                $("#html_form_config_field").autocomplete({
                    source: '/form/getfields',
                    minLength: 1,
                    select: function( event, ui ) {
		    			$("#html_form_config_label").val(ui.item.description);
		    			$("#html_form_config_name").val(ui.item.value);
		    			field_id = ui.item.id;
                    }
                });

            });


            self.$modal.find("#save_field").on('click', function () {
				self.$target.find('label').html(self.$modal.find("#html_form_config_label").val());
				self.$target.find('label').attr('for', self.$modal.find("#html_form_config_name").val() );
				//self.$target.find('input').attr('id', self.$modal.find("#html_form_config_name").val() );
				self.$target.find('input').attr("name2", self.$modal.find("#html_form_config_name").val() );

				var s = new openerp.Session();
				s.rpc('/form/updatefield', {'form':'1', 'html_field_id': self.$target.attr('data-field-id'), 'field': field_id, 'field_type': self.$target.attr('data-form-type'), 'html_name': self.$modal.find("#html_form_config_name").val() }).then(function(result) {
                    self.$target.attr('data-field-id', result);
				});

                self.$modal.modal('hide');
            });

            self.$modal.on('shown.bs.modal', function () {
                self.$modal.find("#html_form_config_field_type").val(self.$target.attr('data-form-type'));
            });

        },

        start : function () {
            var self = this;
            this.$el.find(".js_form_field_settings").on("click", _.bind(this.change_field_settings, this));
            this._super();
        },

    })




})();