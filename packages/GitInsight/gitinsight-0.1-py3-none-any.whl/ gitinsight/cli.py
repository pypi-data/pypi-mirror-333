import click
import matplotlib.pyplot as plt
from .analyzer import GitAnalyzer

@click.command()
@click.argument('repo_path', type=click.Path(exists=True))
@click.option('--commit-frequency', is_flag=True, help='Show commit frequency over time')
@click.option('--contributor-stats', is_flag=True, help='Show contributor statistics')
@click.option('--active-hours', is_flag=True, help='Show commit activity by hour of the day')
def analyze(repo_path, commit_frequency, contributor_stats, active_hours):
    """
    Analyze a Git repository and provide insights.
    """
    analyzer = GitAnalyzer(repo_path)

    if commit_frequency:
        df = analyzer.get_commit_frequency()
        plt.figure(figsize=(10, 5))
        plt.plot(df['date'], df['commits'], marker='o')
        plt.title('Commit Frequency Over Time')
        plt.xlabel('Date')
        plt.ylabel('Commits')
        plt.grid(True)
        plt.show()

    if contributor_stats:
        df = analyzer.get_contributor_stats()
        print("Contributor Statistics:")
        print(df.to_string(index=False))

    if active_hours:
        df = analyzer.get_active_hours()
        plt.figure(figsize=(10, 5))
        plt.bar(df['hour'], df['commits'])
        plt.title('Commit Activity by Hour of the Day')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Commits')
        plt.xticks(range(24))
        plt.grid(True)
        plt.show()