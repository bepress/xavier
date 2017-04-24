from xavier.aws.func import LambdaHTTPEvent, build_lambda_router_for_bot
from xavier.bot import Bot
from xavier.http import Response, HTTPError


def build_raw_event(path=u'/abc'):
    return {
        u'body': None,
        u'headers': {
            u'Accept': u'*/*',
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
            u'x-api-key': u'54bUUzjrml4sQWuJiZP51EEQYe45g3j6rAuMjwO5'
        },
        u'httpMethod': u'GET',
        u'isBase64Encoded': False,
        u'path': path,
        u'pathParameters': {u'proxy': u'abc'},
        u'queryStringParameters': {u'a': u'3', u'b': u'2'},
        u'requestContext': {
            u'accountId': u'140099371219',
            u'apiId': u'zih8gs4uja',
            u'httpMethod': u'GET',
            u'identity': {
                u'accessKey': None,
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
                u'userArn': None
            },
            u'requestId': u'7997f0d1-27d4-11e7-b03b-277e30e86ae4',
            u'resourceId': u'dtl0zo',
            u'resourcePath': u'/{proxy+}',
            u'stage': u'prod'
        },
        u'resource': u'/{proxy+}',
        u'stageVariables': None
    }


def test_lambda_http_event_parse():
    raw_event = build_raw_event()

    http_event = LambdaHTTPEvent.from_raw_event(raw_event)

    assert raw_event['headers']['Accept-Encoding'] == http_event.headers['Accept-Encoding']
    assert raw_event['httpMethod'] == http_event.method
    assert raw_event['path'] == http_event.path
    assert raw_event['body'] == http_event.body
    assert raw_event['queryStringParameters']['a'] == http_event.params['a']


def test_build_lambda_router_for_bot():
    bot = Bot()

    @bot.add_route('/test')
    def view_func(*args, **kwargs):
        return Response(200, {
            'important': 'awesome'
        })

    @bot.add_route('/error')
    def error_func(*args, **kwargs):
        raise HTTPError(
            "This is a message",
            'error-slug',
            599
        )

    @bot.add_route('/really-error')
    def really_error_func(*args, **kwargs):
        raise Exception("blah")

    lambda_router = build_lambda_router_for_bot(bot)

    raw_event = build_raw_event('/blah')
    resp = lambda_router(raw_event, {})
    assert resp['statusCode'] == '404'

    raw_event = build_raw_event('/test')
    resp = lambda_router(raw_event, {})
    assert resp['body'] == '{"important": "awesome"}'

    raw_event = build_raw_event('/error')
    resp = lambda_router(raw_event, {})
    assert resp['body'] == '"This is a message"'
    assert resp['statusCode'] == "599"

    raw_event = build_raw_event('/really-error')
    resp = lambda_router(raw_event, {})
    assert resp['body'] == '"Server error"'
    assert resp['statusCode'] == "500"