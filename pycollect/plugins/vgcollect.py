import requests

class VgCollectApi():
    excluded_category_id = ['29', '380', '381', '382', '383',
                            '384', '385', '386', '387']
    api_base_url = "http://api.vgcollect.com"
    api_key = 'abcdefg'

    def search_items(self, args):
        r = requests.get(
            '/'.join([self.api_base_url, 'search', '+'.join(args),
                     self.api_key]))
        if r.status_code == 200 and len(r.json()):
            return r.json()
        else:
            return None

    def get_item(self, item_id):
        r = requests.get('/'.join([self.api_base_url, 'items',
                                   item_id, self.api_key]))
        if r.status_code == 200 and len(r.json()):
            return r.json()['results']

    def search_games(self, *args):
        items = self.search_items(*args)
        results = []
        for r in items:
            if r['category_id'] not in self.excluded_category_id:
                results.append(r)
        return results
