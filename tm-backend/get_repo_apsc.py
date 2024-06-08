import requests
import os,json



def get_all_issues_and_prs(username, repo_name, oauth_token=None):
    base_url = f"https://api.github.com/repos/{username}/{repo_name}"

    headers = {"Authorization": f"token {oauth_token}"} if oauth_token else {}

    # 获取 issues
    issues_url = f"{base_url}/issues?state=all"
    issues_response = requests.get(issues_url, headers=headers)
    issues = issues_response.json() if issues_response.status_code == 200 else []

    # 获取 pull requests
    prs_url = f"{base_url}/pulls?state=all"
    prs_response = requests.get(prs_url, headers=headers)
    prs = prs_response.json() if prs_response.status_code == 200 else []

    return issues, prs


def get_repo_run():
    username = "datawhalechina"

    # 获取所有仓库信息
    # repos = get_all_repos(username)
    # save_info_to_json(repos, "all_repos.json")

    # repos =[{'name':'joyrl-book'}]
    repos = [{'name': 'grape-book'}]

    # 获取每个仓库的所有issues和PRs
    for repo in repos:
        repo_name = repo['name']
        issues, prs = get_all_issues_and_prs(username, repo_name)
        issue_html = [issue['html_url'] for issue in issues]
        print(issue_html)

        issues_closed = [issue for issue in issues if 'issues' in issue['html_url'] and issue['state'] == 'closed']
        issues_open = [issue for issue in issues if 'issues' in issue['html_url'] and issue['state'] == 'open']

        for index, issue in enumerate(issues_closed):
            print(index)
            print(type(issue))
            print(issue['html_url'])
            state = issue['state']
            num = issue['number']
            filename = f'{repo_name}_issue_{state}_{num}.json'
            if index == 0:
                print(issue)
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(issue, f, ensure_ascii=False, indent=4)
        print('-------------------' * 3)


if __name__ == "__main__":

    username = "datawhalechina"

    #获取所有仓库信息
    # repos = get_all_repos(username)
    # save_info_to_json(repos, "all_repos.json")


    # repos =[{'name':'joyrl-book'}]
    repos =[{'name':'grape-book'}]
    
    all_issues = []
    all_prs = []

    # 获取每个仓库的所有issues和PRs
    for repo in repos:
        repo_name = repo['name']
        issues, prs = get_all_issues_and_prs(username, repo_name)
        issue_html = [issue['html_url']for issue in issues]
        print(issue_html)

        issues_closed = [issue for issue in issues if 'issues' in issue['html_url'] and issue['state']=='closed']
        issues_open = [issue for issue in issues if 'issues' in issue['html_url'] and issue['state']=='open']

        for index,issue in enumerate(issues_closed):
            print(index)
            print(type(issue))
            print(issue['html_url'])
            state = issue['state']
            num = issue['number']
            filename = f'{repo_name}_issue_{state}_{num}.json'
            if index==0:
                print(issue)
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(issue, f, ensure_ascii=False, indent=4)
        print('-------------------'*3)

        # pr_closed = [pr for pr in prs if 'pull' in pr['html_url'] and pr['state']=='closed']
        # pr_open = [pr for pr in prs if 'pull' in pr['html_url'] and pr['state']=='open']
        # for item in [pr_closed,pr_open]:
        #     for index,pr in enumerate(item):
        #         print(index)
        #         print(type(pr))
        #         print(pr['html_url'])
        #         state = pr['state']
        #         num = pr['number']
        #         filename = f'{repo_name}_pr_{state}_{num}.json'
        #         if index==0:
        #             print(pr)
        #             with open(filename, 'w', encoding='utf-8') as f:
        #                 json.dump(issue, f, ensure_ascii=False, indent=4)


    #获取所有仓库贡献者
    # repos_info = get_all_repos_contributors(repos,username)
    # print(repos_info)

    # save_info_to_json(repos_info, "all_repos_contributors.json")

    # 获取单个仓库贡献者
    # repo_name = 'pythonrumen'
    # contributors = get_one_repo_contributors(username, repo_name)
    # print(contributors)
    # save_info_to_json(contributors, f'{repo_name}_contributors.json')

