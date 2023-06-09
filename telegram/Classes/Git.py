import requests
from pathlib import Path
import configparser
from typing import Any

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]

config = configparser.ConfigParser()
config.read(ROOT /'config.ini')
backhost = config['DEFAULT']['BACKHOST']
backport = config['DEFAULT']['BACKPORT']


class Contribution:

    def __init__(
            self,
            action: str,
            count: int
            ) -> None:
        self.action = action
        self.count = count
        

class GitHistory:
    
    def __init__(
            self,
            userId: int,
            contributions: list[dict[str, Any]]
            ) -> None:
        self.userId = userId
        self.contributions = [Contribution(**e) for e in contributions]

    @property
    def ApprovedMergeRequests(self) -> int:
        try:
            return self.contributions[[e.action for e in self.contributions].index('Одобрил merge request')].count
        except ValueError:
            return 0
        
    @property
    def OpenedMergeRequests(self) -> int:
        try:
            return self.contributions[[e.action for e in self.contributions].index('Создал merge request')].count
        except ValueError:
            return 0

    @property
    def AcceptedMergeRequests(self) -> int:
        try:
            return self.contributions[[e.action for e in self.contributions].index('Слил ветку')].count
        except ValueError:
            return 0

    @property
    def PushedCommits(self) -> int:
        try:
            return self.contributions[[e.action for e in self.contributions].index('Запушил commit')].count
        except ValueError:
            return 0


def GetChatGit(chatId: int):
    responce: requests.Response = requests.get(
        url=f'http://{backhost}:{backport}/api/gitlab/get/stats/{chatId}',
        headers={"Content-Type": "application/json"})
    
    data: list[dict[str, Any]] = responce.json()
    gits: list[GitHistory] = [GitHistory(**e) for e in data]
    return gits

        