import logging
import argparse  

from implementation.telegram_parser import TelegramParser
from implementation.file_generator import JsonFileGenerator
from orchestrator.orchestrator import Orchestrator

"""Logging to file 'parser_errors.log'"""
logging.basicConfig(
    filename='parser_errors.log', 
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'  
)

if __name__ == "__main__":
    logging.info("Application started")
    
    """Parser of command-line arguments"""
    parser = argparse.ArgumentParser(description="Parse Telegram export JSON to extract subscribers.")
    parser.add_argument('--input_file', type=str, required=True, help="Path to the input JSON file (e.g., result.json)")
    args = parser.parse_args()
    
    input_file = args.input_file
    
    try:
        """Create instance of parser, generator, and orchestrator"""
        telegram_parser = TelegramParser()
        generator = JsonFileGenerator()
        orchestrator = Orchestrator(telegram_parser, generator)
        
        result_file = orchestrator.run(input_file)
        print(f"Success! Generated file: {result_file}")
        print("Check the output file for parsed subscribers.")
        logging.info("Application finished successfully")
    except Exception as e:
        logging.error(f"Application error: {str(e)}")
        print(f"Error: {e}")
    logging.info("Application finished")
    