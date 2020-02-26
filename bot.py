# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

#bot
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
#google translate
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/wenyentseng/Downloads/key/ornate-bond-268804-1834cb83fa5a.json"

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types

    async def on_message_activity(self, turn_context: TurnContext):
        await turn_context.send_activity(f"Bot: '{ turn_context.activity.text }'")

    async def on_members_added_activity(
        self,
        members_added: ChannelAccount,
        turn_context: TurnContext
    ):
        for member_added in members_added:
            if member_added.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello and welcome!")

            
#detect_intent_texts('ornate-bond-268804', '12345', 'enAgent', ['test en bot'], 'en')
#detect_intent_texts('southern-bonsai-269210', '12345', 'twAgent', ['測試台灣客服'], 'tw')