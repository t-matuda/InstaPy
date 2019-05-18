""" Module that handles the like features """
import random
import re
from re import findall

from .time_util import sleep
from .util import format_number
from .util import add_user_to_blacklist
from .util import click_element
from .util import is_private_profile
from .util import is_page_available
from .util import update_activity
from .util import web_address_navigator
from .util import get_number_of_posts
from .util import get_action_delay
from .util import explicit_wait
from .util import extract_text_from_element
from .like_util import check_link
from .like_util import get_tags
from .quota_supervisor import quota_supervisor
from .unfollow_util import get_following_status
from .comment_util import is_commenting_enabled
from .comment_util import get_comments_count

from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException    
from selenium.common.exceptions import JavascriptException


def get_post_engagement(browser, link, logger):
    # コメント数
    comments_count = 0
    commenting_state, msg = is_commenting_enabled(browser, logger)
    if commenting_state is not True:
        logger.info("--> Not commenting! {}".format(msg))

    comments_count, msg = get_comments_count(browser, logger)
    if not comments_count:
        logger.info("--> Not commenting! {}".format(msg))


    # いいね数
    """ Get the amount of existing existing likes"""
    likes_count = 0
    try:
        likes_count = browser.execute_script(
            "return window._sharedData.entry_data."
            "PostPage[0].graphql.shortcode_media.edge_media_preview_like"
            ".count")

    except WebDriverException:
        try:
            browser.execute_script("location.reload()")
            update_activity()

            likes_count = browser.execute_script(
                "return window._sharedData.entry_data."
                "PostPage[0].graphql.shortcode_media.edge_media_preview_like"
                ".count")

        except WebDriverException:
            try:
                likes_count = (browser.find_element_by_css_selector(
                    "section._1w76c._nlmjy > div > a > span").text)

                if likes_count:
                    likes_count = format_number(likes_count)
                else:
                    logger.info(
                        "Failed to check likes' count  ~empty string\n")

            except NoSuchElementException:
                logger.info("Failed to check likes' count\n")

    # ハッシュタグ
    try:
        tags = get_tags(browser, link)
    
    except JavascriptException as err:
        logger.error('Can not get tags: {}'.format(err))
        tags = []
    
    
    return likes_count, comments_count, tags