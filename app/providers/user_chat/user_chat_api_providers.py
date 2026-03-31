from app.services.user_chat_service import UserChatService


def get_user_chat_service() -> UserChatService:
    return UserChatService()