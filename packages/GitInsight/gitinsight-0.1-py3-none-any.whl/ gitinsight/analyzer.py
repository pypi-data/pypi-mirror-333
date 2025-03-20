from git import Repo
import pandas as pd
from datetime import datetime

class GitAnalyzer:
    def __init__(self, repo_path):
        """
        Initialize the analyzer with the repository path.
        :param repo_path: Path to the Git repository
        """
        self.repo = Repo(repo_path)

    def get_commit_frequency(self):
        """
        Get commit frequency over time.
        :return: DataFrame with commit counts per day
        """
        commits = list(self.repo.iter_commits())
        commit_dates = [commit.committed_datetime.date() for commit in commits]
        df = pd.DataFrame(commit_dates, columns=['date'])
        return df.groupby('date').size().reset_index(name='commits')

    def get_contributor_stats(self):
        """
        Get contributor statistics.
        :return: DataFrame with contributor commit counts
        """
        commits = list(self.repo.iter_commits())
        contributors = {}
        for commit in commits:
            author = commit.author.name
            contributors[author] = contributors.get(author, 0) + 1
        return pd.DataFrame(list(contributors.items()), columns=['contributor', 'commits'])

    def get_active_hours(self):
        """
        Get commit activity by hour of the day.
        :return: DataFrame with commit counts per hour
        """
        commits = list(self.repo.iter_commits())
        commit_hours = [commit.committed_datetime.hour for commit in commits]
        df = pd.DataFrame(commit_hours, columns=['hour'])
        return df.groupby('hour').size().reset_index(name='commits')