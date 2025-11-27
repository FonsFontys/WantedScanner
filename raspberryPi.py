from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import cv2
import numpy as np


@dataclass
class PosterData:
	"""Helper object om persoonsinfo te structureren."""

	name: str = "Onbekend"
	danger_level: int = 0
	crime: str = ""

	@classmethod
	def from_person(cls, person: Any) -> "PosterData":
		return cls(
			name=getattr(person, "name", getattr(person, "naam", "Onbekend")),
			danger_level=int(getattr(person, "danger_level", 0)),
			crime=getattr(person, "crime", getattr(person, "misdrijf", "")),
		)


class Interface:
	"""Simpele interface die het Raspberry Pi scherm aanstuurt via OpenCV."""

	def __init__(self) -> None:
		self.window_name = "WantedScanner"
		cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
		cv2.resizeWindow(self.window_name, 800, 480)

	def update_live(self, frame) -> None:
		cv2.imshow(self.window_name, frame)
		cv2.waitKey(1)

	def wanted_poster(self, person) -> None:
		poster_info = PosterData.from_person(person)
		poster = self._build_poster_canvas(poster_info)
		cv2.imshow(self.window_name, poster)
		cv2.waitKey(1)

	def _build_poster_canvas(self, info: PosterData) -> np.ndarray:
		canvas = np.zeros((480, 800, 3), dtype=np.uint8)
		canvas[:] = (30, 30, 30)

		cv2.putText(canvas, "WANTED", (220, 80), cv2.FONT_HERSHEY_DUPLEX, 2.5, (0, 0, 255), 4)
		cv2.putText(canvas, f"Naam: {info.name}", (60, 170), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2)
		cv2.putText(
			canvas,
			f"Gevaar: {info.danger_level}",
			(60, 240),
			cv2.FONT_HERSHEY_SIMPLEX,
			1.1,
			(0, 200, 255),
			2,
		)
		if info.crime:
			cv2.putText(
				canvas,
				f"Delict: {info.crime}",
				(60, 310),
				cv2.FONT_HERSHEY_SIMPLEX,
				1.0,
				(255, 255, 255),
				2,
			)

		cv2.putText(
			canvas,
			"Meld direct bij politie",
			(60, 400),
			cv2.FONT_HERSHEY_SIMPLEX,
			0.9,
			(0, 255, 0),
			2,
		)

		return canvas
