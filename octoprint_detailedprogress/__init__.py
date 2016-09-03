# coding=utf-8
from __future__ import absolute_import
import time

import octoprint.plugin
import octoprint.util
import traceback
from octoprint.events import Events

class DetailedProgressPlugin(octoprint.plugin.EventHandlerPlugin,
                             octoprint.plugin.SettingsPlugin):
	_last_updated = 0.0
	_last_message = 0
	_repeat_timer = None
	_etl_format = ""
	_eta_strftime = ""
	_messages = []
	def on_event(self, event, payload):
		if event == Events.PRINT_STARTED:
			self._logger.info("Printing started. Detailed progress started.")
			self._etl_format = self._settings.get(["etl_format"])
			self._eta_strftime = self._settings.get(["eta_strftime"])
			self._messages = self._settings.get(["messages"])
			self._repeat_timer = octoprint.util.RepeatedTimer(self._settings.get_int(["time_to_change"]), self.do_work)
			self._repeat_timer.start()
		elif event in (Events.PRINT_DONE, Events.PRINT_FAILED, Events.PRINT_CANCELLED):
			if self._repeat_timer != None:
				self._repeat_timer.cancel()
				self._repeat_timer = None
			self._logger.info("Printing stopped. Detailed progress stopped.")

	def do_work(self):
		try:
			currentData = self._printer.get_current_data()
			currentData = self._sanitize_current_data(currentData)

			message = self._get_next_message(currentData)
		except Exception as e:
			self._logger.info("Caught an exception {0}\nTraceback:{1}".format(e,traceback.format_exc()))
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
		currentData["progress"]["ETA"] = time.strftime(self._eta_strftime, time.localtime(time.time() + currentData["progress"]["printTimeLeft"]))
		return currentData

	def _get_next_message(self, currentData):
		message = self._messages[self._last_message]
		self._last_message += 1
		if (self._last_message >= len(self._messages)):
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
		return self._etl_format.format(**locals())

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
	}

