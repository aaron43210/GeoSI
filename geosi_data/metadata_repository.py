"""
GeoSI Data Layer — Metadata Repository
═══════════════════════════════════════════════════════════════════

Stores and queries workflow history and execution results.
This is the persistence backend for the knowledge/memory layer —
every query → plan → result cycle is recorded here for future
retrieval and learning.
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("geosi_data.metadata_repository")


class MetadataRepository:
    """
    Repository for workflow history and execution results.

    Usage:
        repo = MetadataRepository(database)
        repo.store_execution_result(query, plan, result)
        history = repo.get_workflow_history(limit=20)
    """

    def __init__(self, database):
        self.db = database

    def store_execution_result(
        self,
        query: str,
        plan: Any,
        result: Any,
    ) -> Optional[str]:
        """
        Store a complete execution cycle (query → plan → result).

        Args:
            query: Original user query text
            plan: ExecutionPlan object (will be serialized to JSON)
            result: ExecutionResult object (will be serialized to JSON)

        Returns:
            Workflow history record ID, or None if storage failed.
        """
        if not self.db.available:
            return None

        from geosi_data.db_models import (
            ExecutionResultRecord,
            WorkflowHistoryRecord,
        )

        try:
            # Serialize plan
            plan_data = None
            tool_sequence = []
            intent = None
            if plan:
                plan_data = {
                    "plan_id": getattr(plan, "plan_id", ""),
                    "reasoning": getattr(plan, "reasoning", ""),
                    "steps": [
                        {
                            "step_id": s.step_id,
                            "tool_name": s.tool_name,
                            "parameters": s.parameters,
                            "output_name": s.output_name,
                            "description": s.description,
                        }
                        for s in (plan.steps or [])
                    ],
                }
                tool_sequence = [s.tool_name for s in (plan.steps or [])]
                if plan.request:
                    intent_obj = plan.request.intent
                    intent = intent_obj.value if hasattr(intent_obj, "value") else str(intent_obj)

            # Serialize result
            result_data = None
            status = "unknown"
            duration = 0.0
            error_msg = None
            if result:
                status = "success" if result.success else "failed"
                duration = getattr(result, "total_duration_ms", 0.0)
                error_msg = getattr(result, "error", None)
                result_data = {
                    "success": result.success,
                    "answer": getattr(result, "answer", ""),
                    "reasoning": getattr(result, "reasoning", ""),
                    "error": error_msg,
                    "total_duration_ms": duration,
                }

            with self.db.get_session() as session:
                # Create workflow history record
                workflow = WorkflowHistoryRecord(
                    query=query,
                    intent=intent,
                    plan_json=plan_data,
                    result_json=result_data,
                    status=status,
                    duration_ms=duration,
                    tool_sequence=tool_sequence,
                    error_message=error_msg,
                )
                session.add(workflow)
                session.flush()

                # Create per-step execution records
                if result and hasattr(result, "logs"):
                    for log in result.logs:
                        step_record = ExecutionResultRecord(
                            workflow_id=workflow.id,
                            step_id=log.step_id,
                            tool_name=log.tool_name,
                            status=log.status.value if hasattr(log.status, "value") else str(log.status),
                            duration_ms=log.duration_ms,
                            output_features=log.output_features,
                            error_message=log.error_message,
                        )
                        session.add(step_record)

                logger.info(
                    f"Stored workflow history: query='{query[:50]}...', " f"status={status}, {len(tool_sequence)} tools"
                )
                return workflow.id

        except Exception as e:
            logger.error(f"Failed to store execution result: {e}")
            return None

    def get_workflow_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent workflow history, most recent first.

        Args:
            limit: Maximum number of records to return.

        Returns:
            List of workflow history dicts.
        """
        if not self.db.available:
            return []

        from geosi_data.db_models import WorkflowHistoryRecord

        try:
            with self.db.get_session() as session:
                records = (
                    session.query(WorkflowHistoryRecord)
                    .order_by(WorkflowHistoryRecord.created_at.desc())
                    .limit(limit)
                    .all()
                )
                return [self._workflow_to_dict(r) for r in records]
        except Exception as e:
            logger.error(f"Failed to get workflow history: {e}")
            return []

    def search_history(self, query_text: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search workflow history by query text (ILIKE pattern match).

        Args:
            query_text: Search text
            limit: Maximum results

        Returns:
            Matching workflow history records.
        """
        if not self.db.available:
            return []

        from geosi_data.db_models import WorkflowHistoryRecord

        try:
            with self.db.get_session() as session:
                records = (
                    session.query(WorkflowHistoryRecord)
                    .filter(WorkflowHistoryRecord.query.ilike(f"%{query_text}%"))
                    .order_by(WorkflowHistoryRecord.created_at.desc())
                    .limit(limit)
                    .all()
                )
                return [self._workflow_to_dict(r) for r in records]
        except Exception as e:
            logger.error(f"Failed to search history: {e}")
            return []

    def get_tool_statistics(self) -> Dict[str, Dict[str, Any]]:
        """
        Get per-tool execution statistics (success rate, avg duration).

        Returns:
            Dict mapping tool_name → {total, success, fail, avg_ms}
        """
        if not self.db.available:
            return {}

        from sqlalchemy import func

        from geosi_data.db_models import ExecutionResultRecord

        try:
            with self.db.get_session() as session:
                results = (
                    session.query(
                        ExecutionResultRecord.tool_name,
                        func.count().label("total"),
                        func.sum((ExecutionResultRecord.status == "success").cast(int)).label("success_count"),
                        func.avg(ExecutionResultRecord.duration_ms).label("avg_ms"),
                    )
                    .group_by(ExecutionResultRecord.tool_name)
                    .all()
                )
                stats = {}
                for row in results:
                    total = row.total or 0
                    success = row.success_count or 0
                    stats[row.tool_name] = {
                        "total": total,
                        "success": success,
                        "fail": total - success,
                        "success_rate": success / total if total > 0 else 0.0,
                        "avg_duration_ms": float(row.avg_ms or 0),
                    }
                return stats
        except Exception as e:
            logger.error(f"Failed to get tool statistics: {e}")
            return {}

    @staticmethod
    def _workflow_to_dict(record) -> Dict[str, Any]:
        """Convert a WorkflowHistoryRecord to a plain dict."""
        return {
            "id": record.id,
            "query": record.query,
            "intent": record.intent,
            "plan": record.plan_json,
            "result": record.result_json,
            "status": record.status,
            "duration_ms": record.duration_ms,
            "tool_sequence": record.tool_sequence,
            "error_message": record.error_message,
            "created_at": record.created_at.isoformat() if record.created_at else None,
        }
