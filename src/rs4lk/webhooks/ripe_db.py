import logging
import re

import requests


class RipeDb:
    URL: str = 'https://rest.db.ripe.net/search.txt?query-string=AS%d&flags=no-referenced&flags=no-irt&source=RIPE'
    RPSL_REGEX = re.compile(r"^(?P<key>.*):\s+(?P<value>.*)$")

    def get_local_as_rules(self, as_num: int) -> (list[str], list[str]):
        logging.info(f"Querying RIPE DB for AS{as_num}.")

        response = requests.get(url=self.URL % as_num)
        response.raise_for_status()

        import_rules = []
        export_rules = []

        lines = response.text.split('\n')
        for line in lines:
            matches = self.RPSL_REGEX.search(line.strip())

            if not matches:
                continue

            key = matches.group("key").strip()
            value = matches.group("value").strip()

            if 'import' in key:
                import_rules.append(value)
            if 'export' in key:
                export_rules.append(value)

        return import_rules, export_rules
