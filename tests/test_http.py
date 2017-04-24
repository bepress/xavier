from xavier.http import Response, HTTPError


def test_response():
    blah = Response(
        500,
        {'blah': 'data'},
        {'Content-Type': 'application/xml'}
    )

    assert blah.render() == '{"blah": "data"}'


def test_http_error():
    xyz = HTTPError("something went wrong", "slug-slug", 499)
    assert xyz.message == "something went wrong"
    assert xyz.slug == "slug-slug"
    assert xyz.status_code == 499
