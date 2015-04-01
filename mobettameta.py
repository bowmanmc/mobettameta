
#!/usr/bin/env python
from bs4 import BeautifulSoup
import json
import requests


class Stats:

    def __init__(self):
        self.stats = {}

    def increment_stat(self, name):
        if name not in self.stats:
            self.stats[name] = 0
        self.stats[name] = self.stats[name] + 1

    def max_stat(self, name, val):
        if name not in self.stats:
            self.stats[name] = 0
        if self.stats[name] < val:
            self.stats[name] = val

    def min_stat(self, name, val):
        if name not in self.stats:
            self.stats[name] = 0
        if self.stats[name] > val:
            self.stats[name] = val

    def set_stat(self, name, val):
        self.stats[name] = val


class StatsProcessor:

    def __init__(self):
        self.globalStats = Stats()

    def process_site(self, site):
        url = 'http://%s' % site
        print 'Processing url %s' % url

        siteStats = Stats()
        siteStats.set_stat('site_name', site)

        r = requests.get(url)
        page = BeautifulSoup(r.text)
        tags = page.find_all('meta')
        for tag in tags:
            print '    Processing Tag: %s' % tag
            self.globalStats.increment_stat('tag_count')
            siteStats.increment_stat('tag_count')
            attrs = tag.attrs
            for attr in attrs:
                self.globalStats.increment_stat('attribute.%s' % attr.lower())
        self.globalStats.increment_stat('num_sites')
        return siteStats


if __name__ == '__main__':
    file_path = 'data/top-100.csv'
    processor = StatsProcessor()
    #process_file(file_path)
    siteStats = processor.process_site('webslinger.io')
    print '----------------'
    print json.dumps(processor.globalStats.stats, sort_keys=True, indent=4)
    print '----------------'
    print json.dumps(siteStats.stats, sort_keys=True, indent=4)
