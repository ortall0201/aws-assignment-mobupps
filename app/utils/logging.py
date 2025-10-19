# Module: logging.py
"""
Structured logging utilities for MobUpps API
Provides correlation ID tracking, request logging, and performance metrics
"""
import logging
import sys
import json
from datetime import datetime
from typing import Any, Dict, Optional
from contextvars import ContextVar

# Context variable for correlation ID (thread-safe for async)
correlation_id_var: ContextVar[Optional[str]] = ContextVar('correlation_id', default=None)


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logging"""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add correlation ID if available
        correlation_id = correlation_id_var.get()
        if correlation_id:
            log_data["correlation_id"] = correlation_id

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add any extra fields
        if hasattr(record, 'extra_data'):
            log_data.update(record.extra_data)

        return json.dumps(log_data)


class ColoredConsoleFormatter(logging.Formatter):
    """Colorized formatter for console output in development"""

    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESET = '\033[0m'

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, '')
        correlation_id = correlation_id_var.get()
        cid_str = f" [cid:{correlation_id[:8]}]" if correlation_id else ""

        log_msg = f"{color}{record.levelname}{self.RESET} [{record.name}]{cid_str} {record.getMessage()}"

        if record.exc_info:
            log_msg += "\n" + self.formatException(record.exc_info)

        return log_msg


def setup_logging(level: str = "INFO", structured: bool = False) -> None:
    """
    Configure application logging

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        structured: If True, use JSON formatting; if False, use colored console
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    root_logger.handlers.clear()

    # Create console handler
    handler = logging.StreamHandler(sys.stdout)

    # Set formatter based on mode
    if structured:
        formatter = StructuredFormatter()
    else:
        formatter = ColoredConsoleFormatter()

    handler.setFormatter(formatter)
    root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for a module"""
    return logging.getLogger(name)


def set_correlation_id(correlation_id: str) -> None:
    """Set the correlation ID for the current request context"""
    correlation_id_var.set(correlation_id)


def get_correlation_id() -> Optional[str]:
    """Get the correlation ID for the current request context"""
    return correlation_id_var.get()


def log_request(logger: logging.Logger, method: str, path: str, **kwargs: Any) -> None:
    """Log an incoming HTTP request"""
    extra_data = {
        "event_type": "http_request",
        "http_method": method,
        "http_path": path,
        **kwargs
    }
    logger.info(f"{method} {path}", extra={'extra_data': extra_data})


def log_response(logger: logging.Logger, status_code: int, latency_ms: float, **kwargs: Any) -> None:
    """Log an HTTP response"""
    extra_data = {
        "event_type": "http_response",
        "status_code": status_code,
        "latency_ms": latency_ms,
        **kwargs
    }
    logger.info(f"Response {status_code} ({latency_ms:.2f}ms)", extra={'extra_data': extra_data})


def log_ab_assignment(logger: logging.Logger, partner_id: str, app_id: str, arm: str, **kwargs: Any) -> None:
    """Log an A/B test arm assignment"""
    extra_data = {
        "event_type": "ab_assignment",
        "partner_id": partner_id,
        "app_id": app_id,
        "ab_arm": arm,
        **kwargs
    }
    logger.info(f"A/B assignment: {arm}", extra={'extra_data': extra_data})
