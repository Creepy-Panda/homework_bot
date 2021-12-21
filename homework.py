import logging
import os
import time

import requests
from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os .getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 2
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


class GetAPIAnswerError(Exception):
    """Custom error."""

    pass


def send_message(bot, message):
    """Send message to user in telegram."""
    try:
        logging.info('message send')
        return bot.send_message(TELEGRAM_CHAT_ID, message)
    except Exception:
        logging.error('error with send message')
        print(f'error from send message {Exception}')


def get_api_answer(current_timestamp):
    """Get json from api."""
    logging.debug('start get_api_answer')
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    try:
        answer = requests.get(ENDPOINT, headers=HEADERS, params=params)
    except requests.RequestException as e:
        logging.error('Error request')
        error_message = f'error {e}'
        main.old_message = error_message
        send_message(main.bot, error_message)
        raise Exception(error_message)
    if answer.status_code != 200:
        raise Exception('server not response')
    try:
        return answer.json()
    except ValueError:
        logging.error('Error json')
        raise ValueError('json error')


def check_response(response):
    """Check valid json response."""
    logging.debug('start check response')
    if isinstance(response, dict):
        if 'homeworks' in response and isinstance(response['homeworks'], list):
            homeworks = response['homeworks']
        else:
            raise IndexError('Empty response')
        if not isinstance(homeworks[0], dict):
            raise TypeError('not Dict')
        return homeworks
    else:
        raise TypeError('not Dict')


def parse_status(homework):
    """Check status of review work."""
    logging.debug('start parse_status')
    homework_name = homework['homework_name']
    homework_status = homework['status']
    if homework_status in HOMEWORK_STATUSES:
        verdict = HOMEWORK_STATUSES[homework_status]
    else:
        raise ValueError('error verdict')

    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Check tokens if none flag false."""
    if None in [HEADERS, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]:
        return False
    return True


def main():
    """Main logic work for bot."""
    logging.debug('start main')
    bot = Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    old_message = ''
    check = check_tokens()
    if check is False:
        for i in [HEADERS, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]:
            if i is None:
                message = f'Empty token {i}'
                logging.error(message)
                print(message)
    while check:
        try:
            logging.debug('start while')
            homeworks = get_api_answer(current_timestamp)
            homework = check_response(homeworks)
            if homework:
                status_homework = parse_status(homework)
                send_message(bot, status_homework)
            time.sleep(RETRY_TIME)

        except Exception as error:
            logging.error('Error main')
            message = f'Сбой в работе программы: {error}'
            if old_message == message:
                continue
            old_message = message
            send_message(bot, message)
            time.sleep(RETRY_TIME)


def logger():
    """Log setup."""
    logging.basicConfig(
        level=logging.DEBUG,
        filename='main.log',
        filemode='w'
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler
    logger.addHandler(handler)


if __name__ == '__main__':
    logger()
    main()
