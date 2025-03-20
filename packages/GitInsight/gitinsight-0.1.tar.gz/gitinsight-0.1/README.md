
# GitInsight

GitInsight is a CLI tool to analyze Git repositories and provide insights like commit frequency, contributor stats, and more.

## Features
- Commit frequency over time.
- Contributor statistics.
- Commit activity by hour of the day.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
gitinsight /path/to/repo --commit-frequency --contributor-stats --active-hours
```

## Example Output
### Commit Frequency Over Time
![Commit Frequency](https://via.placeholder.com/600x300.png?text=Commit+Frequency+Graph)

### Contributor Statistics
```
Contributor  Commits
John Doe     10
Jane Smith   5
```

### Commit Activity by Hour of the Day
![Active Hours](https://via.placeholder.com/600x300.png?text=Active+Hours+Graph)

## License
MIT

### Step 8: Test the CLI
Run the CLI tool to analyze a Git repository:

```bash
gitinsight /path/to/repo --commit-frequency --contributor-stats --active-hours
```

