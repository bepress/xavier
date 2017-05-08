"""
AWS Lambda Utils
----------------

Functions and classes that make working with lambda easier

Example Event
=============

{u'body': None,
 u'headers': {u'Accept': u'*/*',
              u'Accept-Encoding': u'gzip, deflate',
              u'CloudFront-Forwarded-Proto': u'https',
              u'CloudFront-Is-Desktop-Viewer': u'true',
              u'CloudFront-Is-Mobile-Viewer': u'false',
              u'CloudFront-Is-SmartTV-Viewer': u'false',
              u'CloudFront-Is-Tablet-Viewer': u'false',
              u'CloudFront-Viewer-Country': u'US',
              u'Host': u'zih8gs4uja.execute-api.us-west-2.amazonaws.com',
              u'User-Agent': u'HTTPie/0.9.2',
              u'Via': u'1.1 28fd9501206a11a06951e60ad8a996fd.cloudfront.net (CloudFront)',
              u'X-Amz-Cf-Id': u'bCwUp5PccOol5Fe4hiTLA3k-c4UEdaGqxk6jHIdHRxyW27mzKqnPkA==',
              u'X-Amzn-Trace-Id': u'Root=1-58fc1e9e-165b6a031797c7e57c5bda0e',
              u'X-Forwarded-For': u'67.166.124.36, 54.182.238.75',
              u'X-Forwarded-Port': u'443',
              u'X-Forwarded-Proto': u'https',
              u'x-api-key': u'54bUUzjrml4sQWuJiZP51EEQYe45g3j6rAuMjwO5'},
 u'httpMethod': u'GET',
 u'isBase64Encoded': False,
 u'path': u'/abc',
 u'pathParameters': {u'proxy': u'abc'},
 u'queryStringParameters': {u'a': u'3', u'b': u'2'},
 u'requestContext': {u'accountId': u'140099371219',
                     u'apiId': u'zih8gs4uja',
                     u'httpMethod': u'GET',
                     u'identity': {u'accessKey': None,
                                   u'accountId': None,
                                   u'apiKey': u'54bUUzjrml4sQWuJiZP51EEQYe45g3j6rAuMjwO5',
                                   u'caller': None,
                                   u'cognitoAuthenticationProvider': None,
                                   u'cognitoAuthenticationType': None,
                                   u'cognitoIdentityId': None,
                                   u'cognitoIdentityPoolId': None,
                                   u'sourceIp': u'67.166.124.36',
                                   u'user': None,
                                   u'userAgent': u'HTTPie/0.9.2',
                                   u'userArn': None},
                     u'requestId': u'7997f0d1-27d4-11e7-b03b-277e30e86ae4',
                     u'resourceId': u'dtl0zo',
                     u'resourcePath': u'/{proxy+}',
                     u'stage': u'prod'},
 u'resource': u'/{proxy+}',
 u'stageVariables': None}

"""
import json
from urllib.parse import parse_qs

from frozendict import frozendict
from functools import partial

from xavier.http import Response, HTTPError


class LambdaHTTPEvent(object):
    def __init__(self, method='GET', path=None, body=None, params=None, headers=None, request_context=None, raw_event=None):
        params = params if params else {}
        headers = headers if headers else {}

        self.method = method
        self.path = path
        self.body = body
        self.params = frozendict(params)
        self.headers = frozendict(headers)
        self.request_context = request_context
        self.raw_event = raw_event

    @classmethod
    def from_raw_event(cls, event):
        method = event.get('httpMethod')
        path = event.get('path')
        params = event.get('queryStringParameters', {})
        body = event.get('body')
        headers = event.get('headers')
        request_context = event.get('requestContext')

        return cls(method, path, body, params, headers, request_context, event)

    def parse_body(self):
        if self.headers.get('Content-Type', '').startswith('application/json'):
            return json.loads(self.body)
        else:
            return parse_qs(self.body)


def build_response(response):

    return {
        'statusCode': str(response.status_code),
        'body': response.render(),
        'headers': response.headers,
    }


def lambda_http_handler(bot, event, context):
    lambda_http_event = LambdaHTTPEvent.from_raw_event(event)
    contoller = bot.find_route(lambda_http_event.path)
    if not contoller:
        return build_response(
            Response(404, "Missing route")
        )

    try:
        response = contoller['view'](lambda_http_event)
        return build_response(response)
    except HTTPError as e:
        return build_response(
            Response(e.status_code, e.message)
        )
    except Exception as e:
        return build_response(
            Response(500, 'Server error')
        )


def build_lambda_router_for_bot(bot):
    return partial(lambda_http_handler, bot)
