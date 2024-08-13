import subprocess
import json
import shlex
import os
import urllib
from urllib.parse import quote

bookmarks_command_first_line = "curl --compressed 'https://x.com/i/api/graphql/xLjCVTqYWz8CGSprLU349w/Bookmarks?variables=%7B%22count%22%3A20%2C%22includePromotedContent%22%3Atrue%7D'"

while True: 

    bookmarks_command = bookmarks_command_first_line + """
        -X POST \
        -H 'Accept: */*' \
        -H 'Accept-Encoding: gzip, deflate, br, zstd' \
        -H 'Accept-Language: en-US,en;q=0.5' \
        -H 'Authorization: Bearer ' \
        -H 'Connection: keep-alive' \
        -H 'Content-Type: application/json' \
        -H 'Cookie: ' \
        -H 'Referer: https://x.com/i/bookmarks' \
        -H 'Sec-Fetch-Dest: empty' \
        -H 'Sec-Fetch-Mode: cors' \
        -H 'Sec-Fetch-Site: same-origin' \
        -H 'TE: trailers' \
        -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0' \
        -H 'x-client-transaction-id: ' \
        -H 'X-Client-UUID: ' \
        -H 'x-csrf-token: ' \
        -H 'x-twitter-active-user: yes' \
        -H 'x-twitter-auth-type: OAuth2Session' \
        -H 'x-twitter-client-language: en' \
        -d '{"features":{"graphql_timeline_v2_bookmark_timeline":true,"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_timeline_navigation_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"communities_web_enable_tweet_community_results_fetch":true,"c9s_tweet_anatomy_moderator_badge_enabled":true,"articles_preview_enabled":true,"tweetypie_unmention_optimization_enabled":true,"responsive_web_edit_tweet_api_enabled":true,"graphql_is_translatable_rweb_tweet_is_translatable_enabled":true,"view_counts_everywhere_api_enabled":true,"longform_notetweets_consumption_enabled":true,"responsive_web_twitter_article_tweet_consumption_enabled":true,"tweet_awards_web_tipping_enabled":false,"creator_subscriptions_quote_tweet_preview_enabled":false,"freedom_of_speech_not_reach_fetch_enabled":true,"standardized_nudges_misinfo":true,"tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled":true,"rweb_video_timestamps_enabled":true,"longform_notetweets_rich_text_read_enabled":true,"longform_notetweets_inline_media_enabled":true,"responsive_web_enhance_cards_enabled":false}}' 
    """

    bookmarks_command_split = shlex.split(bookmarks_command)
    subprocess.run(bookmarks_command_split)

    bottom_cursor = ""

    with open('skibidi16.txt', 'a') as file:
        process = subprocess.Popen(bookmarks_command_split, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        for line in process.stdout:
            file.write(line + '\n')  
            bottom_cursor = json.loads(line)["data"]["bookmark_timeline_v2"]["timeline"]["instructions"][0]["entries"][-1]["content"]["value"]
        
        for line in process.stderr:
            print(f"{line}", end='')

        process.wait(10)

    encoded_cursor = urllib.parse.quote(bottom_cursor)
    
    print(encoded_cursor)
    bookmarks_command_first_line = (
        f"curl --compressed 'https://x.com/i/api/graphql/xLjCVTqYWz8CGSprLU349w/Bookmarks?"
        f"variables=%7B%22count%22%3A20%2C%22includePromotedContent%22%3Atrue%2C%22cursor%22%3A%22{encoded_cursor}%22%7D'"
    )


