# -*- coding: utf-8 -*-

from typing import Any

import ui
from speech.extensions import filter_speechSequence

from ..common import cues
from .manager import TranslationManager


class SpeechFilter:
	# Annotate instance variables at the class level
	manager: TranslationManager
	last_spoken_text: str
	_is_speaking_translation: bool
	_suppress_capture: int

	def __init__(self, manager: TranslationManager) -> None:
		super().__init__()
		self.manager = manager
		self.last_spoken_text = ""
		self._is_speaking_translation = False
		self._suppress_capture = 0

	def register(self) -> None:
		filter_speechSequence.register(self.on_speech_sequence)
		cues.register_speech_hook(self.suppress_next_capture)

	def unregister(self) -> None:
		_unused = filter_speechSequence.unregister(self.on_speech_sequence)
		cues.unregister_speech_hook()

	def suppress_next_capture(self) -> None:
		self._suppress_capture += 1

	def on_speech_sequence(self, sequence: list[Any]) -> list[Any]:
		# Extract the text from the speech sequence.
		text_to_save = " ".join([s for s in sequence if isinstance(s, str) and s.strip()])
		# Save the text unless suppression was requested by the cues module.
		if text_to_save:
			if self._suppress_capture > 0:
				self._suppress_capture -= 1
			else:
				self.last_spoken_text = text_to_save
		if not self.manager.auto_translate_enabled:
			return sequence
		# To prevent translation loops, skip if the speech is already a translation result.
		if self._is_speaking_translation:
			self._is_speaking_translation = False
			return sequence
		# Trigger auto-translation if there is text.
		if text_to_save:
			self.manager.request_translation(
				text_to_save,
				is_manual=False,
				show_status=False,
				allow_copy=False,
				on_success=self._handle_auto_translation_result,
			)
		# Block the original speech sequence; it will be replaced by the translation.
		return []

	def _handle_auto_translation_result(self, translation: str) -> None:
		"""
		Callback for a successful auto-translation.
		Called by the TranslationManager on the main thread.
		"""
		# 1. Set a flag to prevent this result from being re-translated.
		self._is_speaking_translation = True
		# 2. Speak the translation.
		ui.message(translation)
