import urllib.request
import json
import argparse

#COLORS
green = "\033[92m"
red = "\033[31m"
reset = "\033[0m"

def load_api(username):
    with urllib.request.urlopen(f'https://api.github.com/users/{username}/events') as response:
        html_response = response.read()

    with open("user_data.json", "w") as f:
        json_data = json.loads(html_response.decode("utf-8"))
        json.dump(json_data, f, indent=2)

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
        load_api(username=args.username)
        data = save_api_data()
        push_count = {}
        
        for i in data:
            if i['type'] == "PushEvent":
                repo_name = i['repo']['name']

                push_count[repo_name] = push_count.get(repo_name, 0) + 1
        for repo, count in push_count.items():
            print(f"{args.username} pushed {red}{count}{reset} updates to {green}{repo}{reset}")

if __name__ == "__main__":
    main()