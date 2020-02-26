# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

#bot
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount
#google translate
from google.cloud import translate_v2 as translate
import os
import dialogflow_v2 as dialogflow
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/wenyentseng/Downloads/key/ornate-bond-268804-1834cb83fa5a.json"

class MyBot(ActivityHandler):
    # See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.
    def detect_intent_texts(self, project_id, session_id, agent, texts, language_code):
        session_client = dialogflow.SessionsClient()

        session = session_client.session_path(project_id, session_id)
        for text in texts:
            text_input = dialogflow.types.TextInput(
                text=text, language_code=language_code)

            query_input = dialogflow.types.QueryInput(text=text_input)

            response = session_client.detect_intent(
                session=session, query_input=query_input)

            print('=' * 20)
            print('Query text: {}'.format(response.query_result.query_text))
            print('Detected intent: {} (confidence: {})\n'.format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence))
            print('Fulfillment text: {}\n'.format(
                response.query_result.fulfillment_text))
        return response.query_result.fulfillment_text

    async def on_message_activity(self, turn_context: TurnContext):
        translate_client = translate.Client()
        result = translate_client.detect_language(turn_context.activity.text)
        await turn_context.send_activity(f"Language : {result['language']}, Confidence: {result['confidence']}")
        lang_code = 'en'
        lang_agent = 'enAgent'
        project_id = 'ornate-bond-268804'
        if result['language'] == 'en':
            lang_code ='en'
            lang_agent = 'enAgent'
            project_id = 'ornate-bond-268804'
        elif result['language'] == 'zh-TW':
            lang_code ='tw'
            lang_agent = 'twAgent'
            project_id = 'southern-bonsai-269210'
        await turn_context.send_activity(lang_code+' '+ lang_agent+ " "+ project_id)
        response_text = self.detect_intent_texts(project_id, '12345', lang_agent, [turn_context.activity.text], lang_code)
        await turn_context.send_activity(f"Bot: '{ response_text }'")

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