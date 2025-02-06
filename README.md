# X Auto-Responder

An AWS Lambda function that automatically generates and posts contextually relevant responses to X (formerly Twitter) comments using OpenAI's GPT models.

## Description

This project provides an automated solution for managing social media engagement on X. It monitors comments on specified posts and generates AI-powered responses that maintain consistent tone and messaging while staying within X's character limits.

## Features

- Automated response generation using OpenAI's GPT models
- Smart thread detection and management
- Contextual responses that consider full conversation history
- Customizable response parameters (tone, topic, keywords)
- Character limit enforcement for X platform
- Structured JSON logging
- Error handling and retry mechanisms
- AWS Lambda and SQS integration

## Prerequisites

- Python 3.11+
- AWS Account with Lambda and SQS configured
- X Developer Account with API access
- OpenAI API access

## Environment Variables

```
# X API Credentials
X_CONSUMER_KEY=your_consumer_key
X_CONSUMER_SECRET=your_consumer_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
X_BEARER_TOKEN=your_bearer_token

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4  # or any other supported model
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/x-auto-responder.git
cd x-auto-responder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Build the Lambda deployment package:
```bash
chmod +x build-function-zip.sh
./build-function-zip.sh
```

## SQS Message Format

The Lambda function expects SQS messages in the following format:

```json
{
    "post_id": "string",
    "original_author_id": "string",
    "post": "string",
    "topic": "string",
    "keywords": ["string"],
    "tone": "string",
    "min_char_count": "number"
}
```

## Project Structure

```
├── main.py                 # Lambda handler and main logic
├── x_poster.py            # X posting functionality
├── reply_x_util.py        # Reply fetching and processing
├── prompt_builder.py      # OpenAI prompt construction
├── utils/
│   └── logger_util.py     # Structured logging setup
├── prompts/
│   └── reply_prompt.txt   # OpenAI system prompt template
└── requirements.txt       # Project dependencies
```

## Testing
```bash
pytest tests/test_main.py -v --cov=main --cov-report=term-missing
```

## Deployment

1. Run the build script to create the deployment package:
```bash
./build-function-zip.sh
```

2. Upload the generated `function.zip` to AWS Lambda
3. Configure the Lambda function with the required environment variables
4. Set up an SQS trigger for the Lambda function

## Error Handling

The application includes comprehensive error handling for:
- X API authentication and permission issues
- Rate limiting
- Network failures
- Invalid message formats
- OpenAI API errors

All errors are logged with relevant context using structured JSON logging.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)