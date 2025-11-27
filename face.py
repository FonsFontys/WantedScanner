from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Tuple

from deepface import DeepFace


class Gezichtsherkenner:
	"""Wrapt DeepFace-logica zodat Main/Database enkel namen hoeven af te handelen."""

	def __init__(
		self,
		*,
		database_dir: Path | str = Path("reference_faces"),
		model_name: str = "VGG-Face",
		detector_backend: str = "opencv",
		distance_metric: str = "cosine",
		match_threshold: float = 0.4,
	) -> None:
		self.database_dir = Path(database_dir)
		self.database_dir.mkdir(parents=True, exist_ok=True)

		self.model_name = model_name
		self.detector = detector_backend
		self.distance_metric = distance_metric
		self.match_threshold = match_threshold

		self._last_distance: Optional[float] = None
		self._last_error: Optional[str] = None

	# -----------------------------------------------------
	# Publieke API volgens UML
	# -----------------------------------------------------
	def faceScan(self, image: Any) -> Optional[str]:
		"""Zoekt naar een match in de database map en geeft de mapnaam terug."""

		self._last_error = None
		self._last_distance = None

		if image is None:
			return None
		if not self._has_reference_faces():
			self._last_error = "Geen referentiebeelden beschikbaar"
			return None

		try:
			result = DeepFace.find(
				img_path=image,
				db_path=str(self.database_dir),
				model_name=self.model_name,
				detector_backend=self.detector,
				distance_metric=self.distance_metric,
				enforce_detection=False,
			)
		except Exception as exc:  # DeepFace kan MissingFaces of TF-fouten gooien
			self._last_error = str(exc)
			return None

		df = self._first_dataframe(result)
		if df is None or getattr(df, "empty", True):
			return None

		best_row = df.iloc[0]
		distance = float(best_row.get("distance", 1.0))
		self._last_distance = distance
		if distance > self.match_threshold:
			return None

		identity_path = Path(best_row.get("identity", ""))
		# neem de mapnaam als identifier (bijv. "JohnDoe")
		return identity_path.parent.name if identity_path.parent.name else identity_path.stem

	def faceCompare(self, pic1: Any, pic2: Any) -> Tuple[bool, Optional[float]]:
		"""Vergelijkt twee beelden en geeft (match, afstand) terug."""

		self._last_error = None

		try:
			result = DeepFace.verify(
				img1_path=pic1,
				img2_path=pic2,
				model_name=self.model_name,
				detector_backend=self.detector,
				distance_metric=self.distance_metric,
				enforce_detection=False,
			)
		except Exception as exc:
			self._last_error = str(exc)
			return False, None

		distance = float(result.get("distance", 1.0))
		return bool(result.get("verified")), distance

	# -----------------------------------------------------
	# Helper functies
	# -----------------------------------------------------
	def _has_reference_faces(self) -> bool:
		return any(p.is_file() for p in self.database_dir.rglob("*"))

	@staticmethod
	def _first_dataframe(result: Any):
		if isinstance(result, list):
			for item in result:
				if hasattr(item, "empty"):
					return item
			return None
		return result

	@property
	def last_distance(self) -> Optional[float]:
		return self._last_distance

	@property
	def last_error(self) -> Optional[str]:
		return self._last_error


if __name__ == "__main__":
	recognizer = Gezichtsherkenner()
	# Voorbeeld: gebruik het laatst genomen snapshot van de Camera
	snapshot_path = Path("snapshots/candidate.jpg")
	if snapshot_path.exists():
		match = recognizer.faceScan(str(snapshot_path))
		print("Match gevonden:", match)
	else:
		print("Geen snapshot gevonden om te scannen.")
