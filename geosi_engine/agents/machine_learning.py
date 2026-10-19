"""
GeoSI v2 — Machine Learning Agent (Core Agent #8)
════════════════════════════════════════════════════════════════════
Classification, regression, clustering, forecasting, model training,
model evaluation, and spatial prediction.

PRD §4.1 Agent #8 — Production requirements
─────────────────────────────────────────────
* Training/inference jobs tagged ``mutating`` at minimum (writes
  model artifacts).
* Subject to Permission & Safety Agent review before any write.
* Artifacts and metrics written to PostGIS ``geosi_eval_runs`` for
  reproducibility (FR-8).
* Auto-tier: ``ask`` minimum (never ``allow``-default for training).
* Libraries: Scikit-Learn, PyTorch (TensorFlow optional).
"""

from __future__ import annotations

import logging
import os
import tempfile
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional

from geosi_engine.telemetry import set_span_attr, span

logger = logging.getLogger("geosi_engine.agents.ml")

# Minimum permission tier for any ML job — never lower than "mutating"
_MIN_ML_RISK: Literal["mutating", "destructive"] = "mutating"


@dataclass
class MLJobRequest:
    """A machine learning job request."""

    job_type: str  # "classification" | "regression" | "clustering" | "forecasting" | "predict"
    algorithm: str  # e.g. "random_forest" | "gradient_boosting" | "kmeans" | "lstm"
    input_layers: List[str] = field(default_factory=list)
    feature_columns: List[str] = field(default_factory=list)
    target_column: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    model_path: Optional[str] = None  # for loading a pre-trained model
    output_path: Optional[str] = None  # where to save the model / predictions
    session_id: str = ""


@dataclass
class MLJobResult:
    """Result of a machine learning job."""

    success: bool
    job_type: str
    algorithm: str
    metrics: Dict[str, Any] = field(default_factory=dict)
    output_path: Optional[str] = None
    eval_run_id: Optional[str] = None
    error: Optional[str] = None
    duration_ms: float = 0.0


def _temp_path(name: str) -> str:
    return os.path.join(tempfile.mkdtemp(prefix="geosi_ml_"), name)


