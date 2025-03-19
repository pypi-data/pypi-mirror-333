<h1 align="center">EasySoccerData</h1>
<p align="center">
A simple python package for extracting real-time soccer data from diverse online sources, providing essential statistics and insights.
</p>


> [!IMPORTANT]  
> Currently in the early development phase. Please take this into consideration.

# Installation
```
pip install EasySoccerData
```

# Usage

Simple demonstration of a live table using Sofascore module (see [source code](https://github.com/manucabral/EasySoccerData/blob/main/examples/live_table.py))
<p align="center">
<img src="https://github.com/manucabral/EasySoccerData/blob/main/assets/sofascore-live-table.gif" width="550" title="LiveTableUsingSofascore">
</p>

Another example
```py
import esd

# get live events
client = esd.SofascoreClient()
events = client.get_events(live=True)
for event in events:
    print(event)
```

[How to search for matches, teams, tournaments, and players](https://github.com/manucabral/EasySoccerData/blob/main/examples/search_matchs.py)

[How to get lineups for a match](https://github.com/manucabral/EasySoccerData/blob/main/examples/match_lineups.py)

[How to get live match statistics](https://github.com/manucabral/EasySoccerData/blob/main/examples/get_live_matchs.py)


And more! Check out [examples](https://github.com/manucabral/EasySoccerData/tree/main/examples)

# Supported modules

| Name | Implemented |
| :---  | :---: |
| Sofascore   | ✔️ |
| FBref    | ❌ |
| Understat | ❌ |
...

### Constributions
All constributions, bug reports or fixes and ideas are welcome.
