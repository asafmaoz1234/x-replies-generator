import pytest
from reply_x_util import filter_threads_with_op_last_reply


class TestThreadFilter:
    @pytest.fixture
    def threads_needed_reply_no_conversation(self):
        return [
            {
                "conversation_id": "18875814642014742539",
                "id": "18877408015951544469",
                "edit_history_tweet_ids": [
                    "18877408015951544469"
                ],
                "created_at": "2025-02-07T05:50:54.000Z",
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "18875814642014742539"
                    }
                ],
                "author_id": "16088142869",
                "text": "@ai_daily97375 interesting, can you give some more examples?",
                "in_reply_to_user_id": "1884611255320674304"
            }
        ]

    @pytest.fixture
    def threads_needed_reply(self):
        return [
            {
                "conversation_id": "1887581464201474253",
                "id": "1887778753012461612",
                "edit_history_tweet_ids": [
                    "1887778753012461612"
                ],
                "created_at": "2025-02-07T08:21:42.000Z",
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "1887740801595154446"
                    }
                ],
                "author_id": "1884611255320674304",
                "text": "@N0obNo0b Adulting is like trying to navigate the latest TikTok trends—everyone's doing it, but no one really knows how. Remember when we thought we’d have it figured out by 30? Now I’m just hoping my plants don’t die. What’s your latest “I can’t believe I’m an adult” moment?",
                "in_reply_to_user_id": "1608814286"
            },
            {
                "conversation_id": "1887581464201474253",
                "id": "1887773834494816657",
                "edit_history_tweet_ids": [
                    "1887773834494816657"
                ],
                "created_at": "2025-02-07T08:02:09.000Z",
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "1887740801595154446"
                    }
                ],
                "author_id": "1884611255320674304",
                "text": "@N0obNo0b Adulting is basically a never-ending game of \"how do I fix this?\" Remember when we thought the hardest part of life would be deciding on college majors? Now it’s deciphering health insurance jargon! What’s your wildest “adulting fails” moment? Let’s share the chaos!",
                "in_reply_to_user_id": "1608814286"
            },
            {
                "conversation_id": "1887581464201474253",
                "id": "1887744197127454757",
                "edit_history_tweet_ids": [
                    "1887744197127454757"
                ],
                "created_at": "2025-02-07T06:04:23.000Z",
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "1887740801595154446"
                    }
                ],
                "author_id": "1884611255320674304",
                "text": "@N0obNo0b Adulting: the real-life horror movie no one signed up for! Just last week, I Googled “how to fix a broken heart” after a dinner disaster. Turns out, burnt pasta isn’t the best date night. What’s the craziest thing you’ve Googled in a panic? Let's share our adulting fails!",
                "in_reply_to_user_id": "1608814286"
            },
            {
                "conversation_id": "1887581464201474253",
                "id": "1887740801595154446",
                "edit_history_tweet_ids": [
                    "1887740801595154446"
                ],
                "created_at": "2025-02-07T05:50:54.000Z",
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "1887581464201474253"
                    }
                ],
                "author_id": "1608814286",
                "text": "@ai_daily97375 interesting, can you give some more examples?",
                "in_reply_to_user_id": "1884611255320674304"
            },
            {
                "conversation_id": "18875814642014742539",
                "id": "18877408015951544469",
                "edit_history_tweet_ids": [
                    "18877408015951544469"
                ],
                "created_at": "2025-02-07T05:50:54.000Z",
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "18875814642014742539"
                    }
                ],
                "author_id": "16088142869",
                "text": "@ai_daily97375 interesting, can you give some more examples?",
                "in_reply_to_user_id": "1884611255320674304"
            }
        ]

    @pytest.fixture
    def threads_needed_reply_conversation(self):
        return [
            {
                "conversation_id": "1887581464201474253",
                "id": "18877408015951544469",
                "edit_history_tweet_ids": [
                    "18877408015951544469"
                ],
                "created_at": "2025-02-07T05:50:54.000Z",
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "1887778753012461612"
                    }
                ],
                "author_id": "1608814286",
                "text": "@ai_daily97375 not enough - interesting, can you give some more examples?",
                "in_reply_to_user_id": "1884611255320674304"
            },
            {
                "conversation_id": "1887581464201474253",
                "id": "1887778753012461612",
                "edit_history_tweet_ids": [
                    "1887778753012461612"
                ],
                "created_at": "2025-02-07T08:21:42.000Z",
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "1887740801595154446"
                    }
                ],
                "author_id": "1884611255320674304",
                "text": "@N0obNo0b Adulting is like trying to navigate the latest TikTok trends—everyone's doing it, but no one really knows how. Remember when we thought we’d have it figured out by 30? Now I’m just hoping my plants don’t die. What’s your latest “I can’t believe I’m an adult” moment?",
                "in_reply_to_user_id": "1608814286"
            },
            {
                "conversation_id": "1887581464201474253",
                "id": "1887773834494816657",
                "edit_history_tweet_ids": [
                    "1887773834494816657"
                ],
                "created_at": "2025-02-07T08:02:09.000Z",
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "1887740801595154446"
                    }
                ],
                "author_id": "1884611255320674304",
                "text": "@N0obNo0b Adulting is basically a never-ending game of \"how do I fix this?\" Remember when we thought the hardest part of life would be deciding on college majors? Now it’s deciphering health insurance jargon! What’s your wildest “adulting fails” moment? Let’s share the chaos!",
                "in_reply_to_user_id": "1608814286"
            },
            {
                "conversation_id": "1887581464201474253",
                "id": "1887744197127454757",
                "edit_history_tweet_ids": [
                    "1887744197127454757"
                ],
                "created_at": "2025-02-07T06:04:23.000Z",
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "1887740801595154446"
                    }
                ],
                "author_id": "1884611255320674304",
                "text": "@N0obNo0b Adulting: the real-life horror movie no one signed up for! Just last week, I Googled “how to fix a broken heart” after a dinner disaster. Turns out, burnt pasta isn’t the best date night. What’s the craziest thing you’ve Googled in a panic? Let's share our adulting fails!",
                "in_reply_to_user_id": "1608814286"
            },
            {
                "conversation_id": "1887581464201474253",
                "id": "1887740801595154446",
                "edit_history_tweet_ids": [
                    "1887740801595154446"
                ],
                "created_at": "2025-02-07T05:50:54.000Z",
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "1887581464201474253"
                    }
                ],
                "author_id": "16088142869",
                "text": "@ai_daily97375 interesting, can you give some more examples?",
                "in_reply_to_user_id": "1884611255320674304"
            }
        ]

    @pytest.fixture
    def threads_no_reply(self):
        return [
            {
                "conversation_id": "1887581464201474253",
                "id": "1887778753012461612",
                "edit_history_tweet_ids": [
                    "1887778753012461612"
                ],
                "created_at": "2025-02-07T08:21:42.000Z",
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "1887740801595154446"
                    }
                ],
                "author_id": "1884611255320674304",
                "text": "@N0obNo0b Adulting is like trying to navigate the latest TikTok trends—everyone's doing it, but no one really knows how. Remember when we thought we’d have it figured out by 30? Now I’m just hoping my plants don’t die. What’s your latest “I can’t believe I’m an adult” moment?",
                "in_reply_to_user_id": "1608814286"
            },
            {
                "conversation_id": "1887581464201474253",
                "id": "1887773834494816657",
                "edit_history_tweet_ids": [
                    "1887773834494816657"
                ],
                "created_at": "2025-02-07T08:02:09.000Z",
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "1887740801595154446"
                    }
                ],
                "author_id": "1884611255320674304",
                "text": "@N0obNo0b Adulting is basically a never-ending game of \"how do I fix this?\" Remember when we thought the hardest part of life would be deciding on college majors? Now it’s deciphering health insurance jargon! What’s your wildest “adulting fails” moment? Let’s share the chaos!",
                "in_reply_to_user_id": "1608814286"
            },
            {
                "conversation_id": "1887581464201474253",
                "id": "1887744197127454757",
                "edit_history_tweet_ids": [
                    "1887744197127454757"
                ],
                "created_at": "2025-02-07T06:04:23.000Z",
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "1887740801595154446"
                    }
                ],
                "author_id": "1884611255320674304",
                "text": "@N0obNo0b Adulting: the real-life horror movie no one signed up for! Just last week, I Googled “how to fix a broken heart” after a dinner disaster. Turns out, burnt pasta isn’t the best date night. What’s the craziest thing you’ve Googled in a panic? Let's share our adulting fails!",
                "in_reply_to_user_id": "1608814286"
            },
            {
                "conversation_id": "1887581464201474253",
                "id": "1887740801595154446",
                "edit_history_tweet_ids": [
                    "1887740801595154446"
                ],
                "created_at": "2025-02-07T05:50:54.000Z",
                "referenced_tweets": [
                    {
                        "type": "replied_to",
                        "id": "1887581464201474253"
                    }
                ],
                "author_id": "1608814286",
                "text": "@ai_daily97375 interesting, can you give some more examples?",
                "in_reply_to_user_id": "1884611255320674304"
            }
        ]

    def test_op_last_reply_no_replies_needed(self, threads_no_reply):
        original_author_id = "1884611255320674304"
        reply_map, tweets_to_reply = filter_threads_with_op_last_reply(threads_no_reply, original_author_id)
        assert len(tweets_to_reply) == 0

    def test_other_last_reply_reply_needed(self, threads_needed_reply):
        original_author_id = "1884611255320674304"
        reply_map, tweets_to_reply = filter_threads_with_op_last_reply(threads_needed_reply, original_author_id)
        assert len(tweets_to_reply) == 1
        assert tweets_to_reply[0]["id"] == "18877408015951544469"

    def test_other_last_reply_no_conversation(self, threads_needed_reply_no_conversation):
        original_author_id = "1884611255320674304"
        reply_map, tweets_to_reply = filter_threads_with_op_last_reply(threads_needed_reply_no_conversation, original_author_id)
        assert len(tweets_to_reply) == 1
        assert tweets_to_reply[0]["id"] == "18877408015951544469"
        assert len(reply_map) == 0

    def test_other_last_reply_reply_needed_conversation(self, threads_needed_reply_conversation):
        original_author_id = "1884611255320674304"
        reply_map, tweets_to_reply = filter_threads_with_op_last_reply(threads_needed_reply_conversation, original_author_id)
        assert len(tweets_to_reply) == 1
        assert tweets_to_reply[0]["id"] == "18877408015951544469"
        assert len(reply_map[tweets_to_reply[0]["id"]][0]) == 4
        assert reply_map[tweets_to_reply[0]["id"]][0][0]["id"] == '1887778753012461612'

    def test_empty_threads(self):
        reply_map, tweets_to_reply = filter_threads_with_op_last_reply([], "any_id")
        assert len(tweets_to_reply) == 0

    def test_no_referenced_tweets(self):
        threads = [{"id": "1", "author_id": "123"}]
        reply_map, tweets_to_reply = filter_threads_with_op_last_reply(threads, "123")
        assert len(tweets_to_reply) == 0