class MachineLearningAgent:
    """
    Machine Learning domain agent (PRD §4.1, Agent #8).

    Wraps Scikit-Learn, PyTorch, and TensorFlow for spatial ML workflows.
    Every training/inference job:
      1. Routes through Permission & Safety Agent (``ask`` minimum).
      2. Writes artifacts + metrics to ``geosi_eval_runs`` (FR-8).
      3. Produces a structured ``MLJobResult`` for the Report Generation Agent.

    Parameters
    ----------
    engine:
        Session-scoped GeoSI instance.
    permission_agent:
        The ``PermissionSafetyAgent`` for the current session.
    """

    def __init__(self, engine: Any, permission_agent: Any) -> None:
        self._engine = engine
        self._permission = permission_agent

    # ------------------------------------------------------------------
    # Public: primary dispatch
    # ------------------------------------------------------------------

    @span("ml_agent.execute", agent="ml")
    def execute(self, job: MLJobRequest) -> MLJobResult:
        """
        Execute an ML job with full permission enforcement.

        The risk level is always at least ``mutating`` (writes model
        artifacts). Jobs that overwrite existing models are ``destructive``.
        """
        set_span_attr("ml.job_type", job.job_type)
        set_span_attr("ml.algorithm", job.algorithm)

        # Escalate risk if overwriting an existing model
        risk_level = "destructive" if job.output_path and self._path_exists(job.output_path) else _MIN_ML_RISK
        set_span_attr("ml.risk_level", risk_level)

        # ── Permission gate ────────────────────────────────────────────
        from geosi_engine.agents.gis_agent import ApprovalPendingError, PermissionDeniedError
        from geosi_engine.models import ToolStep

        proxy_step = ToolStep(
            tool_name=f"ml:{job.job_type}:{job.algorithm}",
            risk_level=risk_level,
            parameters=job.parameters,
            description=f"ML {job.job_type} using {job.algorithm}",
        )
        decision = self._permission.check_permission(f"ml:{job.job_type}", risk_level)
        audit_id = self._permission.audit_log_before_execution(proxy_step, session_id=job.session_id, decision=decision)

        if decision.decision == "deny":
            self._permission.update_audit_log(audit_id, "denied")
            raise PermissionDeniedError(f"ML job '{job.job_type}' is denied by policy.")

        if decision.decision == "ask":
            approval = self._permission.request_approval(proxy_step, session_id=job.session_id)
            raise ApprovalPendingError(
                action_id=approval.action_id,
                message=f"ML job '{job.job_type}' ({job.algorithm}) requires approval. action_id={approval.action_id}",
            )

        # ── Execute ────────────────────────────────────────────────────
        start = time.monotonic()
        try:
            result = self._dispatch(job)
            result.duration_ms = (time.monotonic() - start) * 1000
            # Write to geosi_eval_runs (FR-8)
            result.eval_run_id = self._persist_eval_run(job, result)
            status = "success" if result.success else "failed"
            self._permission.update_audit_log(audit_id, status, error=result.error)
            set_span_attr("ml.eval_run_id", result.eval_run_id or "")
            return result
        except (ApprovalPendingError, PermissionDeniedError):
            raise
        except Exception as exc:
            self._permission.update_audit_log(audit_id, "error", error=str(exc))
            raise

    # ------------------------------------------------------------------
    # Job type handlers
    # ------------------------------------------------------------------

    def train_classifier(self, job: MLJobRequest) -> MLJobResult:
        """Train a spatial classification model."""
        try:
            import joblib
            from sklearn.metrics import accuracy_score
            from sklearn.model_selection import train_test_split

            X, y = self._load_spatial_features(job)
            if X is None:
                return MLJobResult(
                    success=False,
                    job_type="classification",
                    algorithm=job.algorithm,
                    error="Could not load spatial features from input layers.",
                )

            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=job.parameters.get("test_size", 0.2),
                random_state=job.parameters.get("random_state", 42),
            )

            clf = self._build_sklearn_classifier(job.algorithm, job.parameters)
            clf.fit(X_train, y_train)
            preds = clf.predict(X_test)

            metrics = {
                "accuracy": float(accuracy_score(y_test, preds)),
                "n_train": len(X_train),
                "n_test": len(X_test),
                "algorithm": job.algorithm,
            }

            out_path = job.output_path or _temp_path(f"model_{job.algorithm}.joblib")
            joblib.dump(clf, out_path)
            logger.info("Classifier trained: accuracy=%.3f → %s", metrics["accuracy"], out_path)

            return MLJobResult(
                success=True, job_type="classification", algorithm=job.algorithm, metrics=metrics, output_path=out_path
            )

        except ImportError as e:
            return MLJobResult(
                success=False,
                job_type="classification",
                algorithm=job.algorithm,
                error=f"scikit-learn not available: {e}",
            )
        except Exception as exc:
            return MLJobResult(success=False, job_type="classification", algorithm=job.algorithm, error=str(exc))

    def train_regressor(self, job: MLJobRequest) -> MLJobResult:
        """Train a spatial regression model."""
        try:
            import joblib
            import numpy as np
            from sklearn.metrics import mean_squared_error, r2_score
            from sklearn.model_selection import train_test_split

            X, y = self._load_spatial_features(job)
            if X is None:
                return MLJobResult(
                    success=False,
                    job_type="regression",
                    algorithm=job.algorithm,
                    error="Could not load spatial features.",
                )

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            reg = self._build_sklearn_regressor(job.algorithm, job.parameters)
            reg.fit(X_train, y_train)
            preds = reg.predict(X_test)

            metrics = {
                "r2_score": float(r2_score(y_test, preds)),
                "rmse": float(np.sqrt(mean_squared_error(y_test, preds))),
                "n_train": len(X_train),
            }
            out_path = job.output_path or _temp_path(f"regressor_{job.algorithm}.joblib")
            joblib.dump(reg, out_path)

            return MLJobResult(
                success=True, job_type="regression", algorithm=job.algorithm, metrics=metrics, output_path=out_path
            )

        except ImportError as e:
            return MLJobResult(
                success=False, job_type="regression", algorithm=job.algorithm, error=f"scikit-learn not available: {e}"
            )
        except Exception as exc:
            return MLJobResult(success=False, job_type="regression", algorithm=job.algorithm, error=str(exc))

    def cluster(self, job: MLJobRequest) -> MLJobResult:
        """Perform spatial clustering (K-Means, DBSCAN)."""
        try:
            from sklearn.cluster import DBSCAN, KMeans
            from sklearn.metrics import silhouette_score

            X, _ = self._load_spatial_features(job)
            if X is None:
                return MLJobResult(
                    success=False,
                    job_type="clustering",
                    algorithm=job.algorithm,
                    error="Could not load spatial features.",
                )

            algo = job.algorithm.lower()
            if algo == "kmeans":
                k = job.parameters.get("n_clusters", 5)
                model = KMeans(n_clusters=k, random_state=42, n_init="auto")
            elif algo == "dbscan":
                model = DBSCAN(
                    eps=job.parameters.get("eps", 0.5),
                    min_samples=job.parameters.get("min_samples", 5),
                )
            else:
                return MLJobResult(
                    success=False,
                    job_type="clustering",
                    algorithm=job.algorithm,
                    error=f"Unknown clustering algorithm '{job.algorithm}'. Use kmeans or dbscan.",
                )

            labels = model.fit_predict(X)
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            sil = float(silhouette_score(X, labels)) if n_clusters > 1 and len(set(labels)) > 1 else None

            metrics = {"n_clusters": n_clusters, "n_noise": int((labels == -1).sum()) if -1 in labels else 0}
            if sil is not None:
                metrics["silhouette_score"] = sil
            # Keep the result: the input features with a "cluster" column (-1 = noise for DBSCAN)
            out = self._last_frame.copy()
            out["cluster"] = labels
            out_path = job.output_path or _temp_path(f"clusters_{algo}.gpkg")
            out.to_file(out_path, driver="GPKG")

            return MLJobResult(
                success=True, job_type="clustering", algorithm=job.algorithm, metrics=metrics, output_path=out_path
            )

        except ImportError as e:
            return MLJobResult(
                success=False, job_type="clustering", algorithm=job.algorithm, error=f"scikit-learn not available: {e}"
            )
        except Exception as exc:
            return MLJobResult(success=False, job_type="clustering", algorithm=job.algorithm, error=str(exc))

    def predict(self, job: MLJobRequest) -> MLJobResult:
        """Run inference using a pre-trained model."""
        if not job.model_path:
            return MLJobResult(
                success=False,
                job_type="predict",
                algorithm=job.algorithm,
                error="model_path is required for inference.",
            )
        try:
            import joblib

            model = joblib.load(job.model_path)
            X, _ = self._load_spatial_features(job)
            if X is None:
                return MLJobResult(
                    success=False, job_type="predict", algorithm=job.algorithm, error="Could not load input features."
                )
            preds = model.predict(X)
            return MLJobResult(
                success=True,
                job_type="predict",
                algorithm=job.algorithm,
                metrics={"n_predictions": len(preds), "sample_predictions": preds[:5].tolist()},
            )
        except ImportError as e:
            return MLJobResult(
                success=False, job_type="predict", algorithm=job.algorithm, error=f"joblib not available: {e}"
            )
        except Exception as exc:
            return MLJobResult(success=False, job_type="predict", algorithm=job.algorithm, error=str(exc))

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _dispatch(self, job: MLJobRequest) -> MLJobResult:
        jt = job.job_type.lower()
        if jt in ("classification", "regression") and not job.target_column:
            return MLJobResult(
                success=False,
                job_type=jt,
                algorithm=job.algorithm,
                error=f"{jt.capitalize()} needs a target_column: the attribute to learn.",
            )
        if jt == "classification":
            return self.train_classifier(job)
        elif jt == "regression":
            return self.train_regressor(job)
        elif jt == "clustering":
            return self.cluster(job)
        elif jt == "predict":
            return self.predict(job)
        else:
            return MLJobResult(
                success=False,
                job_type=jt,
                algorithm=job.algorithm,
                error=(
                    f"Unknown ML job type '{job.job_type}'. "
                    "Supported: classification, regression, clustering, predict"
                ),
            )

    def _load_spatial_features(self, job: MLJobRequest):
        """
        Load spatial features from input layers into numpy arrays (X, y).
        Returns (None, None) on failure.
        """
        try:
            import numpy as np

            if not job.input_layers:
                return None, None
            import geopandas as gpd

            gdf = gpd.read_file(job.input_layers[0])
            self._last_frame = gdf
            if not job.feature_columns and job.job_type.lower() == "clustering":
                # Spatial clustering: group features by where they are
                pts = gdf.geometry.representative_point()
                X = np.column_stack([pts.x.values, pts.y.values])
            else:
                cols = job.feature_columns or [c for c in gdf.columns if c not in ("geometry", job.target_column)]
                X = gdf[cols].select_dtypes(include="number").values
                if X.shape[1] == 0:
                    logger.warning("No numeric feature columns in %s", job.input_layers[0])
                    return None, None
            has_target = job.target_column and job.target_column in gdf.columns
            y = gdf[job.target_column].values if has_target else np.zeros(len(X))
            return X, y
        except Exception as exc:
            logger.warning("Feature loading failed: %s", exc)
            return None, None

    @staticmethod
    def _build_sklearn_classifier(algorithm: str, params: dict):
        from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.svm import SVC

        algo = algorithm.lower().replace("-", "_").replace(" ", "_")
        if "random_forest" in algo or algo == "rf":
            return RandomForestClassifier(n_estimators=params.get("n_estimators", 100), random_state=42)
        elif "gradient_boosting" in algo or algo == "gbm":
            return GradientBoostingClassifier(n_estimators=params.get("n_estimators", 100))
        elif "svm" in algo or "svc" in algo:
            return SVC(C=params.get("C", 1.0))
        elif "knn" in algo:
            return KNeighborsClassifier(n_neighbors=params.get("n_neighbors", 5))
        return RandomForestClassifier(random_state=42)

    @staticmethod
    def _build_sklearn_regressor(algorithm: str, params: dict):
        from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
        from sklearn.linear_model import LinearRegression, Ridge

        algo = algorithm.lower()
        if "random_forest" in algo or algo == "rf":
            return RandomForestRegressor(n_estimators=params.get("n_estimators", 100), random_state=42)
        elif "gradient_boosting" in algo:
            return GradientBoostingRegressor()
        elif "ridge" in algo:
            return Ridge(alpha=params.get("alpha", 1.0))
        return LinearRegression()

    def _persist_eval_run(self, job: MLJobRequest, result: MLJobResult) -> Optional[str]:
        """Write ML job results to geosi_eval_runs for reproducibility (FR-8)."""
        try:
            db = self._get_db()
            if db is None or not db.available:
                return None
            from geosi_data.db_models import EvalRunRecord

            record = EvalRunRecord(
                job_type=job.job_type,
                algorithm=job.algorithm,
                metrics=result.metrics,
                status="success" if result.success else "failed",
                session_id=job.session_id,
                output_path=result.output_path,
            )
            with db.get_session() as sess:
                sess.add(record)
            return str(record.id)
        except Exception as exc:
            logger.debug("Failed to persist eval run: %s", exc)
            return None

    def _get_db(self):
        try:
            if self._engine and self._engine.data:
                return self._engine.data.get("database")
        except Exception:
            logger.debug("suppressed exception", exc_info=True)
        return None

    @staticmethod
    def _path_exists(path: str) -> bool:
        import os

        return os.path.exists(path)
