# coding=utf-8
from __future__ import absolute_import
import time

import octoprint.plugin

class DetailedProgressPlugin(octoprint.plugin.SettingsPlugin):
	_last_updated = 0.0
	_last_message = 0

	##~~ gcode.queued hook
	def do_work(self, comm_instance, phase, cmd, cmd_type, gcode, *args, **kwargs):
		if(comm_instance.getState() != comm_instance.STATE_PRINTING):
			return
		if(time.time() - self._last_updated < self._settings.get_int(["time_to_change"])):
			return
		self._last_updated = time.time()
		currentData = self._printer.get_current_data()
		currentData = self._sanitize_current_data(currentData)

		message = self._get_next_message(currentData)
		self._printer.commands("M117 {}".format(message))

	def _sanitize_current_data(self, currentData):
		if (currentData["progress"]["printTimeLeft"] == None):
			currentData["progress"]["printTimeLeft"] = currentData["job"]["estimatedPrintTime"]
		if (currentData["progress"]["filepos"] == None):
			currentData["progress"]["filepos"] = 0
		if (currentData["progress"]["printTime"] == None):
			currentData["progress"]["printTime"] = currentData["job"]["estimatedPrintTime"]

		#Add additional data
		currentData["progress"]["printTimeLeftString"] = self._get_time_from_seconds(currentData["progress"]["printTimeLeft"])
		currentData["progress"]["ETA"] = time.strftime(self._settings.get(["eta_strftime"]), time.localtime(time.time() + currentData["progress"]["printTimeLeft"]))
		return currentData

	def _get_next_message(self, currentData):
		messsages = self._settings.get(["messages"])
		message = messsages[self._last_message]
		self._last_message += 1
		if (self._last_message >= len(messsages)):
			self._last_message = 0
		return message.format(
			completion = currentData["progress"]["completion"],
			printTimeLeft = currentData["progress"]["printTimeLeftString"],
			ETA = currentData["progress"]["ETA"],
			filepos = currentData["progress"]["filepos"]
		)

	def _get_time_from_seconds(self, seconds):
		hours = 0
		minutes = 0
		if seconds > 3600:
			hours = int(seconds / 3600)
			seconds = seconds % 3600
		if seconds > 60:
			minutes = int(seconds / 60)
			seconds = seconds % 60
		return self._settings.get(["etl_format"]).format(**locals())

	##~~ Settings

	def get_settings_defaults(self):
		return dict(
			messages = [
				"{completion:.2f} % complete",
				"ETL {printTimeLeft}",
				"ETA {ETA}"
			],
			eta_strftime = "%H:%M:%S Day %d",
			etl_format = "{hours:02d}:{minutes:02d}:{seconds:02d}",
			time_to_change = 10
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		return dict(
			detailedprogress=dict(
				displayName="DetailedProgress Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="dattas",
				repo="OctoPrint-DetailedProgress",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/dattas/OctoPrint-DetailedProgress/archive/{target_version}.zip"
			)
		)

__plugin_name__ = "Detailed Progress Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = DetailedProgressPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information,
		"octoprint.comm.protocol.gcode.queued": __plugin_implementation__.do_work
	}

