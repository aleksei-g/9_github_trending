import requests
from datetime import date, timedelta
import time


TOP_SIZE = 20


def get_trending_repositories():
    created_repository_days_ago = 7
    created_prior_to_date = date.today() -\
        timedelta(days=created_repository_days_ago)
    url = 'https://api.github.com/search/repositories'
    payload = {'q': 'created:>=%s' % created_prior_to_date,
               'sort': 'stars',
               'order': 'desc'}
    response = requests.get(url, params=payload)
    return response.json()['items'][:TOP_SIZE]


def get_open_issues_amount(repo_owner, repo_name):
    url = 'https://api.github.com/repos/%s/%s/issues' % (repo_owner, repo_name)
    response = requests.get(url)
    return len(response.json())


def output_repositories_to_console(repositories):
    print('Trending repositories on GitHub this week:')
    for num, repo in enumerate(repositories, start=1):
        fmt_in = "%Y-%m-%dT%H:%M:%SZ"
        fmt_out = "%Y-%m-%d %H:%M:%S"
        print('%s.\tName: %s' % (num, repo['name']))
        print('\tLogin owner: %s' % repo['owner']['login'])
        print('\tURL: %s' % repo['html_url'])
        print('\tCreated at: %s' % time.strftime(fmt_out,
              time.strptime(repo['created_at'], fmt_in)))
        print('\tStargazers count: %s' % repo['stargazers_count'])
        print('\tOpen issues amount: %s' %
              get_open_issues_amount(repo['owner']['login'], repo['name']))
        print('')


if __name__ == '__main__':
    trending_repositories = get_trending_repositories()
    output_repositories_to_console(trending_repositories)
