---
hide:
  - toc
tags:
  - Cooking book
title: Cisco cooking book
---
# Cisco cooking book
{% for item in page.parent.children[1:] %}
{% if item.children %}
</br>
**{{ item.title }}**
{% for item in item.children %}
[**{{ urldecode(item.url).split('/')[:-1] | last }}**](/{{ item.url }})
{% endfor %}
{% else %}
[**{{ urldecode(item.url).split('/')[:-1] | last }}**](/{{ item.url }})
{% endif %}
{% endfor %}