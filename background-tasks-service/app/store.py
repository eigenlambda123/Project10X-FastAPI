from uuid import UUID

# Global in-memory task registry
task_store: dict[UUID, dict] = {}