
# Imports
from config import *
from src.print import *
from autogen_core import MessageContext, RoutedAgent, default_subscription, message_handler

@default_subscription
class SimpleAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("A simple agent that prints received messages.")

    @message_handler
    async def handle_message(self, message: Message, ctx: MessageContext) -> None:
        print(f"Received message: {message.content}")

