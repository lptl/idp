import os
from dotenv import load_dotenv
from app import app


def main() -> None:
    '''main function'''
    load_dotenv()
    debug = bool(int(os.environ.get('DEBUG', False)))
    debug = app.enable_dev_tools(debug=debug)
    app.server.run(host='0.0.0.0', port=8060, debug=debug)


if __name__ == '__main__':
    main()
