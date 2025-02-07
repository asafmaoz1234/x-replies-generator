import json
from unittest.mock import Mock, patch, mock_open

import openai
import pytest

from main import lambda_handler, process_reply_thread, load_prompt_template


class TestMainModule:
    @pytest.fixture(autouse=True)
    def setup_env(self):
        """Setup environment variables for each test"""
        self.test_env = {
            'OPENAI_API_KEY': 'test_key',
            'X_CONSUMER_KEY': 'test_consumer_key',
            'X_CONSUMER_SECRET': 'test_consumer_secret',
            'X_ACCESS_TOKEN': 'test_access_token',
            'X_ACCESS_TOKEN_SECRET': 'test_access_token_secret'
        }
        with patch.dict('os.environ', self.test_env):
            openai.api_key = self.test_env['OPENAI_API_KEY']
            yield

    @pytest.fixture
    def context(self):
        context = Mock()
        context.aws_request_id = "test-request-id"
        return context

    @pytest.fixture
    def event(self):
        return {
            "Records": [{
                "body": json.dumps({
                    "post_id": "123",
                    "original_author_id": "456",
                    "post": "Original post",
                    "topic": "tech",
                    "keywords": ["ai", "ml"],
                    "tone": "professional"
                })
            }]
        }

    @pytest.fixture
    def thread(self):
        return [{
            "id": "789",
            "text": "Test reply",
            "author_id": "101112"
        }]

    @pytest.fixture
    def openai_response(self):
        response = Mock()
        response.choices = [Mock()]
        response.choices[0].message.content = "AI generated response"
        return response

    def test_load_prompt_template_success(self):
        mock_template = "Test template {topic}"
        with patch("builtins.open", mock_open(read_data=mock_template)):
            result = load_prompt_template()
            assert result == mock_template

    def test_load_prompt_template_fallback(self):
        with patch("builtins.open", side_effect=Exception("File not found")):
            result = load_prompt_template()
            assert "You are a social media manager" in result

    @patch("tweepy.Client")
    @patch("openai.chat.completions.create")
    def test_process_reply_thread_success(self, mock_openai, mock_tweepy, thread, openai_response):
        mock_openai.return_value = openai_response
        mock_tweepy.return_value.create_tweet.return_value.data = {"id": "new_post_id"}

        message = {
            "post": "Original post",
            "topic": "tech",
            "keywords": ["ai", "ml"],
            "tone": "professional"
        }

        result = process_reply_thread(
            mock_tweepy,
            message,
            thread,
            "gpt-4",
            "test template"
        )

        assert result["reply_id"] == "789"
        assert "content" in result
        assert "response_id" in result

    @patch("tweepy.Client")
    @patch("openai.chat.completions.create")
    def test_process_reply_thread_error(self, mock_openai, mock_tweepy, thread):
        mock_openai.side_effect = Exception("API Error")

        with pytest.raises(Exception):
            process_reply_thread(
                mock_tweepy,
                {},
                thread,
                "gpt-4",
                "test template"
            )

    @patch("reply_x_util.fetch_replies_to_post")
    def test_lambda_handler_no_replies(self, mock_fetch_replies, event, context):
        mock_fetch_replies.return_value = []

        result = lambda_handler(event, context)

        assert result["statusCode"] == 200
        assert "No replies requiring response" in result["body"]

    @patch("reply_x_util.fetch_replies_to_post")
    @patch("tweepy.Client")
    @patch("openai.chat.completions.create")
    def test_lambda_handler_success(self, mock_openai, mock_tweepy, mock_fetch_replies,
                                    event, context, thread, openai_response):
        mock_fetch_replies.return_value = [thread]
        mock_openai.return_value = openai_response
        mock_tweepy.return_value.create_tweet.return_value.data = {"id": "new_post_id"}

        result = lambda_handler(event, context)

        assert result["statusCode"] == 200
        assert "Successfully processed reply threads" in result["body"]

    @patch("reply_x_util.fetch_replies_to_post")
    def test_lambda_handler_error(self, mock_fetch_replies, event, context):
        mock_fetch_replies.side_effect = Exception("Test error")

        result = lambda_handler(event, context)

        assert result["statusCode"] == 500
        assert "Test error" in result["body"]

    @patch("reply_x_util.fetch_replies_to_post")
    @patch("tweepy.Client")
    @patch("openai.chat.completions.create")
    def test_lambda_handler_partial_success(self, mock_openai, mock_tweepy, mock_fetch_replies,
                                            event, context, thread):
        mock_fetch_replies.return_value = [thread, thread]
        mock_openai.side_effect = [Exception("API Error"), Mock(choices=[Mock(message=Mock(content="Success"))])]
        mock_tweepy.return_value.create_tweet.return_value.data = {"id": "new_post_id"}

        result = lambda_handler(event, context)

        assert result["statusCode"] == 207
        body = json.loads(result["body"])
        assert len(body["errors"]) > 0
        assert len(body["processed_replies"]) > 0

    def test_lambda_handler_invalid_event(self, context):
        invalid_event = {"Records": [{"body": "invalid json"}]}
        result = lambda_handler(invalid_event, context)
        assert result["statusCode"] == 500