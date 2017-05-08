import requests
import json


class SlashCommandException(Exception):
    pass


class SlashCommandEvent(object):
    def __init__(self, token, team_id, team_domain,
                 channel_id, channel_name, user_id,
                 user_name, command, text, response_url):

        self.token = token
        self.team_id = team_id
        self.team_domain = team_domain
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.user_id = user_id
        self.user_name = user_name
        self.command = command
        self.text = text
        self.response_url = response_url

    @classmethod
    def from_request(cls, request, token=None):
        event = cls(**request.parse_body())
        if token and event.token != token:
            assert SlashCommandException('Invalid token: {}'.format(event.token))

        return event

    def respond(self, message):
        resp = requests.post(self.response_url, data=json.dumps(message), headers={"Content-Type": "application/json"})
        resp.raise_for_status()
