import urllib.request
import json
import argparse

#COLORS
green = "\033[92m"
red = "\033[31m"
reset = "\033[0m"

def load_api(username):
    try:
        with urllib.request.urlopen(f'https://api.github.com/users/{username}/events') as response:
            html_response = response.read()

        with open("user_data.json", "w") as f:
            json_data = json.loads(html_response.decode("utf-8"))
            json.dump(json_data, f, indent=2)
    except urllib.error.HTTPError:
        return False
    
def save_api_data():
    with open('user_data.json', 'r') as f:
        data = json.load(f)
        return data

def main():
#Setting up argparse
    parser = argparse.ArgumentParser(description= "A command line interface for finding out recent data on a users Github")
    subparser = parser.add_subparsers(dest="command")
#Setting up Look Up Tool
    find_parser = subparser.add_parser("find")
    find_parser.add_argument("username")
#setting up args
    args = parser.parse_args()

#FIND
    if args.command == "find":
        if load_api(username=args.username) is False:
            print(f"{red}Invalid Username, Try Again{reset}")
        else:
            data = save_api_data()
            push_count = {}
            issue_count = {}
    #Finding repo commits
            for i in data:
                if i['type'] == "PushEvent":
                    repo_name = i['repo']['name']

                    push_count[repo_name] = push_count.get(repo_name, 0) + 1
            for repo, count in push_count.items():
                if count > 1:
                    print(f"{args.username} pushed {red}{count}{reset} commits to {green}{repo}{reset}")
                else:
                    print(f"{args.username} pushed {red}{count}{reset} commit to {green}{repo}{reset}")

    #Finding issues
            for i in data:
                if i['type'] == "IssuesEvent":
                    issue_count[repo_name] = issue_count.get(repo_name, 0) + 1
            for repo, count in issue_count.items():
                if count > 1:
                    print(f"{args.username} opened {red}{count}{reset} new issue's in {green}{repo}{reset}")
                else:
                    print(f"{args.username} opened {red}{count}{reset} new issue in {green}{repo}{reset}")

if __name__ == "__main__":
    main()