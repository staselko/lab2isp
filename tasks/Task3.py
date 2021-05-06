import re

class Task3:
    def validate_email(self, string):
        return True if re.fullmatch(r"^[\w\.]+@[\w\.]+\.[\w\.]+$", string) != None else False

    def validate_float(self, string):
        return True if re.fullmatch(r"^[+-]?(?:\d(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?$", string) != None else False

    def inspect_url(self, url_string):
        parts = re.match(r"^(?P<scheme>\w+)\:\/\/(?:(?P<host_ip>(?:\d{1,3}\.){3}\d)?:(?P<port>\d{1,5})?|(?P<web_domain>[\w\.]+))\/(?P<path>[^?#]*)?(?:\?(?P<params>.*))?\#?(?P<element_id>.*)?", url_string)
        for v in parts.groupdict():
            if v is not None or v != "None":
                print(v + " -> " + parts[v] if parts[v] is not None else v + " -> None")
        return