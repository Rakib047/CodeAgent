# legacy_code.py

import utils1
import data_processing
import logger

def main():
    logger.log("Starting legacy code main")
    data = data_processing.load_data()
    processed = data_processing.process_data(data)
    utils1.print_list(processed)
    logger.log("Finished legacy code main")

if __name__ == "__main__":
    main()


