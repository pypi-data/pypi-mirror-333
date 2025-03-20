# Python Houndify SDK

The Houndify Python SDK allows you to make streaming voice and text queries to the Houndify API from your Python project. The SDK provides two classes **TextHoundClient** and **StreamingHoundClient** for making text and voice queries to the Houndify API. See the *Usage* section below as well as sample scripts in the SDK for more information.

## Sample Scripts

The Python SDK ships with sample scripts that demonstrate how to use various features. Before you use the SDK, you need a valid Client ID and Client Key. You can get these keys from [Houndify.com](https://www.houndify.com) by registering a new client, and enabling domains.

### Sending Text Queries

For an example of a text client take a look at the sample project *sample_text.py*. It lets you pass in a text query and returns a [JSON Response](https://docs.houndify.com/reference/HoundServer).

```bash
./sample_text.py -id <CLIENT ID> -key <CLIENT KEY> '<QUERY>'
```

### Sending Audio Queries

You can send streaming audio to the sample program *sample_wave.py*. There are two `.wav` files you can try. You will get back a [JSON Response](https://docs.houndify.com/reference/HoundServer) based on the contents of the audio.

```bash
./sample_wave.py -id <CLIENT ID> -key <CLIENT KEY> test_audio/what_is_the_weather_like_in_toronto.wav
```

There is another sample program *sample_stdin.py* which will take PCM samples from `stdin`. You can use it with arecord/sox to do real-time decoding from a microphone.

```bash
arecord -t raw -c 1 -r 16000 -f S16_LE | ./sample_stdin.py <CLIENT ID> <CLIENT KEY>
```
```bash
rec -pq | sox - -c 1 -r 16000 -t s16 -L - | ./sample_stdin.py <CLIENT ID> <CLIENT KEY>
```

### Sending either

`query_houndify.py` contains similar functionality to `sample_wave.py` and `sample_text.py`. Additionally, it provides the following options for setting endpoints and making testing easier.

```
--endpoint ENDPOINT, -e ENDPOINT
                      change endpoint the SDK will hit to query Houndify.
                      text-query default: https://api.houndify.com/v1/text
                      audio-file default: https://api.houndify.com/v1/audio
--request-info-file REQUEST_INFO_FILE, -r REQUEST_INFO_FILE
                      Path to JSON file with Houndify request info options.
--expected-transcript EXPECTED_TRANSCRIPT, -x EXPECTED_TRANSCRIPT
                      The expected transcript from the audio file. If this
                      argument is provided the script will compare it to the
                      transcript from the Houndify. On failure, the
                      script will return 1
--silent, -s          The script will not print the server's JSON response
```

* `endpoint` Can be used on self hosted solutions
* `expected-transcript` is useful when testing Houndify capabilities
* `silent` is often used with `expected-transcript` to make the output less verbose


## Usage

The main module in the SDK is *houndify.py*, which contains three classes:

* **TextHoundClient**
* **StreamingHoundClient**
* **HoundListener**


### Text Queries: TextHoundClient

This class is used for making text queries to the Houndify API. The constructor expects:

* `clientID`: This is the Client ID of your Houndify app.
* `clientKey`: This is the Client Key of your Houndify app.
* `userID`: This parameter should be unique for every user that uses your app.
* `requestInfo`: (optional) This should be a dictionary that will make the JSON response more accurate. See [RequestInfo](https://docs.houndify.com/reference/RequestInfo) for supported keys.
* `proxyHost`: (optional) Pass the host for HTTP Connect Tunnelling to make queries through proxy.
* `proxyPort`: (optional) Port for HTTP Connect Tunnelling.
* `proxyHeaders`: (optional) Extra headers for HTTP Connect Tunnelling.
* `endpoint`: (optional) Change the backend endpoint the SDK will hit for queries

```python
import houndify

clientId = "YOUR_CLIENT_ID"
clientKey = "YOUR_CLIENT_KEY"
userId = "test_user"
requestInfo = {
  "Latitude": 37.388309,
  "Longitude": -121.973968
}

client = houndify.TextHoundClient(clientId, clientKey, userId, requestInfo)
```

The method that is used for sending a text query is **TextHoundClient.query(query_string)** and it returns a dictionary with [response JSON](https://docs.houndify.com/reference/HoundServer) in it.

```python
response = client.query("What is the weather like today?")
```

You can reset [RequestInfo fields](https://docs.houndify.com/reference/RequestInfo) via the **TextHoundClient.setHoundRequestInfo(key, value)** and **TextHoundClient.removeHoundRequestInfo(key)** methods.

```python
client.setHoundRequestInfo("City", "Santa Clara")
client.removeHoundRequestInfo("City")
```


### Audio Queries: StreamingHoundClient

In order to send an audio query to the Houndify API you need to initialize a **StreamingHoundClient**. The constructor expects the following arguments:

* `clientID`: This is the Client ID of your Houndify app.
* `clientKey`: This is the Client Key of your Houndify app.
* `userID`: This parameter should be unique for every user that uses your app.
* `requestInfo`: (optional) This should be a dictionary that will make the JSON response more accurate. See [RequestInfo](https://docs.houndify.com/reference/RequestInfo) for supported keys.
* `sampleRate`: (optional) The sample rate of the audio, either 8000 or 16000 Hz. It will default to 16000 if not supplied.
* `enableVAD`: (optional) Boolean specifying whether you want to support Voice Activity Detection. If True *fill()* method will return True and ignore any more audio bytes after server detects silence. The default value is False.
* `useSpeex`: (optional) This flag enables Speex conversion of audio. The default value is False. See *Speex Compression* section below for instruction on setting Speex up.
* `proxyHost`: (optional) Pass host for HTTP Connect Tunnelling to make queries through proxy.
* `proxyPort`: (optional) Port for HTTP Connect Tunnelling.
* `proxyHeaders`: (optional) Extra headers for HTTP Connect Tunnelling.
* `endpoint`: (optional) Change the backend endpoint the SDK will hit for queries

```python
import houndify

clientId = "YOUR_CLIENT_ID"
clientKey = "YOUR_CLIENT_KEY"
userId = "test_user"
client = houndify.StreamingHoundClient(clientId, clientKey, userId, sampleRate=8000)
```

Additionally you'll need to extend and create **HoundListener**:

```python
class MyListener(houndify.HoundListener):
    def onPartialTranscript(self, transcript):
      """
      onPartialTranscript is fired when the server has sent a partial transcript
      in live transcription mode.  "transcript" is a string with the partial transcript.
      """
    def onPartialTranscriptRaw(self, response):
        """
        onPartialTranscriptRaw is fired when the server has a partial transcript.
        This method gives access to the full Houndify response.
        """
    def onFinalPartialTranscript(self, transcript):
      """
      onFinalPartialTranscript is fired once the server has identified one or more
      complete sentences that are guaranteed not to change in the future.
      These sentences won't be included in partial transcripts going forward,
      the client needs to accumulate them in order to compile the full transcript.
      Only occurs in live transcription mode.
      """
    def onPartialTranscriptProperties(self, transcript, props):
      """
      onPartialTranscriptProperties is fired when the server has a partial transcript
      and detailed information is provided by the server (usually in live transcription
      mode). "props" is a HoundTranscriptProperties JSON object (as a Python dict)
      containing the "Tokens" array and optional extra fields such as "TopicIdentification"
      or "EntityDetection".
      """
    def onFinalPartialTranscriptProperties(self, transcript, props):
      """
      onFinalPartialTranscriptProperties is fired once the server has identified one
      or more complete sentences that are guaranteed not to change in the future.
      These sentences won't be included in partial transcripts going forward,
      the client needs to accumulate them in order to compile the full transcript.
      "props" is a HoundTranscriptProperties JSON object (as a Python dict)
      containing the "Tokens" array and optional extra fields such as "TopicIdentification"
      or "EntityDetection". Only occurs in live transcription mode.
      """
    def onFinalResponse(self, response):
      """
      onFinalResponse is fired when the server has completed processing the query
      and has a response.  "response" is the JSON object (as a Python dict) which
      the server sends back.
      """
    def onError(self, err):
      """
      onError is fired if there is an error interacting with the server.  It contains
      the parsed JSON from the server.
      """

```


### Audio Queries: Code Example

Finally, you should start a request with passing an instance of your Listener to **StreamingHoundClient.start(listener, isSpeexFile=False)**, pipe the audio through **StreamingHoundClient.fill(samples)** and call **StreamingHoundClient.finish()** when the request is done.

*Note: StreamingHoundClient supports 8/16 kHz mono 16-bit little-endian PCM samples.*

```python
class MyListener(houndify.HoundListener):
  def onPartialTranscript(self, transcript):
    print("Partial transcript: " + transcript)

  def onFinalResponse(self, response):
    print("Final response: " + str(response))

  def onError(self, err):
    print("Error " + str(err))


client.start(MyListener())
# 'samples' is the list of mono 16-bit little-endian PCM samples
client.fill(samples)
result = client.finish() # result is either final response or error
```

There are four more useful methods in **StreamingHoundClient** for resetting sample rate, location and request info fields.

```python
client.setSampleRate(8000) #or 16000
client.setLocation(37.388309, -121.973968)
client.setHoundRequestInfo("City", "Santa Clara")
client.removeHoundRequestInfo("City")
```


### Conversation State

Houndify domains can use context to enable a conversational user interaction. For example, users can say "show me coffee shops near me", "which ones have wifi?", "sort by rating", "navigate to the first one". Both **TextHoundClient** and **StreamingHoundClient** have **setConversationState(state)** method that you can use to set [Conversation State](https://docs.houndify.com/reference/CommandResult#field_ConversationState) extracted from a previous response.

```python
client = houndify.TextHoundClient(clientId, clientKey, userId)

response = client.query("What is the weather like in Toronto?")

conversationState = response["AllResults"][0]["ConversationState"]
client.setConversationState(conversationState)

response = client.query("What about Santa Clara?")
```



## Speex Compression

You can use *pySHSpeex* module included in the SDK for sending compressed audio. To build and install *pySHSpeex* run following commands:

```bash
# setup script requires Python development headers:
# sudo apt-get install python-dev
# yum install python-devel

cd pySHSpeex
sudo python setup.py install
```
*Note: this will install pySHSpeex system-wide although it is possible to install it per-user following standard Python module installation procedure.*

You have to pass the additional **useSpeex=True** flag to the StreamingHoundClient in order to enable compression.

```python
import houndify

clientId = "YOUR_CLIENT_ID"
clientKey = "YOUR_CLIENT_KEY"
userId = "test_user"
client = houndify.StreamingHoundClient(clientId, clientKey, userId, useSpeex=True)
```
