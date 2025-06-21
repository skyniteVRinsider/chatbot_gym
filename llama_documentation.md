***Llama API Documentation***
Llama API makes it easy to integrate Llama models in your application.
This quickstart guide teaches you the basics of the API and helps you to make your first API request in just a couple of minutes.
Before you begin, make sure you have a Llama API developer account. Sign up at llama.developer.meta.com if you don’t have an account.
You will also need a way to make API calls from your computer. The examples below use curl, but you can use a tool like Postman or Bruno if you prefer.
Create an API key
To use Llama API you need an API key. The API key represents your permission to access the API on behalf of your team, and is needed for all API calls.
In the API platform dashboard, navigate to the API keys tab and click Create API key. Give your key a memorable name, click Create, then copy the key when it is shown.
In production code, you should store the key somewhere secure, but for now keep it on your clipboard; you will use it soon.
Learn more about API keys in the API keys guide.
Try Llama in the Playground
With your API key created, you can now try Llama models in the API playground.
On the API platform dashboard, go to the Chat completion tab under Playground and select your key. Here you can configure system instructions and some model settings, but we can start with a simple question.
In the Ask Llama… box, type a question like “What is a Llama?” and press Enter. The model will quickly respond to your request, showing your question as “User” and the response as the name of the Llama model that’s being used to make the response.
The playground lets you test different user and system prompts and verify the model’s responses. The playground uses Llama API with the API key you created above, so you can move on to making API calls directly.
Your first API call
Now that you have tried using Llama models in the playground, you can start making API calls directly.
You can use an SDK for languages like Python or JavaScript to call the API endpoints, but this simple example uses curl.

Set your API key
Store the API key you created earlier as an environment variable, using the correct method for your operating system.
macOS or Linux:
export LLAMA_API_KEY='your_api_key_here'
Windows:
set LLAMA_API_KEY='your_api_key_here'

Call the API
Use curl to make a simple request to Llama API, asking it to respond to a "Hello, world!" prompt.
Open your terminal and run the following command:
curl -X POST "https://api.llama.com/v1/chat/completions" \
  -H "Authorization: Bearer $LLAMA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Llama-4-Maverick-17B-128E-Instruct-FP8",
    "messages": [
      {
        "role": "system",
        "content": "You are a friendly assistant."
      },
      {
        "role": "user",
        "content": "Hello, world!"
      }
    ]
  }'

Windows users should use %LLAMA_API_KEY% instead of $LLAMA_API_KEY in the command above.
If everything is set up correctly, you should see a JSON response similar to:
{
  "completion_message": {
    "content": {
      "type": "text",
      "text": "Hello! It's nice to meet you. Is there something I can help you with, or would you like to chat?"
    },
    "role": "assistant",
    "stop_reason": "stop",
    "tool_calls": []
  },
  "metrics": [
    {
      "metric": "num_completion_tokens",
      "value": 25,
      "unit": "tokens"
    },
    {
      "metric": "num_prompt_tokens",
      "value": 25,
      "unit": "tokens"
    },
    {
      "metric": "num_total_tokens",
      "value": 50,
      "unit": "tokens"
    }
  ]
}

Understanding the command
Let’s look more closely at this API call:
•Firstly, notice the URL: https://api.llama.com/v1/chat/completions. This is the Chat completion endpoint, which generates text based on a set of prompt messages.
•Next, you will notice that you declared the content type as application/json via the Content-Type header. The API expects to receive a JSON payload as part of the call.
•For authentication, you passed the API key you created and added to the LLAMA_API_KEY environment variable as a bearer token using the Authorization header.
•Finally you passed a JSON payload comprising a model and an array containing messages of type system and user using the -d flag, which adds it to the body of the POST request.
The API has responded with a JSON object containing the assistant's response in the completion_message.content.text field, and a stop reason of ”stop”, which indicates that it has finished replying to your message.

API keys are generated in the API Dashboard at llama.developer.meta.com. Get a key for yourself or your team by following these steps:
Log into API Dashboard and click on the API keys tab.
Click Create API key and give your key a memorable name. Click Create.
Your new key will be shown, and you can copy it somewhere safe.
API keys are formatted as follows:
LLM|607358788850350|nx9.....LJY
Using API keys
With an API key, you can start to make API calls. The API key is sent in the request using the Authorization header. Llama API keys are bearer keys, so send them using the Bearer authorization scheme.
The following example demonstrates how to use API keys with request headers using curl:
curl https://api.llama.com/v1/models \
  -H "Authorization: Bearer LLM|607358788850350|nx9.....LJY"



The Python SDK for Llama API is found here: https://github.com/meta-llama/llama-api-python

Documentation for the Python Llama SDK:
  Llama API Client Python API library

