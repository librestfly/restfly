import os

from dotenv import load_dotenv

from api.session import GithubAPI

if __name__ == '__main__':
    load_dotenv()  # Get the github credentials and log level from .env file

    with GithubAPI(
        url=os.getenv('GITHUB_URL'),
        token=os.getenv('GITHUB_TOKEN'),
        log_level=os.getenv('LOG_LEVEL'),
    ) as github:
        github._log.info('Fetching the list of users')
        for user in github.users.list(max_pages=1):
            github._log.info(f'id: {user["id"]}')
            github._log.info(f'username: {user["login"]}\n')

        github._log.info('\nFetching the details of logged in user')
        user = github.users.get_current_user()
        if user:
            github._log.info(f'id: {user["id"]}')
            github._log.info(f'username: {user["login"]}')
