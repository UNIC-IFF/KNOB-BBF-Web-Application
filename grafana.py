from grafana_client import GrafanaApi
# Use HTTP basic authentication
import json
import sys


def main():
    grafana = GrafanaApi(
        auth=("admin", "password"),
        host='localhost:3000'
    )

    print("## All folders on play.grafana.org", file=sys.stderr)
    folders = grafana.dashboard.get_dashboard('QC1Arp5Wk')
    print(json.dumps(folders))



if __name__ == "__main__":
    main()