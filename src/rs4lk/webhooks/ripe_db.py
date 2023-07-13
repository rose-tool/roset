import logging
import re


class RipeDb:
    URL: str = 'https://rest.db.ripe.net/search.txt?query-string=AS%d&flags=no-referenced&flags=no-irt&source=RIPE'
    RPSL_REGEX = re.compile(r"^(?P<key>.*):\s+(?P<value>.*)$")

    def get_local_as_rules(self, as_num: int) -> (list[str], list[str]):
        logging.info(f"Querying RIPE DB for AS{as_num}.")

        # TODO: Reactivate this
        # response = requests.get(
        #     url=self.RIPE_DB_URL_TEMPLATE % as_num,
        # )
        # response.raise_for_status()

        response_text = """
        as-block:       AS59392 - AS61261
descr:          RIPE NCC ASN block
remarks:        These AS Numbers are assigned to network operators in the RIPE NCC service region.
mnt-by:         RIPE-NCC-HM-MNT
created:        2020-06-22T15:23:11Z
last-modified:  2020-06-22T15:23:11Z
source:         RIPE

aut-num:        AS59715
as-name:        SBTAP-AS
org:            ORG-CdSB1-RIPE
mp-import:      afi ipv4.unicast from AS12874 accept any
mp-import:      afi ipv6.unicast from AS12874 accept any
mp-import:      afi ipv4.unicast from AS6762 accept any
mp-import:      afi ipv6.unicast from AS6762 accept any
mp-import:      afi ipv4.unicast from AS112 accept AS112
mp-import:      afi ipv6.unicast from AS112 accept AS112
mp-export:      afi ipv4.unicast to AS12874 announce AS-SBTAP
mp-export:      afi ipv6.unicast to AS12874 announce AS-SBTAP
mp-export:      afi ipv4.unicast to AS6762 announce AS-SBTAP
mp-export:      afi ipv6.unicast to AS6762 announce AS-SBTAP
mp-export:      afi ipv4.unicast to AS112 announce any
mp-export:      afi ipv6.unicast to AS112 announce any
admin-c:        SBT21-RIPE
tech-c:         SBT20-RIPE
tech-c:         AP7729-RIPE
status:         ASSIGNED
mnt-by:         RIPE-NCC-END-MNT
mnt-by:         SBTAP-MNT
created:        2012-10-04T12:53:46Z
last-modified:  2022-10-24T14:18:26Z
source:         RIPE
"""

        import_rules = []
        export_rules = []

        lines = response_text.split('\n')
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
