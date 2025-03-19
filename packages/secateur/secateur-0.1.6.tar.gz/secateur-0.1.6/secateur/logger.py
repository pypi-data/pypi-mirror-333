import json
import logging
import warnings

class Logger:
    def __init__(self, secateur_id, log):
        self.secateur_id = secateur_id
        self.logger = logging.getLogger("Secateur")
        self.logger.setLevel(logging.INFO)
        self.report = {
            "id": secateur_id,
            "collections": {}
        }
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        if log:
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(formatter)

            fh = logging.FileHandler(f"secateur-{secateur_id}.log", mode="a")
            fh.setLevel(logging.INFO)
            fh.setFormatter(formatter)

            self.logger.addHandler(ch)
            self.logger.addHandler(fh)

    def save_report(self, path: str = None) -> None:
        path = f"report-{self.secateur_id}.json" if not(path) else path
        with open(path, 'w') as json_file:
            json.dump(self.report, json_file, indent=4)
