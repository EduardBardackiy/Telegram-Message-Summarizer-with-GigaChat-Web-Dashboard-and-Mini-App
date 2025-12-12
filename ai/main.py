import argparse
import logging
import sys

from gigachat import GigaChatError, generate_summary, get_access_token
from utils import init_env, pick_input_text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="CLI для получения выжимки текста через GigaChat"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    summary_parser = subparsers.add_parser("summary", help="Сделать выжимку текста")
    summary_parser.add_argument(
        "--file", type=str, help="Путь до файла с текстом", default=None
    )
    summary_parser.add_argument(
        "--text", type=str, help="Текст напрямую в аргументе", default=None
    )

    subparsers.add_parser("token", help="Получить OAuth access token для GigaChat")
    return parser


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
    )
    parser = build_parser()
    args = parser.parse_args(argv)

    init_env()

    if args.command == "summary":
        try:
            user_text = pick_input_text(args.text, args.file)
            result = generate_summary(user_text)
            print("\n--- Summary ---\n")
            print(result)
            print("\n--------------")
            return 0
        except FileNotFoundError as err:
            logging.error(str(err))
            return 1
        except ValueError as err:
            logging.error(str(err))
            parser.print_help()
            return 1
        except GigaChatError as err:
            logging.error("GigaChat error: %s", err)
            return 1
        except Exception as err:  # pragma: no cover - safety net
            logging.exception("Unexpected error: %s", err)
            return 1
    if args.command == "token":
        try:
            token = get_access_token()
            print(token)
            return 0
        except GigaChatError as err:
            logging.error("GigaChat error: %s", err)
            return 1
        except Exception as err:  # pragma: no cover - safety net
            logging.exception("Unexpected error: %s", err)
            return 1

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())

