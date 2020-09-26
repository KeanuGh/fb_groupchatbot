from fbchat import log, Client
from fbchat.models import *
from dotenv import load_dotenv
from bot_functions import *
import os
import random

# env variables
load_dotenv()
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASWD')

# dictionaries of reply-responses
quick_replies = {
    "bot speak": "woof!",
    "good bot": "🥰",
    "sexy bot": "😉",
    "thanks bot": "no problem",
    "thank you bot": "you're welcome!",
    "ty bot": "np",
}
quick_reacts = {
    "good bot": MessageReaction.HEART,
    "bad bot": MessageReaction.SAD,
    "kill yourself bot": MessageReaction.ANGRY,
}


class BarelyKnowHerBot(Client):
    def __init__(self, email, password):

        # =================================
        # ------------ STATES -------------
        # =================================

        self.SHUT_UP = False

        super().__init__(email, password)

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        # don't reply to self
        is_self = (author_id == self.uid)

        # just look at text messages
        if message_object.text is not None\
                and not is_self:

            # get message message stripped of nonalphanumeric chars & trailing whitespace
            message = message_object.text
            message_stripped = clean_message(message)

            # speak and don't speak
            if message_stripped in ('bot shut up', 'shut up bot'):
                if not self.SHUT_UP:
                    self.reactToMessage(message_id=message_object.uid, reaction=MessageReaction.YES)
                    self.SHUT_UP = True
            elif 'bot speak' == message_stripped:
                if self.SHUT_UP:
                    # if starting to speak again after being silenced, thumb up message
                    self.reactToMessage(message_id=message_object.uid, reaction=MessageReaction.YES)
                    self.SHUT_UP = False

            # =================================
            # ---------- REACTIONS ------------
            # =================================

            # simple reply-reactions
            if message_stripped in quick_reacts:
                self.reactToMessage(message_id=message_object.uid, reaction=quick_reacts[message_stripped])

            # bot appreciates a good joke (but doesn't laugh at its own jokes)
            elif 'i hardly know her' in message_stripped and author_id != self.uid:
                self.reactToMessage(message_id=message_object.uid, reaction=MessageReaction.SMILE)

            # =================================
            # ---------- REPLIES --------------
            # =================================

            # - dont reply if bot is silenced -
            if not self.SHUT_UP:
                # check if bot can make a rip-roaringly hilarious joke

                # simple reply-responses
                if message_stripped in quick_replies:
                    self.send(Message(text=quick_replies[message_stripped], reply_to_id=message_object.uid),
                              thread_id=thread_id, thread_type=thread_type)

                # absolutely hilarious joke
                # reply if not replying to self, and passing a roll
                elif random.random() < .2 \
                        and (funny_quip := hardly_know_em(message_stripped)):
                    log.info(f'The message: "\n{message}\n" contains a hilarious word. Will reply now!')

                    self.send(Message(text=funny_quip, reply_to_id=message_object.uid),
                              thread_id=thread_id, thread_type=thread_type)

                # haiku detection (only if more than 3 words)
                elif len(message_stripped.split()) < 4 \
                        and (haiku := haiku_detection(message_stripped)):
                    self.send(Message(text=haiku, reply_to_id=message_object.uid),
                              thread_id=thread_id, thread_type=thread_type)

                # ___ boy and lava girl
                elif 'boy' in message_stripped:
                    if reply := boy_and_lavagirl(message_stripped):
                        self.send(Message(text=reply, reply_to_id=message_object.uid),
                                  thread_id=thread_id, thread_type=thread_type)

            # =================================
            # ------------ MISC ---------------
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


# run bot
client = BarelyKnowHerBot(EMAIL, PASSWORD)
client.listen()
