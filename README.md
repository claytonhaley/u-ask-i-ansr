# u-ask-i-ansr

This project is aimed at YouTube creators who want to better understand their viewers by allowing creators to converse with a chatbot that has a knowledge base consisting of the comments of one of their videos.

## Getting Started
1. Get started with the [YouTube Data API](https://developers.google.com/youtube/v3/getting-started).

You will need to add the following to a `.env` file once your YouTube Data API account is set up:
```text
DEVELOPER_KEY=your-developer-key
CLIENT_SECRETS_FILE=your-client-secrets-file.json
YOUTUBE_READ_WRITE_SSL_SCOPE=https://www.googleapis.com/auth/youtube.force-ssl
YOUTUBE_API_SERVICE_NAME=youtube
YOUTUBE_API_VERSION=v3
BASE_URL_COMMENTS=https://www.googleapis.com/youtube/v3/commentThreads
BASE_URL_VIDEOS=https://www.googleapis.com/youtube/v3/videos
```
2. Get started with the [OpenAI API](https://platform.openai.com/docs/quickstart)

Add the following to your `.env` file:
```text
OPENAI_API_KEY=your-openai-api-key
```

3. Set up your virtual environment
```shell
python3 -m venv u-ask-i-ansr
source u-ask-i-ansr/bin/activate
```

4. Install dependencies
```shell
pip install requirements.txt
```

5. Get YouTube video ID
`https://www.youtube.com/watch?v={video_id}`
or
`https://youtu.be/{video_id}`

6. Run the program
```shell
python main.py --video_id {video_id}
```