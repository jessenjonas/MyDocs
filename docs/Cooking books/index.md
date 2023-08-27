---
hide:
  - toc
title: Cooking Books
---
# Cooking books
{% for item in navigation.pages if item.url.startswith(page.url) and not item.url == page.url %}
[**{{ urldecode(item.url).split('/')[:-1] | last }}**](/{{ item.url }})
{% endfor %}