/*
 * View model for OctoPrint-DetailedProgress
 *
 * Author: jneilliii
 * License: AGPLv3
 */
$(function() {
    function DetailedProgressViewModel(parameters) {
        var self = this;

		// assign the injected parameters, e.g.:
		self.settings = parameters[0];

		self.time_to_change = ko.observable();
		self.eta_strftime = ko.observable();
		self.etl_format = ko.observable();
		self.print_done_message = ko.observable();
		self.all_messages = ko.observableArray();
		self.messages = ko.observableArray();

		self.onBeforeBinding = function() {
            self.time_to_change(self.settings.settings.plugins.detailedprogress.time_to_change());
            self.eta_strftime(self.settings.settings.plugins.detailedprogress.eta_strftime());
            self.etl_format(self.settings.settings.plugins.detailedprogress.etl_format());
            self.print_done_message(self.settings.settings.plugins.detailedprogress.print_done_message());
			self.messages(self.settings.settings.plugins.detailedprogress.messages());
			self.all_messages(self.settings.settings.plugins.detailedprogress.all_messages());
        };

		self.onEventSettingsUpdated = function (payload) {
            self.time_to_change = self.settings.settings.plugins.detailedprogress.time_to_change();
            self.eta_strftime = self.settings.settings.plugins.detailedprogress.eta_strftime();
            self.etl_format = self.settings.settings.plugins.detailedprogress.etl_format();
            self.print_done_message = self.settings.settings.plugins.detailedprogress.print_done_message();
			self.messages = self.settings.settings.plugins.detailedprogress.messages();
			self.all_messages = self.settings.settings.plugins.detailedprogress.all_messages();
        };

		$('#dtPrg_addMsg').click(function () {
		    var msgToAdd = $('#dtPrg_msgToAdd').val();
		    // Prevent blanks and duplicates
			if (msgToAdd.length > 0 &&
			    $('#dtPrg_selMsg option').filter(function () { return $(this).html() == msgToAdd; }).length == 0) {
                $('#dtPrg_selMsg').append('<option selected>'+msgToAdd+'</option>');
                self.all_messages.push(msgToAdd);
			}
			$('#dtPrg_msgToAdd').val('');; // Clear the text box
			return false;
		});

		$('#dtPrg_removeSelected').click(function () {
		    var msgToRemove = $('#dtPrg_selMsg').val();
		    if (msgToRemove.length == 0) return false;
		    $('#dtPrg_selMsg option').each(function() {
                if (msgToRemove.indexOf($(this).val()) > - 1) $(this).remove();
            });
			self.all_messages.removeAll(msgToRemove);
            return false;
		});
    };

    // view model class, parameters for constructor, container to bind to
    OCTOPRINT_VIEWMODELS.push([
        DetailedProgressViewModel,

        // e.g. loginStateViewModel, settingsViewModel, ...
        ["settingsViewModel"],

        // e.g. #settings_plugin_DetailedProgress, #tab_plugin_DetailedProgress, ...
        []
    ]);
});
