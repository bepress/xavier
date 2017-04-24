from .bot import Bot
from .aws.func import build_lambda_router_for_bot

xavier_bot = Bot()


lambda_http_handler = build_lambda_router_for_bot(xavier_bot)
