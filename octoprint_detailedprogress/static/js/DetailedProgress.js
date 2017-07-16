/*
 * View model for OctoPrint-DetailedProgress
 *
 * Author: jneilliii
 * License: AGPLv3
 */
$(function() {
    function DetaileProgressViewModel(parameters) {
        var self = this;
		
		// assign the injected parameters, e.g.:
		self.settingsViewModel = parameters[0];
		
		self.time_to_change = ko.observable();
		
		self.onBeforeBinding = function() {
            self.time_to_change(self.settingsViewModel.settings.plugins.DetailedProgress.time_to_change());
        };
		
		self.onEventSettingsUpdated = function (payload) {            
            self.time_to_change = self.settingsViewModel.settings.plugins.DetailedProgress.time_to_change();
        };
    };

    // view model class, parameters for constructor, container to bind to
    ADDITIONAL_VIEWMODELS.push([
        DetaileProgressViewModel,

        // e.g. loginStateViewModel, settingsViewModel, ...
        ["settingsViewModel"],

        // e.g. #settings_plugin_DetailedProgress, #tab_plugin_DetailedProgress, ...
        ["settings_plugin_DetailedProgress_form"]
    ]);
});
