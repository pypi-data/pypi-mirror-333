import os
import tempfile
from git import Repo
from gitinsight.analyzer import GitAnalyzer

def test_get_commit_frequency():
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = Repo.init(tmpdir)
        open(os.path.join(tmpdir, 'test.txt'), 'w').close()
        repo.index.add(['test.txt'])
        repo.index.commit('Initial commit')

        analyzer = GitAnalyzer(tmpdir)
        df = analyzer.get_commit_frequency()
        assert not df.empty

def test_get_contributor_stats():
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = Repo.init(tmpdir)
        open(os.path.join(tmpdir, 'test.txt'), 'w').close()
        repo.index.add(['test.txt'])
        repo.index.commit('Initial commit')

        analyzer = GitAnalyzer(tmpdir)
        df = analyzer.get_contributor_stats()
        assert not df.empty