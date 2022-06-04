import json


class Stats:
    def __init__(self):
        self.reserved_path = "resources/statistics_cpy.json"
        self.path = "resources/statistics.json"

        self.wins_stats_path = "resources/wins_stats.json"
        self.reserved_wins_stats_path = "resources/wins_stats_cpy.json"

        self.data: dict
        self.reserved_data: dict
        self.wins_stats: dict
        self.reserved_wins_stats: dict
        self.parse()

    def __del__(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f)

        with open(self.wins_stats_path, "w") as f:
            json.dump(self.wins_stats, f)

    def parse(self):
        with open(self.path) as f:
            self.data = json.load(f)

        with open(self.wins_stats_path) as f:
            self.wins_stats = json.load(f)

    def add_to_stats(self, wins_or_loses: str, first_number: str, problem: str):
        self.data[wins_or_loses][first_number][problem] += 1

        if wins_or_loses == "wins":
            self.wins_stats["wins"] += 1
            self.wins_stats["total"] += 1

        if wins_or_loses == "loses":
            self.wins_stats["loses"] += 1
            self.wins_stats["total"] += 1

    def reset_stats(self):
        with open(self.reserved_path) as inp:
            with open(self.path, "w") as out:
                for line in inp:
                    out.write(line)

        with open(self.reserved_wins_stats_path) as inp:
            with open(self.wins_stats_path, "w") as out:
                for line in inp:
                    out.write(line)

        self.parse()

