Xavier: An AWS Lambda Python Bot Framework
==========================================

Xavier is a bot framework. Specially built to operate on AWS Lambda.


Example
-------

.. code-block:: python

	import os
	import logging
	import sys

	from xavier.active import register_bot
	from xavier.bot import Bot
	from xavier.aws.func import build_lambda_router_for_bot
	from xavier.slack.slash import SlashCommandEvent
	from xavier.http import Response

	xavier_bot = Bot(env=env)
	register_bot(xavier_bot)

	@xavier_bot.add_route("/slack/commands/hello", methods=['POST'])
	def handle_find(request):
	    slash_command = SlashCommandEvent.from_request(request)
	    if slash_command.text == 'Hi':
	    	slash_command.respond({'text': "Howdy"})
		else:
			slash_command.respond({'text': "Hi"})

	    return Response(204, "")

	lambda_http_handler = build_lambda_router_for_bot(xavier_bot)

