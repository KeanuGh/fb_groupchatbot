from fbchat import log, Client, MessageReaction
from fbchat.models import *
from dotenv import load_dotenv
from bot_functions import *
import string
import os
import random

load_dotenv()
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASWD')


class BarelyKnowHerBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        # just look at text messages
        if message_object.text is not None:
            message = message_object.text
            message_stripped = message.lower().translate(str.maketrans('', '', string.punctuation))

            if message_stripped == "bot speak":
                self.send(Message(text="woof!"), thread_id=thread_id, thread_type=thread_type)
            elif message_stripped == "good bot":
                self.reactToMessage(message_id=message_object.uid, reaction=MessageReaction.HEART)

            # absolutely hilarious joke
            # reply if not replying to self, and passing a roll
            reply = good_word(message)
            if reply \
                    and author_id != self.uid \
                    and random.random() < 0.2:
                log.info(f"The message: \n{message}\n contains a hilarious word. Will reply now!")

                funny_quip = f'{reply}? I hardly know her!'
                self.send(Message(text=funny_quip, reply_to_id=message_object.uid), thread_id=thread_id,
                          thread_type=thread_type)
            else:
                # Sends the data to the inherited onMessage, so that we can still see when a message is received
                super(BarelyKnowHerBot, self).onMessage(
                    author_id=author_id,
                    message_object=message_object,
                    thread_id=thread_id,
                    thread_type=thread_type,
                    **kwargs
                )


client = BarelyKnowHerBot(EMAIL, PASSWORD)
client.listen()

