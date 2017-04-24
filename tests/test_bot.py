from xavier.bot import Bot


def test_bot_name():
    assert Bot(name='test-bot').name == 'test-bot'


def test_add_route():
    bot = Bot()

    @bot.add_route('/test', extra='blah')
    def view_func(*args, **kwargs):
        return ''

    r = bot.find_route('/test')

    assert r['extra'] == 'blah'
