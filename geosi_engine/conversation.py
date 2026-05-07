# -*- coding: utf-8 -*-
"""
GeoSI Conversation Manager — Maintains multi-turn dialogue history for interactive Ollama sessions.
"""

import json
from typing import List, Dict, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class Message:
    """Single message in a conversation."""
    role: str  # "user", "assistant", "system"
    content: str
    metadata: Dict = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)


class ConversationManager:
    """
    Manages multi-turn conversation history for interactive LLM sessions.
    Maintains context across queries for natural dialogue flow.
    """

    def __init__(self, max_history: int = 20, system_prompt: Optional[str] = None):
        """
        Initialize conversation manager.
        
        Args:
            max_history: Maximum number of turns to keep in history
            system_prompt: Optional system message to set LLM behavior
        """
        self.max_history = max_history
        self.history: List[Message] = []
        self.system_prompt = system_prompt
        
        if system_prompt:
            self.history.append(Message(role="system", content=system_prompt))

    def add_user_message(self, content: str, metadata: Optional[Dict] = None) -> None:
        """Add user message to history."""
        msg = Message(role="user", content=content, metadata=metadata or {})
        self.history.append(msg)
        self._trim_history()

    def add_assistant_message(self, content: str, metadata: Optional[Dict] = None) -> None:
        """Add assistant response to history."""
        msg = Message(role="assistant", content=content, metadata=metadata or {})
        self.history.append(msg)
        self._trim_history()

    def get_context(self, include_system: bool = True) -> str:
        """
        Build formatted conversation context for LLM prompts.
        
        Args:
            include_system: Whether to include system message
            
        Returns:
            Formatted conversation history
        """
        context_lines = []
        for msg in self.history:
            if msg.role == "system" and not include_system:
                continue
            context_lines.append(f"{msg.role.upper()}: {msg.content}")
        return "\n".join(context_lines)

    def get_messages_for_api(self, exclude_system: bool = False) -> List[Dict]:
        """
        Get messages formatted for API calls (OpenAI-style).
        
        Args:
            exclude_system: Whether to exclude system messages
            
        Returns:
            List of message dicts with role and content
        """
        messages = []
        for msg in self.history:
            if msg.role == "system" and exclude_system:
                continue
            messages.append({"role": msg.role, "content": msg.content})
        return messages

    def get_user_queries(self) -> List[str]:
        """Get all user queries from history (excludes assistant responses)."""
        return [msg.content for msg in self.history if msg.role == "user"]

    def get_last_exchange(self) -> Optional[tuple]:
        """Get last user-assistant exchange as (user_msg, assistant_msg) tuple."""
        user_msg = None
        assistant_msg = None
        
        for msg in reversed(self.history):
            if msg.role == "assistant" and not assistant_msg:
                assistant_msg = msg.content
            elif msg.role == "user" and not user_msg:
                user_msg = msg.content
            
            if user_msg and assistant_msg:
                return (user_msg, assistant_msg)
        
        return None

    def clear(self) -> None:
        """Clear conversation history (keeps system prompt if set)."""
        if self.system_prompt:
            self.history = [Message(role="system", content=self.system_prompt)]
        else:
            self.history = []

    def _trim_history(self) -> None:
        """Keep only recent messages, respecting max_history limit."""
        # Always keep system message if present
        system_msgs = [m for m in self.history if m.role == "system"]
        other_msgs = [m for m in self.history if m.role != "system"]
        
        if len(other_msgs) > self.max_history:
            other_msgs = other_msgs[-self.max_history:]
        
        self.history = system_msgs + other_msgs

    def to_json(self) -> str:
        """Serialize conversation to JSON."""
        return json.dumps(
            [msg.to_dict() for msg in self.history],
            indent=2
        )

    def from_json(self, json_str: str) -> None:
        """Load conversation from JSON."""
        try:
            data = json.loads(json_str)
            self.history = [
                Message(
                    role=msg.get("role"),
                    content=msg.get("content"),
                    metadata=msg.get("metadata", {})
                )
                for msg in data
            ]
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid conversation JSON: {e}")

    def __len__(self) -> int:
        """Return number of messages (excluding system message)."""
        return len([m for m in self.history if m.role != "system"])

    def __str__(self) -> str:
        """String representation of conversation."""
        return f"ConversationManager(turns={len(self)}, system_prompt={'Yes' if self.system_prompt else 'No'})"
