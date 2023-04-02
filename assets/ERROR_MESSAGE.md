# ERROR MESSAGE

##### Reply 的字數不能太長
```shell
Error occurred: LineBotApiError: status_code=400, request_id=06f06056-7d52-4117-99c7-def1df68e570, error_response={"details": [{"message": "must not be more than 3 items", "property": "template/columns/0/actions"}], "message": "A message (messages[1])\u00a0in the request body is invalid"}, headers={'Server': 'legy', 'Content-Type': 'application/json', 'x-content-type-options': 'nosniff', 'x-frame-options': 'DENY', 'x-line-request-id': '06f06056-7d52-4117-99c7-def1df68e570', 'x-xss-protection': '1; mode=block', 'Content-Length': '165', 'Expires': 'Sat, 01 Apr 2023 15:48:37 GMT', 'Cache-Control': 'max-age=0, no-cache, no-store', 'Pragma': 'no-cache', 'Date': 'Sat, 01 Apr 2023 15:48:37 GMT', 'Connection': 'close'}
[2023-04-01 23:48:37,569] ERROR in app: Exception on /callback [POST]
Traceback (most recent call last):
  File "/Users/linchunho/Developer/leftovers-bot/run.py", line 396, in handle_text_message
    line_bot_api.reply_message(
  File "/Users/linchunho/Developer/leftovers-bot/venv/lib/python3.9/site-packages/linebot/api.py", line 116, in reply_message
    self._post(
  File "/Users/linchunho/Developer/leftovers-bot/venv/lib/python3.9/site-packages/linebot/api.py", line 2033, in _post
    self.__check_error(response)
  File "/Users/linchunho/Developer/leftovers-bot/venv/lib/python3.9/site-packages/linebot/api.py", line 2069, in __check_error
    raise LineBotApiError(
linebot.exceptions.LineBotApiError: LineBotApiError: status_code=400, request_id=06f06056-7d52-4117-99c7-def1df68e570, error_response={"details": [{"message": "must not be more than 3 items", "property": "template/columns/0/actions"}], "message": "A message (messages[1])\u00a0in the request body is invalid"}, headers={'Server': 'legy', 'Content-Type': 'application/json', 'x-content-type-options': 'nosniff', 'x-frame-options': 'DENY', 'x-line-request-id': '06f06056-7d52-4117-99c7-def1df68e570', 'x-xss-protection': '1; mode=block', 'Content-Length': '165', 'Expires': 'Sat, 01 Apr 2023 15:48:37 GMT', 'Cache-Control': 'max-age=0, no-cache, no-store', 'Pragma': 'no-cache', 'Date': 'Sat, 01 Apr 2023 15:48:37 GMT', 'Connection': 'close'}

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/linchunho/Developer/leftovers-bot/venv/lib/python3.9/site-packages/flask/app.py", line 2528, in wsgi_app
    response = self.full_dispatch_request()
  File "/Users/linchunho/Developer/leftovers-bot/venv/lib/python3.9/site-packages/flask/app.py", line 1825, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/Users/linchunho/Developer/leftovers-bot/venv/lib/python3.9/site-packages/flask/app.py", line 1823, in full_dispatch_request
    rv = self.dispatch_request()
  File "/Users/linchunho/Developer/leftovers-bot/venv/lib/python3.9/site-packages/flask/app.py", line 1799, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
  File "/Users/linchunho/Developer/leftovers-bot/run.py", line 102, in callback
    handler.handle(body, signature)
  File "/Users/linchunho/Developer/leftovers-bot/venv/lib/python3.9/site-packages/linebot/webhook.py", line 263, in handle
    self.__invoke_func(func, event, payload)
  File "/Users/linchunho/Developer/leftovers-bot/venv/lib/python3.9/site-packages/linebot/webhook.py", line 275, in __invoke_func
    func(event)
  File "/Users/linchunho/Developer/leftovers-bot/run.py", line 415, in handle_text_message
    line_bot_api.reply_message(
  File "/Users/linchunho/Developer/leftovers-bot/venv/lib/python3.9/site-packages/linebot/api.py", line 116, in reply_message
    self._post(
  File "/Users/linchunho/Developer/leftovers-bot/venv/lib/python3.9/site-packages/linebot/api.py", line 2033, in _post
    self.__check_error(response)
  File "/Users/linchunho/Developer/leftovers-bot/venv/lib/python3.9/site-packages/linebot/api.py", line 2069, in __check_error
    raise LineBotApiError(
linebot.exceptions.LineBotApiError: LineBotApiError: status_code=400, request_id=f3a62d1e-fe44-4848-995f-88013d707d95, error_response={"details": [], "message": "Invalid reply token"}, headers={'Server': 'legy', 'Content-Type': 'application/json', 'x-content-type-options': 'nosniff', 'x-frame-options': 'DENY', 'x-line-request-id': 'f3a62d1e-fe44-4848-995f-88013d707d95', 'x-xss-protection': '1; mode=block', 'Content-Length': '33', 'Expires': 'Sat, 01 Apr 2023 15:48:37 GMT', 'Cache-Control': 'max-age=0, no-cache, no-store', 'Pragma': 'no-cache', 'Date': 'Sat, 01 Apr 2023 15:48:37 GMT', 'Connection': 'close'}
127.0.0.1 - - [01/Apr/2023 23:48:37] "POST /callback HTTP/1.1" 500 -
```