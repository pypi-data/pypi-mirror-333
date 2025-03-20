import logging
import os
import sys
from activation import Activation


def main():
    logging.info("***********BEGIN: main***********")
    if (len(sys.argv) == 2 and os.path.exists(sys.argv[1])):
        logging.info("***********JSON file provided***********")
        logging.info(sys.argv[1])
        activation_obj = Activation(sys.argv[1])
        activation_obj.entry_point()
    else:
        logging.error("***********JSON file not provided***********")
        logging.error("***********Please provide JSON file***********")


if __name__ == "__main__":
    main()
 