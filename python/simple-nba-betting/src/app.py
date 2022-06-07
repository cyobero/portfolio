from utils import get_results
from urllib.error import HTTPError

if __name__ == "__main__":
    team = ""
    year = 2022
    while True:
        user_input = input(
            """
            Enter team and year season ends (example: `bos 2022` returns game results for
            Boston Celtics 2021-2022 season) [press 'q' to exit]:  
            """
        )
        if user_input == 'q'.lower():
            print("OK bye then!")
            break
        team, season = user_input.split(' ')[0].rstrip(), user_input.split(' ')[1].rstrip()
        try:
            df = get_results(team.upper(), int(year))
            print(df.to_string())
        except HTTPError:
            print("Couldn't find team or season")
