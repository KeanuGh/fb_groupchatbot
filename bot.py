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
    "kill yourself bot": MessageReaction.ANGRY,
    "shut up bot": MessageReaction.YES,
    "bot shut up": MessageReaction.YES,
}


class BarelyKnowHerBot(Client):
    def __init__(self, email, password):

        # ---------STATES-----------
        self.SHUT_UP = False
        # --------/STATES-----------

        super().__init__(email, password)

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        # just look at text messages
        if message_object.text is not None:
            message = message_object.text
            message_stripped = clean_message(message)

            funny_quip = hardly_know_em(message_stripped)

            # speak and don't speak
            if message_stripped in ('bot shut up', 'shut up bot'):
                self.SHUT_UP = True
            elif 'bot speak' == message_stripped:
                if self.SHUT_UP:
                    self.reactToMessage(message_id=message_object.uid, reaction=MessageReaction.YES)
                    self.SHUT_UP = False

            # =================================
            # ---------- REACTIONS ------------

            # simple reply-reactions
            if message_stripped in react_replies:
                self.reactToMessage(message_id=message_object.uid, reaction=react_replies[message_stripped])

            # bot appreciates a good joke (but doesn't laugh at its own jokes)
            elif 'i hardly know her' in message_stripped and author_id != self.uid:
                self.reactToMessage(message_id=message_object.uid, reaction=MessageReaction.SMILE)

            # -------- /REACTIONS -------------
            # =================================

            # =================================
            # ---------- REPLIES --------------

            # - dont reply if bot is silenced -
            if not self.SHUT_UP:

                # simple reply-responses
                if message_stripped in quick_replies:
                    self.send(Message(text=quick_replies[message_stripped], reply_to_id=message_object.uid),
                              thread_id=thread_id, thread_type=thread_type)

                # absolutely hilarious joke
                # reply if not replying to self, and passing a roll
                elif funny_quip \
                        and author_id != self.uid \
                        and random.random() < .2:
                    log.info(f"The message: \n{message}\n contains a hilarious word. Will reply now!")

                    self.send(Message(text=funny_quip, reply_to_id=message_object.uid), thread_id=thread_id,
                              thread_type=thread_type)

            # ---------- /REPLIES -------------
            # =================================

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
