import os
import requests
from typing import List, Dict
from utils.logger_util import logger


def filter_threads_with_op_last_reply(threads: List[Dict], original_author_id: str) -> List[Dict]:
    logger.info("Input threads:", extra={'extra_data': {'threads': threads}})
    reply_threads = {}

    reply_map = {}
    ai_tweet_responses = []
    non_ai_tweets = []

    # Map responses to parent tweets and collect AI tweets
    for tweet in threads:
        if tweet['author_id'] == original_author_id:
            if 'referenced_tweets' in tweet:
                for ref in tweet['referenced_tweets']:
                    if ref['type'] == 'replied_to' and ref['id'] not in ai_tweet_responses:
                        ai_tweet_responses.append(ref['id'])
            continue
        non_ai_tweets.append(tweet)

    # Find nonAi tweets without responses
    others_last_replies = []
    for non_ai_tweet in non_ai_tweets:
        if non_ai_tweet['id'] not in ai_tweet_responses:
            others_last_replies.append(non_ai_tweet)

    # Debug logging
    logger.info("All threads found:")
    for thread in reply_threads.values():
        for reply in thread:
            logger.info("all replies to thread: ", extra={'extra_data': {
                'thread_id': reply['id'],
                'author_id': reply['author_id'],
                'text': reply['text']
            }})

    logger.info("Threads requiring response:")
    for tweet in others_last_replies:
        logger.info("requiring response: ", extra={'extra_data': {
            'thread_id': tweet['id'],
            'author_id': tweet['author_id'],
            'text': tweet['text']
        }})

    return others_last_replies


def fetch_replies_to_post(post_id: str, original_author_id: str) -> List[Dict]:
    """
    Fetches recent replies to a post and identifies threads where someone other
    than the original poster was the last to reply.

    Args:
        post_id: The ID of the post to fetch replies for
        original_author_id: The ID of the original post's author

    Returns:
        List of reply threads where someone else was last to reply
    """
    try:
        logger.info('Fetching replies',
                    extra={'extra_data': {
                        'post_id': post_id,
                        'original_author_id': original_author_id
                    }})

        headers = {"Authorization": f"Bearer {os.environ['X_BEARER_TOKEN']}"}

        # Fetch replies
        search_url = "https://api.twitter.com/2/tweets/search/recent"
        params = {
            "query": f"conversation_id:{post_id}",
            "tweet.fields": "author_id,created_at,in_reply_to_user_id,conversation_id,referenced_tweets",
            "max_results": 100,
            "user.fields": "username"
        }

        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code != 200:
            logger.error('Failed to fetch replies',
                         extra={'extra_data': {
                             'status_code': response.status_code,
                             'response': response.text
                         }})
            raise Exception(f'Failed to fetch replies for post {post_id}, exception: {response.text}')

        result = response.json()

        if 'data' not in result:
            logger.info('No replies found', extra={'extra_data': {'post_id': post_id}})
            return []

        return filter_threads_with_op_last_reply(result['data'], original_author_id)
    except Exception as e:
        logger.error('Error processing replies',
                     extra={'extra_data': {
                         'post_id': post_id,
                         'error': str(e)
                     }},
                     exc_info=True)
        raise
