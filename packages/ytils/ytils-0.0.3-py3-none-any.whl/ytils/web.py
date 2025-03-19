import re
import traceback

import requests
try:
    from fake_useragent import FakeUserAgent
    from linkpreview import Link, LinkGrabber, LinkPreview, link_preview
except ImportError:
    pass

from .logger import Logger
from .reg_exp import RE

logger = Logger("ytils." + __name__)


def get_preview(url: str, content: str = None, parser: str = "html.parser") -> "LinkPreview":
    """
    The same as link_preview but with bigger buff size
    parser can be 'lxml'
    """
    if content is None:
        grabber = LinkGrabber(
            initial_timeout=50,
            maxsize=9048576,
            receive_timeout=50,
            chunk_size=1024,
        )
        content, url = grabber.get_content(url)

    link = Link(url, content)
    return LinkPreview(link, parser=parser)


def get_user_agent() -> str:
    default_user_agent = "Mozilla/5.0 (Linux; arm_64; Android 9; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 YaApp_Android/20.113.0 YaSearchBrowser/20.113.0 BroPP/1.0 SA/3 Mobile Safari/537.36"

    if not hasattr(get_user_agent, "fake_user_agent"):
        try:
            fake_user_agent = FakeUserAgent()
            get_user_agent.fake_user_agent = fake_user_agent
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error(e)

    if hasattr(get_user_agent, "fake_user_agent"):
        try:
            user_agent = get_user_agent.fake_user_agent.random
        except:
            user_agent = default_user_agent
    else:
        user_agent = default_user_agent

    return user_agent


def get_web_page_title(url: str) -> str:
    title = ""
    try:
        for i in range(3):
            user_agent = get_user_agent()
            headers = {"User-Agent": user_agent}
            if "youtube" in url:
                headers = {}

            response = requests.get(url, headers=headers)
            content = response.content
            if isinstance(content, bytes):
                content = content.decode()

            if len(content) != 0:
                search_results = re.search(r"<\W*title\W*(.*)</title", content, re.IGNORECASE)
                if not search_results:
                    continue
                title = search_results.group(1)
                if ">" in title:
                    x = title.split(">")[1:]
                    title = ">".join(x)
                if title:
                    break
    except Exception as e:
        logger.error(traceback.format_exc())
    return title


def extract_links_from_text(text: str) -> list:
    result = re.findall(RE.LINK, text)
    urls = [x[0] for x in result]
    return urls


def save_response_html(response, path="index.html"):
    with open(path, "wb") as f:
        f.write(response.content)

    return response.text


def get_ipinfo() -> dict:
    """Get user latitude and longitude etc"""
    try:
        response = requests.get('https://ipinfo.io')
        data = response.json()
        return data
    except:
        print("Error: Unable to detect your location.")
        return None

if __name__ == "__main__":
    text = "Hello https://play.google.com/store/apps/details?id=ua.sportlife.customer dear bear"
    links = extract_links_from_text(text)
    link = links[0] if links[0:] else None
    if link:
        title = get_web_page_title(link)
        print(title)
        preview = get_preview(link)
        print(f"[{preview.title}]({link})\n![{preview.title}]({preview.image})\n\n")
