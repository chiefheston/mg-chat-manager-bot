from dataclasses import dataclass, field

from constants import JOIN_LATER, JOIN_NEVER, JOIN_NOW
from enums import ChatPriority

MESSAGE_BY_PRIORITY = {
    ChatPriority.HIGH: JOIN_NOW,
    ChatPriority.MEDIUM: JOIN_LATER,
    ChatPriority.LOW: JOIN_NEVER,
}


@dataclass(slots=True)
class Chat:
    id: int
    name: str
    invite_link: str
    priority: ChatPriority


@dataclass(slots=True)
class InviteMessageView:
    _chats: list[Chat] = field(default_factory=list, init=False)
    _chats_by_priority: dict[ChatPriority, list[Chat]] = field(init=False)

    def append_chat(self, chat: Chat):
        self._chats.append(chat)

        if self._chats_by_priority.get(chat.priority) is not None:
            self._chats_by_priority[chat.priority].append(chat)
        else:
            self._chats_by_priority[chat.priority] = [chat]

    def to_text(self) -> str | None:
        parts = []

        for priority, chats in self._chats_by_priority.items():
            if len(chats) > 0:
                priority_message = MESSAGE_BY_PRIORITY[priority]
                part = self._generate_part(priority_message, chats)
                parts.append(part)

        if len(parts) > 0:
            return '\n\n'.join(parts)

        return None

    def get_chats(self) -> list[Chat]:
        return self._chats

    def _generate_part(self, priority_message: str, chats: list[Chat]) -> str:
        invite_strings = [
            self._generate_invite_string(priority_chat) for priority_chat in chats
        ]

        part = priority_message + '\n'.join(
            f'— {invite_string}' for invite_string in invite_strings
        )

        return part

    @staticmethod
    def _generate_invite_string(chat: Chat) -> str:
        return f'{chat.name}:\n{chat.invite_link}'
