import  sys
import http.client
import json

def fetch_github_activity(username):
    try:
        #Step 1: Create a connection to the Github API

        conn = http.client.HTTPSConnection("api.github.com")
        endpoint = f"/users/{username}/events"

        #Step 2: Send the GET request

        conn.request("GET", endpoint,headers={"User-Agent": "Github-Activity-CLI"})
        response = conn.getresponse()

        #Step 3: handle response
        if response.status == 200:
            data = json.loads(response.read())
            if not data:
                print(f"No recent activity {username} .")
                return
            display_activity_data(data)
        elif response.status == 400:
            print(f"User {username} not found in Github.")
        else:
            print(f"Failed to fetch data. HTTP Status: {response.status}")
    except Exception as e:
        print(f"An error occured as {e}")
    finally:
        conn.close()

def display_activity_data(events):
    print("\nRecent Activity")
    for event in events[:5]:
        event_type = event.get("type", "Unknown event")
        repo_name = event["repo"]["name"]
        created_at = event["created_at"]

        if event_type == "Pushevent":
            commits = len(event.get("payload",{}.get("commits",[])))
            print(f"- Pushed {commits} commits to {repo_name} at {created_at}")
        elif event_type == "IssuesEvent":
            action = event["payload"]["action"]
            print(f"- {action.capitalize()} an issue in {repo_name} at {created_at}")
        elif event_type == "WatchEvent":
            print(f"- Starred {repo_name} at {created_at}")
        else:
            print(f"- {event_type} on {repo_name} at {created_at}")

def main():
    if len(sys.argv) != 2:
        print("Usage: github-activity <username>")
        return
    
    username = sys.argv[1]
    fetch_github_activity(username)

if __name__ == "__main__":
    main()