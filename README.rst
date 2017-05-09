Xavier: AWS Lambda Bot
======================

Xavier is a bot.


Features
--------

- Inbound Web hooks
- Async/offline functions
- Actions like

Examples
--------

Slack / Command
^^^^^^^^^^^^^^^

Data you get from slack for a /slash command in webhook post

Data from /weather 94070

.. code-block::

  token=gIkuvaNzQIHg97ATvDxqgjtO
  team_id=T0001
  team_domain=example
  channel_id=C2147483705
  channel_name=test
  user_id=U2147483697
  user_name=Steve
  command=/weather
  text=94070
  response_url=https://hooks.slack.com/commands/1234/5678


Amazon SNS
^^^^^^^^^^

SNS Message

.. code-block::

  {
    "Records": [
      {
        "EventVersion": "1.0",
        "EventSubscriptionArn": "eventsubscriptionarn",
        "EventSource": "aws:sns",
        "Sns": {
          "SignatureVersion": "1",
          "Timestamp": "1970-01-01T00:00:00.000Z",
          "Signature": "EXAMPLE",
          "SigningCertUrl": "EXAMPLE",
          "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
          "Message": "Hello from SNS!",
          "MessageAttributes": {
            "Test": {
              "Type": "String",
              "Value": "TestString"
            },
            "TestBinary": {
              "Type": "Binary",
              "Value": "TestBinary"
            }
          },
          "Type": "Notification",
          "UnsubscribeUrl": "EXAMPLE",
          "TopicArn": "topicarn",
          "Subject": "TestInvoke"
        }
      }
    ]
  }


Amazon SES Email

.. code-block::

  {
    "Records":[
      {
        "eventVersion":"1.0",
        "ses":{
          "mail":{
            "commonHeaders":{
              "from":[
                "Jane Doe <janedoe@example.com>"
              ],
              "to":[
                "johndoe@example.com"
              ],
              "returnPath":"janedoe@example.com",
              "messageId":"<0123456789example.com>",
              "date":"Wed, 7 Oct 2015 12:34:56 -0700",
              "subject":"Test Subject"
            },
            "source":"janedoe@example.com",
            "timestamp":"1970-01-01T00:00:00.000Z",
            "destination":[
              "johndoe@example.com"
            ],
            "headers":[
              {
                "name":"Return-Path",
                "value":"<janedoe@example.com>"
              },
              {
                "name":"Received",
                "value":"..."
              },
              {
                "name":"DKIM-Signature",
                "value":"..."
              },
              {
                "name":"MIME-Version",
                "value":"1.0"
              },
              {
                "name":"From",
                "value":"Jane Doe <janedoe@example.com>"
              },
              {
                "name":"Date",
                "value":"Wed, 7 Oct 2015 12:34:56 -0700"
              },
              {
                "name":"Message-ID",
                "value":"<0123456789example.com>"
              },
              {
                "name":"Subject",
                "value":"Test Subject"
              },
              {
                "name":"To",
                "value":"johndoe@example.com"
              },
              {
                "name":"Content-Type",
                "value":"text/plain; charset=UTF-8"
              }
            ],
            "headersTruncated":"false",
            "messageId":"o3vrnil0e2ic28trm7dfhrc2v0clambda4nbp0g1x"
          },
          "receipt":{
            "recipients":[
              "johndoe@example.com"
            ],
            "timestamp":"1970-01-01T00:00:00.000Z",
            "spamVerdict":{
              "status":"PASS"
            },
            "dkimVerdict":{
              "status":"PASS"
            },
            "processingTimeMillis":574,
            "action":{
              "type":"Lambda",
              "invocationType":"Event",
              "functionArn":"functionarn"
            },
            "spfVerdict":{
              "status":"PASS"
            },
            "virusVerdict":{
              "status":"PASS"
            }
          }
        },
        "eventSource":"aws:ses"
      }
    ]
  }


Web Input
^^^^^^^^^

Web input

URL and captured arguments
post body, json
