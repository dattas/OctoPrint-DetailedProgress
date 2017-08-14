/*
 * View model for OctoPrint-DetailedProgress
 *
 * Author: jneilliii
 * License: AGPLv3
 */
$(function() {
    function detailedprogressViewModel(parameters) {
        var self = this;
		
		// assign the injected parameters, e.g.:
		self.settings = parameters[0];
		
		self.time_to_change = ko.observable();
		self.eta_strftime = ko.observable();
		self.etl_format = ko.observable();
		self.allmessages = ko.observableArray();
		self.messages = ko.observableArray();
		self.msgToAdd = ko.observable();
		
		self.onBeforeBinding = function() {
            self.time_to_change(self.settings.settings.plugins.detailedprogress.time_to_change());
            self.eta_strftime(self.settings.settings.plugins.detailedprogress.eta_strftime());
            self.etl_format(self.settings.settings.plugins.detailedprogress.etl_format());
			self.messages(self.settings.settings.plugins.detailedprogress.messages());
			self.allmessages(self.settings.settings.plugins.detailedprogress.allmessages());
			self.msgToAdd(self.settings.settings.plugins.detailedprogress.msgToAdd());
        };
		
		self.onEventSettingsUpdated = function (payload) {            
            self.time_to_change = self.settings.settings.plugins.detailedprogress.time_to_change();
            self.eta_strftime = self.settings.settings.plugins.detailedprogress.eta_strftime();
            self.etl_format = self.settings.settings.plugins.detailedprogress.etl_format();
			self.messages = self.settings.settings.plugins.detailedprogress.messages();
			self.allmessages = self.settings.settings.plugins.detailedprogress.allmessages();
			self.msgToAdd = self.settings.settings.plugins.detailedprogress.msgToAdd();
        };
		
		self.addMsg = function () {
			if ((self.msgToAdd() != "") && (self.allmessages.indexOf(self.msgToAdd()) < 0)) // Prevent blanks and duplicates
				self.allmessages.push(self.msgToAdd());
			self.msgToAdd(""); // Clear the text box
		};
	 
		self.removeSelected = function () {
			self.allmessages.removeAll(self.messages());
			self.messages([]); // Clear selection
		};
    };

    // view model class, parameters for constructor, container to bind to
    ADDITIONAL_VIEWMODELS.push([
        detailedprogressViewModel,

        // e.g. loginStateViewModel, settingsViewModel, ...
        ["settingsViewModel"],

        // e.g. #settings_plugin_DetailedProgress, #tab_plugin_DetailedProgress, ...
        []
    ]);
});
