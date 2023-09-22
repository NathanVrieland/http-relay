from html.parser import HTMLParser

# class RouteAdder(HTMLParser):
    # def __init__(self, site_root):
    #     self.site_root = site_root
    #     super().__init__()

#     def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
#         if tag == 'a':
#             for i, (attr, value) in enumerate(attrs):
#                 if attr == "href":
#                     attrs[i] = self.site_root + value

class RouteAdder(HTMLParser):
    def __init__(self, site_root):
        self.site_root = site_root
        self.modified_html = []
        super().__init__()

    def handle_starttag(self, tag, attrs):
        if tag in ('a', 'script', 'img', 'link'):
            # Loop through the attributes of the <a> tag
            modified_attrs = []
            for attr, value in attrs:
                if attr in ('href', 'src'):
                    # Modify the href attribute here
                    try:
                        new_value = f"/https://{self.site_root}{value}" if value[0] == '/' else value
                    except IndexError:
                        new_value = value # just skip it
                    modified_attrs.append((attr, new_value))
                else:
                    modified_attrs.append((attr, value))
            # Reconstruct the <a> tag with modified href
            modified_tag = f"""<{tag} {" ".join([f"{attr}='{value}' " for attr, value in modified_attrs])}>"""
            self.modified_html.append(modified_tag)
        else:
            # For other tags, simply add them as is
            self.modified_html.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        self.modified_html.append(f"</{tag}>")

    def handle_data(self, data):
        self.modified_html.append(data)

    def get_data(self):
        return ''.join(self.modified_html)