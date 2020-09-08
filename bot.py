from fbchat import log, Client
from fbchat.models import *
from dotenv import load_dotenv
from bot_functions import *
import os
import random

load_dotenv()
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASWD')

# dictionaries of reply-responses
quick_replies = {
    "bot speak": "woof!",
    "good bot": "🥰",
    "sexy bot": "😉",
}
react_replies = {
    "good bot": MessageReaction.HEART,
    "bad bot": MessageReaction.SAD,
}


class BarelyKnowHerBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        # just look at text messages
        if message_object.text is not None:
            message = message_object.text
            message_stripped = clean_message(message)

            funny_word = good_word(message_stripped)

            # simple reply-responses
            if message_stripped in quick_replies:
                self.send(Message(text=quick_replies[message_stripped], reply_to_id=message_object.uid),
                          thread_id=thread_id, thread_type=thread_type)
            if message_stripped in react_replies:
                self.reactToMessage(message_id=message_object.uid, reaction=react_replies[message_stripped])

            # bot appreciates a good joke (but doesn't laugh at its own jokes)
            elif 'i hardly know her' in message_stripped and author_id != self.uid:
                self.reactToMessage(message_id=message_object.uid, reaction=MessageReaction.SMILE)

            # absolutely hilarious joke
            # reply if not replying to self, and passing a roll
            elif funny_word \
                    and author_id != self.uid \
                    and random.random() < .2:
                log.info(f"The message: \n{message}\n contains a hilarious word. Will reply now!")

                funny_quip = f'{funny_word}? I hardly know her!'
                self.send(Message(text=funny_quip, reply_to_id=message_object.uid), thread_id=thread_id,
                          thread_type=thread_type)

            else:
                # special surprise
                if random.random() < .001:
                    self.send(Message(text='𓀐𓂸'), thread_id=thread_id, thread_type=thread_type)
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
