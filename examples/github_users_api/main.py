import argparse
import logging
import os

from api.session import GithubAPI

if __name__ == '__main__':
    logger = logging.getLogger('GithubLogger')

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Github Argument Parser')
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        help='Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)',
    )
    parser.add_argument(
        '--token',
        type=str,
        default=os.getenv('GITHUB_TOKEN'),
        help='The user github token',
    )
    args = parser.parse_args()

    # extract arguments
    token = args.token
    log_level = args.log_level.upper()

    # Configure logging
    logging.basicConfig(level=log_level, format='%(message)s')
    with GithubAPI(
        token=token,
    ) as github:
        logger.info('Fetching the list of users')
        for user in github.users.list(max_pages=1):
            logger.info(f'id: {user["id"]}')
            logger.info(f'username: {user["login"]}\n')

        logger.info('\nFetching the details of logged in user')
        user = github.users.get_current_user()
        if user:
            logger.info(f'id: {user["id"]}')
            logger.info(f'username: {user["login"]}')
