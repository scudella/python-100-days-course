from bs4 import BeautifulSoup
import requests

HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}

response = requests.get("https://www.empireonline.com/movies/features/best-movies-2/", headers=HEADERS)
empire_webpage = response.text
# print(empire_webpage)
#
soup = BeautifulSoup(empire_webpage, "html.parser")
#
span_tags = soup.find_all(name="span", class_="content_content__i0P3p")

movie_titles = []
for span_tag in span_tags:
    movie = span_tag.select(selector="h2 strong")
    if movie:
        title = movie[0].get_text()
        if ")" in title:
            movie_titles.append(title)

movie_titles.reverse()
for title in movie_titles:
    print(title)

with open("movies.txt", "w") as file:
    for movie in movie_titles:
        file.write(f"{movie}\n")

