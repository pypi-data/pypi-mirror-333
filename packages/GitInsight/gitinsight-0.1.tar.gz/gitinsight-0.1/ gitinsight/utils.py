def validate_repo_path(repo_path):
    """
    Validate if the given path is a valid Git repository.
    :param repo_path: Path to the repository
    :return: True if valid, False otherwise
    """
    try:
        Repo(repo_path)
        return True
    except:
        return False