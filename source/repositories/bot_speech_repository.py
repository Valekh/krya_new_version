from .abstract_repository import AbstractRepository
from source.models import BotSpeech


class BotSpeechRepository(AbstractRepository[BotSpeech]):
    _model = BotSpeech
