import json

from xavier.aws.func import LambdaHTTPEvent, build_lambda_router
from xavier.http import Response, HTTPError, Router


def build_raw_event(path=u'/abc', content_type='application/json', body=None, method='GET'):
    return {
        u'body': body,
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
            u'Content-Type': content_type,
            u'x-api-key': u'54bUUzjrml4sQWuJiZP51EEQYe45g3j6rAuMjwO5'
        },
        u'httpMethod': method,
        u'isBase64Encoded': False,
        u'path': path,
        u'pathParameters': {u'proxy': u'abc'},
        u'queryStringParameters': {u'a': u'3', u'b': u'2'},
        u'requestContext': {
            u'accountId': u'140099371219',
            u'apiId': u'zih8gs4uja',
            u'httpMethod': method,
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


def test_parse_body():
    raw_event = build_raw_event(body='{"awesome": "awesome"}')

    http_event = LambdaHTTPEvent.from_raw_event(raw_event)

    assert http_event.parse_body() == {'awesome': 'awesome'}

    raw_event = build_raw_event(content_type='application/x-www-form-urlencoded', body='a=b')

    http_event = LambdaHTTPEvent.from_raw_event(raw_event)

    assert http_event.parse_body() == {'a': ['b']}
    assert http_event.parse_body()['a'] == 'b'
    assert http_event.parse_body().getlist('a') == ['b']

    assert http_event.parsed_body == http_event.parse_body()


def test_build_lambda_router_for_brain():
    router = Router()

    @router.add_route('/test', methods=["GET"])
    def view_func_get(*args, **kwargs):
        return Response(200, {
            'important': 'get'
        })

    @router.add_route('/test/cors', methods=["GET"], cors=True)
    def view_func_cors(*args, **kwargs):
        return Response(200, {
            'important': 'cors'
        })

    @router.add_route('/test/cors', methods=["POST"], cors=True)
    def view_func_cors_error(*args, **kwargs):
        raise HTTPError(
            "This is a message",
            'cors-error',
            599
        )

    @router.add_route('/test', methods=["POST"])
    def view_func_post(*args, **kwargs):
        return Response(200, {
            'important': 'post'
        })

    @router.add_route('/error')
    def error_func(*args, **kwargs):
        raise HTTPError(
            "This is a message",
            'error-slug',
            599
        )

    @router.add_route('/really-error')
    def really_error_func(*args, **kwargs):
        raise Exception("blah")

    lambda_router = build_lambda_router(router)

    raw_event = build_raw_event('/blah')
    resp = lambda_router(raw_event, {})
    assert resp['statusCode'] == '404'

    raw_event = build_raw_event('/test')
    resp = lambda_router(raw_event, {})
    assert resp['body'] == '{"important": "get"}'

    raw_event = build_raw_event('/test', method='POST')
    resp = lambda_router(raw_event, {})
    assert resp['body'] == '{"important": "post"}'

    raw_event = build_raw_event('/test/cors', method='GET')
    resp = lambda_router(raw_event, {})
    assert resp['body'] == '{"important": "cors"}'
    assert "Access-Control-Allow-Origin" in resp['headers']
    assert resp['headers']["Access-Control-Allow-Origin"] == "*"

    raw_event = build_raw_event('/test/cors', method='POST')
    resp = lambda_router(raw_event, {})
    assert json.loads(resp['body']) == {
        "status_code": 599,
        "slug": "cors-error",
        "error": "This is a message"
    }
    assert "Access-Control-Allow-Origin" in resp['headers']
    assert resp['headers']["Access-Control-Allow-Origin"] == "*"

    raw_event = build_raw_event('/error')
    resp = lambda_router(raw_event, {})
    assert json.loads(resp['body']) == {
        "error": "This is a message",
        "status_code": 599,
        "slug": "error-slug"
    }
    assert resp['statusCode'] == "599"

    raw_event = build_raw_event('/really-error')
    resp = lambda_router(raw_event, {})
    assert json.loads(resp['body']) == {
        "slug": "server-error",
        "error": "Server Error",
        "status_code": 500
    }
    assert resp['statusCode'] == "500"
