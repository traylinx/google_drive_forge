import os
import datetime
import logging

logger = logging.getLogger(__name__)

class AuditLogger:
    def __init__(self, audit_log_path: str):
        self.audit_log_path = audit_log_path
        # Ensure directory exists
        os.makedirs(os.path.dirname(audit_log_path), exist_ok=True)

    def log_event(self, event_type: str, details: str, status: str = "INFO"):
        """
        Logs an intelligent operation event.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{status}] [{event_type}] {details}\n"
        
        try:
            with open(self.audit_log_path, "a") as f:
                f.write(log_entry)
        except Exception as e:
            logger.error(f"Failed to write to audit log: {e}")

    def log_recovery(self, original_id: str, recovered_name: str, success: bool):
        """
        Specific log for autonomous recovery events.
        """
        status = "SUCCESS" if success else "FAILURE"
        self.log_event("RECOVERY", f"Target ID: {original_id} -> Found: {recovered_name}", status)

    def log_skill_creation(self, skill_name: str):
        """
        Specific log for new skill forging.
        """
        self.log_event("SKILL_FORGE", f"New capability created: {skill_name}")
