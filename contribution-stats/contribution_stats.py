import requests


def contribution_stats(username):
    '''
    Count additions/deletions across all public repositories owned by a particular user
    using GitHub API without authentication
    '''
    counts = {}

    req = requests.get("https://api.github.com/users/{}/repos".format(username))
    resp_json = req.json()

    repo_names = list(map(lambda x: x['name'],resp_json))

    for repo_name in repo_names:
        counts[repo_name] = {'Additions':0, 'Deletions':0, 'Commits':0}
        req_url = "https://api.github.com/repos/{}/{}/stats/contributors".format(username,repo_name)

        curr_req = requests.get(req_url)
        curr_req_json = curr_req.json()

        for contributor in curr_req_json:
            if contributor['author']['login'] == username:
                for week in contributor['weeks']:
                    counts[repo_name]['Additions'] += week['a']
                    counts[repo_name]['Deletions'] += week['d']
                    counts[repo_name]['Commits'] += week['c']

    total_additions = 0
    total_deletions = 0
    total_commits = 0

    print("Breakdown by repository: \n")

    for repo in counts.keys():
        total_additions += counts[repo]['Additions']
        total_deletions += counts[repo]['Deletions']
        total_commits += counts[repo]['Commits']
        print("{}:\nLines added: {}\nLines deleted: {}\nCommits: {}\n".format(repo,counts[repo]['Additions'],counts[repo]['Deletions'],counts[repo]['Commits']))

    print("-----------------------")
    print("Total Additions: {}".format(total_additions))
    print("Total Deletions: {}".format(total_deletions))
    print("Total Additions + Deletions: {}".format(total_additions + total_deletions))
    print("Total Commits: {}".format(total_commits))


username = ""

while (type(username) != str or len(username) == 0):
    username = input("Enter your GitHub username: \n")

contribution_stats(username)
    
    
        
