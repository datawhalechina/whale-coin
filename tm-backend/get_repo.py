import requests
import os,json




def get_all_repos(username):
    repos = []
    url = f"https://api.github.com/users/{username}/repos?page=1"
    while url:
        response = requests.get(url)
        if response.status_code == 200:
            repos += response.json()
            if 'link' in response.headers:
                # 解析分页链接
                links = response.headers['link'].split(', ')
                next_link = [link for link in links if 'rel="next"' in link]
                if next_link:
                    url = next_link[0].split(';')[0].strip('<>')
                else:
                    url = None
            else:
                break
        else:
            return "Error: Unable to fetch repositories"
        
    return repos

def get_all_repos_contributors(repos,username):
    base_url = "https://api.github.com"
   
    repos_info = []
    
    for repo in repos:
        repo_name = repo['name']
        contributors_url = f"{base_url}/repos/{username}/{repo_name}/contributors"
        contributors_response = requests.get(contributors_url)
        contributors = contributors_response.json()
        
        contributor_names = [contributor['login'] for contributor in contributors]
        
        repos_info.append({
            "repo_name": repo_name,
            "contributors": contributor_names
        })
    return repos_info


def get_one_repo_contributors(username, repo_name, oauth_token=None):

    url = f"https://api.github.com/repos/{username}/{repo_name}/contributors"
    headers = {"Authorization": f"token {oauth_token}"} if oauth_token else {}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        contributors = response.json()
        return [{"username": contributor["login"], "contributions": contributor["contributions"]} for contributor in contributors]
    else:
        print("无法获取贡献者信息，状态码：", response.status_code)
        return []

def save_info_to_json(info_dict, filename):

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(info_dict, f, ensure_ascii=False, indent=4)


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

def update_repo():

    username = "datawhalechina"

    #获取所有仓库信息
    # repos = get_all_repos(username)
    # save_info_to_json(repos, "all_repos.json")

    repos =[{'name':'zishu'}]

    all_issues = []
    all_prs = []

    # 获取每个仓库的所有issues和PRs
    for repo in repos:
        repo_name = repo['name']
        issues, prs = get_all_issues_and_prs(username, repo_name)
        issue_html = [issue['html_url']for issue in issues]

        # issues_closed = [issue for issue in issues if 'issues' in issue['html_url'] and issue['state']=='closed']
        # issues_open = [issue for issue in issues if 'issues' in issue['html_url'] and issue['state']=='open']

        for issue in issues[-1:]:
            print("html_url === ",issue['html_url'])
            state = issue['state']
            num = issue['number']
            print("1-------------", issue['number'], issue['state'], issue['title'], issue['comments_url'])
            print("issue ===== ", issue.items())
            for i, s in issue.items():
                print("i---------",i,s)
            # filename = f'{repo_name}_issue_{state}_{num}.json'
            # if index==0:
            #     with open(filename, 'w', encoding='utf-8') as f:
            #         json.dump(issue, f, ensure_ascii=False, indent=4)


        # for index,issue in enumerate(issues_closed):
        #     print("index === ",index)
        #     print("issue-t === ",type(issue),issue.items)
        #     print("html_url === ",issue['html_url'])
        #     state = issue['state']
        #     num = issue['number']
        #     print("1-------------", state, num)
        #     print("issue ===== ", issue.items())
        #     filename = f'{repo_name}_issue_{state}_{num}.json'
        #     if index==0:
        #         with open(filename, 'w', encoding='utf-8') as f:
        #             json.dump(issue, f, ensure_ascii=False, indent=4)
        print('-------------------'*7)



if __name__ == "__main__":
    update_repo()


# if __name__ == "__main__":
#
#     username = "datawhalechina"
#
#     #获取所有仓库信息
#     # repos = get_all_repos(username)
#     # save_info_to_json(repos, "all_repos.json")
#
#
#     # repos =[{'name':'joyrl-book'}]
#     repos =[{'name':'grape-book'}]
#
#     all_issues = []
#     all_prs = []
#
#     # 获取每个仓库的所有issues和PRs
#     for repo in repos:
#         repo_name = repo['name']
#         issues, prs = get_all_issues_and_prs(username, repo_name)
#         issue_html = [issue['html_url']for issue in issues]
#         print("issue_html = ", issue_html)
#
#         issues_closed = [issue for issue in issues if 'issues' in issue['html_url'] and issue['state']=='closed']
#         issues_open = [issue for issue in issues if 'issues' in issue['html_url'] and issue['state']=='open']
#
#         for index,issue in enumerate(issues_closed):
#             print("index === ",index)
#             print("issue-t === ",type(issue),issue.items)
#             print("html_url === ",issue['html_url'])
#             state = issue['state']
#             num = issue['number']
#             print("issue ===== ", issue.items())
#             filename = f'{repo_name}_issue_{state}_{num}.json'
#             if index==0:
#                 with open(filename, 'w', encoding='utf-8') as f:
#                     json.dump(issue, f, ensure_ascii=False, indent=4)
#         print('-------------------'*3)
#
#         # pr_closed = [pr for pr in prs if 'pull' in pr['html_url'] and pr['state']=='closed']
#         # pr_open = [pr for pr in prs if 'pull' in pr['html_url'] and pr['state']=='open']
#         # for item in [pr_closed,pr_open]:
#         #     for index,pr in enumerate(item):
#         #         print(index)
#         #         print(type(pr))
#         #         print(pr['html_url'])
#         #         state = pr['state']
#         #         num = pr['number']
#         #         filename = f'{repo_name}_pr_{state}_{num}.json'
#         #         if index==0:
#         #             print(pr)
#         #             with open(filename, 'w', encoding='utf-8') as f:
#         #                 json.dump(issue, f, ensure_ascii=False, indent=4)
#
#
#     #获取所有仓库贡献者
#     # repos_info = get_all_repos_contributors(repos,username)
#     # print(repos_info)
#
#     # save_info_to_json(repos_info, "all_repos_contributors.json")
#
#     # 获取单个仓库贡献者
#     # repo_name = 'pythonrumen'
#     # contributors = get_one_repo_contributors(username, repo_name)
#     # print(contributors)
#     # save_info_to_json(contributors, f'{repo_name}_contributors.json')

