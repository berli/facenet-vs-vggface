from goose import Goose

url = 'http://3joz.blog.163.com/blog/static/16046290200792807390/'
g = Goose()
article = g.extract(url=url)
print article.title
print article.meta_description
print article.cleaned_text[:1500]
#print article.top_image.src


