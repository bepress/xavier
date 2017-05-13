Xavier: An AWS Lambda Python Bot Framework
==========================================

Xavier is a bot framework. Specially built to operate on AWS Lambda.


Example
-------

.. code-block:: python

	import os
	import logging
	import sys

	from xavier.active import register_brain
	from xavier.brain import Brain
	from xavier.aws.func import build_lambda_router
	from xavier.slack.slash import SlashCommandEvent
	from xavier.http import Response, Router
	from xavier.offline import BackgroundQueue
	from xavier.aws.sns import publish_sns_message, handle_sns_message, handle_sns_schedule

	xavier = Brain(env=env)
	register_brain(xavier_bot)

	background_queue = BackgroundQueue(publish_sns_message('arn:background_task'))
	router = Router()

	@background_queue.task()
	def offline_find(slash_command):
	    if slash_command.text == 'Hi':
	    	slash_command.respond({'text': "Howdy"})
		else:
			slash_command.respond({'text': "Hi"})


	@router.add_route("/slack/commands/hello", methods=['POST'])
	def handle_find(request):
	    slash_command = SlashCommandEvent.from_request(request)
	    offline_task.delay(slash_command)
	    return Response(204, "")


	@background_queue.task(schedule=['aaa'])
	def offline_cron(slash_command):
		...

	lambda_schedule_hander = handle_sns_schedule(background_queue.process_schedule)
	lambda_sns_handler = handle_sns_messages(background_queue.process_event)
	lambda_http_handler = build_lambda_router(router)
