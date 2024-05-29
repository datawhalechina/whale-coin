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


if __name__ == "__main__":

    username = "shalucuidao"

    #获取所有仓库信息
    repos = get_all_repos(username)
    print(repos)
    # save_info_to_json(repos, "all_repos.json")

    #获取所有仓库贡献者
    repos_info = get_all_repos_contributors(repos,username)
    print(repos_info)

    # save_info_to_json(repos_info, "all_repos_contributors.json")

    # 获取单个仓库贡献者
    repo_name = 'pythonrumen'
    contributors = get_one_repo_contributors(username, repo_name)
    print(contributors)
    # save_info_to_json(contributors, f'{repo_name}_contributors.json')