The Llama API Client Python library provides convenient access to the Llama API Client REST API from any Python 3.8+ application. The library includes type definitions for all request params and response fields, and offers both synchronous and asynchronous clients powered by httpx.

Documentation
The REST API documentation can be found on https://llama.developer.meta.com/docs. The full API of this library can be found in api.md.

Installation
pip install llama-api-client
Usage
The full API of this library can be found in api.md.

import os
from llama_api_client import LlamaAPIClient

client = LlamaAPIClient(
    api_key=os.environ.get("LLAMA_API_KEY"),  # This is the default and can be omitted
)

create_chat_completion_response = client.chat.completions.create(
    messages=[
        {
            "content": "string",
            "role": "user",
        }
    ],
    model="model",
)
print(create_chat_completion_response.completion_message)
While you can provide an api_key keyword argument, we recommend using python-dotenv to add LLAMA_API_KEY="My API Key" to your .env file so that your API Key is not stored in source control.

Async usage
Simply import AsyncLlamaAPIClient instead of LlamaAPIClient and use await with each API call:

import os
import asyncio
from llama_api_client import AsyncLlamaAPIClient

client = AsyncLlamaAPIClient(
    api_key=os.environ.get("LLAMA_API_KEY"),  # This is the default and can be omitted
)


async def main() -> None:
    create_chat_completion_response = await client.chat.completions.create(
        messages=[
            {
                "content": "string",
                "role": "user",
            }
        ],
        model="model",
    )
    print(create_chat_completion_response.completion_message)


asyncio.run(main())
Functionality between the synchronous and asynchronous clients is otherwise identical.

Streaming responses
We provide support for streaming responses using Server Side Events (SSE).

from llama_api_client import LlamaAPIClient

client = LlamaAPIClient()

stream = client.chat.completions.create(
    messages=[
        {
            "content": "string",
            "role": "user",
        }
    ],
    model="model",
    stream=True,
)
for chunk in stream:
    print(chunk.event.delta.text, end="", flush=True)
The async client uses the exact same interface.

from llama_api_client import AsyncLlamaAPIClient

client = AsyncLlamaAPIClient()

stream = await client.chat.completions.create(
    messages=[
        {
            "content": "string",
            "role": "user",
        }
    ],
    model="model",
    stream=True,
)
async for chunk in stream:
    print(chunk.event.delta.text, end="", flush=True)
Using types
Nested request parameters are TypedDicts. Responses are Pydantic models which also provide helper methods for things like:

Serializing back into JSON, model.to_json()
Converting to a dictionary, model.to_dict()
Typed requests and responses provide autocomplete and documentation within your editor. If you would like to see type errors in VS Code to help catch bugs earlier, set python.analysis.typeCheckingMode to basic.

Handling errors
When the library is unable to connect to the API (for example, due to network connection problems or a timeout), a subclass of llama_api_client.APIConnectionError is raised.

When the API returns a non-success status code (that is, 4xx or 5xx response), a subclass of llama_api_client.APIStatusError is raised, containing status_code and response properties.

All errors inherit from llama_api_client.APIError.

import llama_api_client
from llama_api_client import LlamaAPIClient

client = LlamaAPIClient()

try:
    client.chat.completions.create(
        messages=[
            {
                "content": "string",
                "role": "user",
            }
        ],
        model="model",
    )
except llama_api_client.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except llama_api_client.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except llama_api_client.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
Error codes are as follows:

Status Code	Error Type
400	BadRequestError
401	AuthenticationError
403	PermissionDeniedError
404	NotFoundError
422	UnprocessableEntityError
429	RateLimitError
>=500	InternalServerError
N/A	APIConnectionError
Retries
Certain errors are automatically retried 2 times by default, with a short exponential backoff. Connection errors (for example, due to a network connectivity problem), 408 Request Timeout, 409 Conflict, 429 Rate Limit, and >=500 Internal errors are all retried by default.

You can use the max_retries option to configure or disable retry settings:

from llama_api_client import LlamaAPIClient

# Configure the default for all requests:
client = LlamaAPIClient(
    # default is 2
    max_retries=0,
)

# Or, configure per-request:
client.with_options(max_retries=5).chat.completions.create(
    messages=[
        {
            "content": "string",
            "role": "user",
        }
    ],
    model="model",
)
Timeouts
By default requests time out after 1 minute. You can configure this with a timeout option, which accepts a float or an httpx.Timeout object:

from llama_api_client import LlamaAPIClient

# Configure the default for all requests:
client = LlamaAPIClient(
    # 20 seconds (default is 1 minute)
    timeout=20.0,
)

# More granular control:
client = LlamaAPIClient(
    timeout=httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
)

# Override per-request:
client.with_options(timeout=5.0).chat.completions.create(
    messages=[
        {
            "content": "string",
            "role": "user",
        }
    ],
    model="model",
)
On timeout, an APITimeoutError is thrown.

