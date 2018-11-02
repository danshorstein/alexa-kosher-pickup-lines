# -*- coding: utf-8 -*-
"""Kosher pickup lines app."""

import random
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response


# =========================================================================================================================================
# TODO: The items below this comment need your attention.
# =========================================================================================================================================
SKILL_NAME = "Kosher Pickup Lines"
GET_LINE_MESSAGE = "Here's your pickup line: "
HELP_MESSAGE = "You can say tell me a pickup line, or, you can say exit... What can I help you with?"
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "The Kosher pickup lines skill can't help you with that.  It can help you with pickup lines if you say tell me a pickup line. What can I help you with?"
FALLBACK_REPROMPT = 'What can I help you with?'
EXCEPTION_MESSAGE = "Sorry. I cannot help you with that."


data = '''You had me at shabbat shalom.
Hey baby, I'll be your MANishewitz.
Pray here often?
Would you light my shabbas candles?
That's a nice looking kipah. it would look even better on my floor tomorrow morning.
I'll take the rest out of your day of rest.
I put the syn in synagogue.
Excuse me ladies, would you like to help me make a quadruple mitzvah?
You must not be shomer shabbas, because you just turned me on.
Kiss me, I'm Kosher.
Eat me, I'm Kosher.
Want to find out how salty my matzoh balls are?
Is that a siddur in your pocket, or are you just happy to see me?
Are you my prize for finding the Afikomen?
Is that the afikoman in your pants or are you just happy to see me?
I'll give you a burning bush.
Do you want something to atone for on Yom Kippur?
I'd like to dip my apple in your honey
I've got a tekiah gedolah for you baby
Would you like to blow my shofar?
Nice Hanukkah bush.
Wanna play spin the dreidel?
Is that sour cream on your latke or were you just happy to see me?
All I want for Christmas is Jew
Hey Rabbi, you had me at "please rise"
Hey baby, wanna shake my lulav?
Is there an afikomen in your pocket, or are you just happy to see me?
Please give me some maror of that gefilte fish.
My kitchen is totally kosher for Passover.
I have two sets of dishes. 
I couldn't help noticing that shank bone on your plate.
Why don't you come over and I'll SHOW you what makes this night different from all other nights.
I make a great matzah brie in the morning
I'll show you my charoset recipe if you show me yours
Hey baby, let's make a Hanukkah miracle and see if I can last 8 nights!
I'll show you my Christmas tree if you show me your Hanukkah bush!
Just meeting you made me want to break a glass.
Hey baby, I wanna see your Shabbat ShalOm face!'''.split('\n')


# =========================================================================================================================================
# Editing anything below this line might break your skill.
# =========================================================================================================================================

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Built-in Intent Handlers
class GetNewPickupLineHandler(AbstractRequestHandler):
    """Handler for Skill Launch and GetNewPickupLine Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("GetNewPickupLineIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In GetNewPickupLineHandler")

        random_line = random.choice(data)
        speech = GET_LINE_MESSAGE + random_line

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, random_line))
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.

    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(FALLBACK_MESSAGE).ask(
            FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)

        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(GetNewPickupLineHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# TODO: Uncomment the following lines of code for request, response logs.
# sb.add_global_request_interceptor(RequestLogger())
# sb.add_global_response_interceptor(ResponseLogger())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()
