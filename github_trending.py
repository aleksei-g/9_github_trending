import requests
from datetime import date, timedelta
import time


TOP_SIZE = 20
AGE_REPO = 7


def get_trending_repositories():
    created_prior_to_date = date.today() - timedelta(days=1)*AGE_REPO
    url = 'https://api.github.com/search/repositories?q=+created:>=%s\
           &sort=stars&order=desc' % (created_prior_to_date)
    response = requests.get(url)
    return response.json()['items'][0:TOP_SIZE]


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