Note that requests that time out are retried twice by default.

Advanced
Logging
We use the standard library logging module.

You can enable logging by setting the environment variable LLAMA_API_CLIENT_LOG to info.

$ export LLAMA_API_CLIENT_LOG=info
Or to debug for more verbose logging.

How to tell whether None means null or missing
In an API response, a field may be explicitly null, or missing entirely; in either case, its value is None in this library. You can differentiate the two cases with .model_fields_set:

if response.my_field is None:
  if 'my_field' not in response.model_fields_set:
    print('Got json like {}, without a "my_field" key present at all.')
  else:
    print('Got json like {"my_field": null}.')
Accessing raw response data (e.g. headers)
The "raw" Response object can be accessed by prefixing .with_raw_response. to any HTTP method call, e.g.,

from llama_api_client import LlamaAPIClient

client = LlamaAPIClient()
response = client.chat.completions.with_raw_response.create(
    messages=[{
        "content": "string",
        "role": "user",
    }],
    model="model",
)
print(response.headers.get('X-My-Header'))

completion = response.parse()  # get the object that `chat.completions.create()` would have returned
print(completion.completion_message)
These methods return an APIResponse object.

The async client returns an AsyncAPIResponse with the same structure, the only difference being awaitable methods for reading the response content.

.with_streaming_response
The above interface eagerly reads the full response body when you make the request, which may not always be what you want.

To stream the response body, use .with_streaming_response instead, which requires a context manager and only reads the response body once you call .read(), .text(), .json(), .iter_bytes(), .iter_text(), .iter_lines() or .parse(). In the async client, these are async methods.

with client.chat.completions.with_streaming_response.create(
    messages=[
        {
            "content": "string",
            "role": "user",
        }
    ],
    model="model",
) as response:
    print(response.headers.get("X-My-Header"))

    for line in response.iter_lines():
        print(line)
The context manager is required so that the response will reliably be closed.

Making custom/undocumented requests
This library is typed for convenient access to the documented API.

If you need to access undocumented endpoints, params, or response properties, the library can still be used.

Undocumented endpoints
To make requests to undocumented endpoints, you can make requests using client.get, client.post, and other http verbs. Options on the client will be respected (such as retries) when making this request.

import httpx

response = client.post(
    "/foo",
    cast_to=httpx.Response,
    body={"my_param": True},
)

print(response.headers.get("x-foo"))
Undocumented request params
If you want to explicitly send an extra param, you can do so with the extra_query, extra_body, and extra_headers request options.

Undocumented response properties
To access undocumented response properties, you can access the extra fields like response.unknown_prop. You can also get all the extra fields on the Pydantic model as a dict with response.model_extra.

Configuring the HTTP client
You can directly override the httpx client to customize it for your use case, including:

Support for proxies
Custom transports
Additional advanced functionality
import httpx
from llama_api_client import LlamaAPIClient, DefaultHttpxClient

client = LlamaAPIClient(
    # Or use the `LLAMA_API_CLIENT_BASE_URL` env var
    base_url="http://my.test.server.example.com:8083",
    http_client=DefaultHttpxClient(
        proxy="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
You can also customize the client on a per-request basis by using with_options():

client.with_options(http_client=DefaultHttpxClient(...))
Managing HTTP resources
By default the library closes underlying HTTP connections whenever the client is garbage collected. You can manually close the client using the .close() method if desired, or with a context manager that closes when exiting.

from llama_api_client import LlamaAPIClient

with LlamaAPIClient() as client:
  # make requests here
  ...

# HTTP client is now closed
Versioning
This package generally follows SemVer conventions, though certain backwards-incompatible changes may be released as minor versions:

Changes that only affect static types, without breaking runtime behavior.
Changes to library internals which are technically public but not intended or documented for external use. (Please open a GitHub issue to let us know if you are relying on such internals.)
Changes that we do not expect to impact the vast majority of users in practice.
We take backwards-compatibility seriously and work hard to ensure you can rely on a smooth upgrade experience.

We are keen for your feedback; please open an issue with questions, bugs, or suggestions.

Determining the installed version
If you've upgraded to the latest version but aren't seeing any new features you were expecting then your python environment is likely still using an older version.

You can determine the version that is being used at runtime with:

import llama_api_client
print(llama_api_client.__version__)
Requirements
Python 3.8 or higher.


Example of Python SDK usage:
import os
from llama_api_client import LlamaAPIClient

client = LlamaAPIClient(
    api_key=os.environ.get("LLAMA_API_KEY"), # This is the default and can be omitted
)

completion = client.chat.completions.create(
    model="Llama-4-Maverick-17B-128E-Instruct-FP8",
    messages=[
        {
            "role": "user",
            "content": "What is the moon made of?",
        }
    ],
)
print(completion.completion_message.content.text)