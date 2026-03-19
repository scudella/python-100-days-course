from bs4 import BeautifulSoup
import requests
import pprint

# with open("website.html", "r") as file:
#     contents = file.read()
#     # print(contents)
#
# soup = BeautifulSoup(contents, "html.parser")

# print(soup.title.string)

# print(soup.prettify())

# all_anchor_tags = soup.find_all(name="a")
#
# print(all_anchor_tags)
#
# for tag in all_anchor_tags:
#     print(tag.get_text())
#     print(tag.get("href"))
#
# heading = soup.find(name="h1", id="name")
# print(heading)
#
# section_heading = soup.find(name="h3", class_="heading")
# print(section_heading.get_text())
#
# company_url = soup.select_one(selector="p a")
# print(company_url)
#
# name = soup.select_one(selector="#name")
# print(name)
#
# headings = soup.select(".heading")
# print(headings)

response = requests.get("https://news.ycombinator.com/news")
yc_webpage = response.text

soup = BeautifulSoup(yc_webpage, "html.parser")

span_tags = soup.find_all(name="span", class_="titleline")
article_texts = []
article_links = []
article_upvotes = []

for span_tag in span_tags:
    first_anchor = span_tag.find('a')
    text = first_anchor.get_text()
    article_texts.append(text)
    link = first_anchor['href']
    article_links.append(link)

print(article_texts)
print(article_links)
article_upvotes = [int(upvote.get_text().split()[0]) for upvote in soup.find_all(name="span", class_="score")]

max_value = max(article_upvotes)
max_index = article_upvotes.index(max_value)
print(max)
print(max_index)
print(article_texts[max_index])
print(article_links[max_index])

print(article_upvotes)