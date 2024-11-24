from typing import List
from decouple import config
from celery import shared_task
from trends.models import Trend
from posts.models import Post
from users.models import User
from datetime import datetime
from langchain import hub
from langchain_community.utilities import BingSearchAPIWrapper
from langchain_community.tools.bing_search import BingSearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import AzureChatOpenAI
import feedparser
import os


def fetch_google_trends() -> List[str]:
    feed = feedparser.parse('https://trends.google.com/trending/rss?geo=KR')
    results = []

    for entry in feed.entries:
        title = entry.title
        search_volume = entry.get('ht_approx_traffic', '0').replace('+', '').replace(',', '')
        results.append(title)

        try:
            started_at = datetime.strptime(entry.get('published'), '%a, %d %b %Y %H:%M:%S %z')
        except ValueError:
            started_at = None

        try:
            search_volume = int(search_volume)
        except ValueError:
            search_volume = 0

        Trend.objects.create(
            keyword=title,
            search_volume=search_volume,
            started_at=started_at,
        )
    return results


def azure_openai(system: str, user: str):
    os.environ["AZURE_OPENAI_API_KEY"] = config('AZURE_OPENAI_API_KEY')
    os.environ["AZURE_OPENAI_ENDPOINT"] = config('AZURE_OPENAI_ENDPOINT')
    os.environ["AZURE_OPENAI_API_VERSION"] = config('AZURE_OPENAI_API_VERSION')
    os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = config('AZURE_OPENAI_DEPLOYMENT_NAME')
    os.environ["BING_SUBSCRIPTION_KEY"] = config('BING_SUBSCRIPTION_KEY')
    os.environ["BING_SEARCH_URL"] = config('BING_SEARCH_URL')
    llm = AzureChatOpenAI(
        openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        azure_deployment=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    )
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=system)
    api_wrapper = BingSearchAPIWrapper(k=3)
    tool = BingSearchResults(api_wrapper=api_wrapper)
    tools = [tool]
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor.invoke({"input": user}).get("output", '')
    

def create_content(content: str):
    system_text = "키워드를 검색하고 글을 요약해주는 AI API야.\n"\
                    "사용자가 글을 입력하면 요약된 글을 한국어로 return 해줘.\n"\
                    "요약된 글은 제목과 함께 5줄이내로 요약해줘.\n"\
                    "무조건 아래와 같이 깔끔한 markdown 형식으로 만들어줘."\
                    "===\n# 제목\n내용"
                    
    data = azure_openai(system_text, content)
    return data


@shared_task
def fetch_and_generate_posts():
    keywords = fetch_google_trends()
    for keyword in keywords:
        content = create_content(keyword)
        Post.objects.create(
            title=keyword,
            content=content,
            author=User.objects.get(email='pangshe10@gmail.com')
        )

