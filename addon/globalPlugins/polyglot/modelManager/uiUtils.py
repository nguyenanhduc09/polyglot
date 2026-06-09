# -*- coding: utf-8 -*-
# A part of the Polyglot add-on for NVDA.
# Copyright (C) 2025 Cary-rowen <manchen_0528@outlook.com>
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.

"""Small wx helpers for cross-thread model manager UI interactions."""

from __future__ import annotations

import gui
import wx
from gui.guiHelper import wxCallOnMain


def messageBoxOnMainThread(
	message: str,
	caption: str,
	style: int,
	parent: wx.Window | None = None,
) -> int:
	"""Show an NVDA message box from any thread and return its result."""
	return wxCallOnMain(gui.messageBox, message, caption, style, parent)
