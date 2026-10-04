from pathlib import Path
import re

# Fix every legacy JSDoc function tag that Shopify's HTML parser can mistake
# for a custom element, e.g. @function[<productInventory>].
js_path = Path('assets/VastaShop.js.liquid')
js = js_path.read_text(encoding='utf-8')
js = re.sub(r'@function\[<([A-Za-z_$][A-Za-z0-9_$]*)>\]', r'@function \1', js)
js_path.write_text(js, encoding='utf-8')

# Balance the popular-collection markup in every Liquid branch.
footer_path = Path('snippets/footer-layout04.liquid')
footer = footer_path.read_text(encoding='utf-8')

old = '''      <div class="popular-collection-links">
        {%- for block in section.blocks -%}
          {%- if 'popular_collection' == block.type -%}
            {%- assign pop = pop | plus: 1 -%}

            {%- if pop == 1 -%}
              <h4 class="popular_collections_title">{{ section.settings.collection_title }}</h4>
              <div class="popular_collections_links">
            {%- endif -%}

            <a
              title="{{ block.settings.text_editable | strip_html | escape }}"
              id="ftr-pop_col-link-{{ block.id }}"
              href="{{ block.settings.link_popular_collection | default: '#' }}"
            >
              {%-
                render 'responsive-image',
                image: block.settings.url_popular_collection,
                width: 200,
                lazyload: true,
                id: index
              -%}
              {% if block.settings.text_editable != blank %}
                <h5 class="popular_collections_text">{{ block.settings.text_editable }}</h5>
              {% endif %}
            </a>
          {%- endif -%}
        {%- endfor -%}
        {%- comment -%} Start Closing of the "popular_collections_links" tag {%- endcomment -%}
        </div>
        {%- comment -%} End Closing of the "popular_collections_links" tag {%- endcomment -%}
      </div>'''

new = '''      <div class="popular-collection-links">
        {%- assign popular_collection_blocks = section.blocks | where: 'type', 'popular_collection' -%}
        {%- if popular_collection_blocks.size > 0 -%}
          <h4 class="popular_collections_title">{{ section.settings.collection_title }}</h4>
          <div class="popular_collections_links">
            {%- for block in popular_collection_blocks -%}
              <a
                title="{{ block.settings.text_editable | strip_html | escape }}"
                id="ftr-pop_col-link-{{ block.id }}"
                href="{{ block.settings.link_popular_collection | default: '#' }}"
              >
                {%-
                  render 'responsive-image',
                  image: block.settings.url_popular_collection,
                  width: 200,
                  lazyload: true,
                  id: index
                -%}
                {% if block.settings.text_editable != blank %}
                  <h5 class="popular_collections_text">{{ block.settings.text_editable }}</h5>
                {% endif %}
              </a>
            {%- endfor -%}
          </div>
        {%- endif -%}
      </div>'''

if old in footer:
    footer = footer.replace(old, new, 1)
elif new not in footer:
    raise SystemExit('Expected footer block was not found; refusing an unsafe rewrite.')

footer_path.write_text(footer, encoding='utf-8')
