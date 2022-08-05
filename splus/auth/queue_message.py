from dataclasses import field, dataclass
from flask import Request
from mashumaro.mixins.json import DataClassJSONMixin

from splus import constants

@dataclass
class QueueMessage(DataClassJSONMixin):
  state: str
  success: bool
  code: str
  error: str

  @classmethod
  def from_request(cls, request : Request):
    code = request.args.get(constants.RESPONSE_TYPE, type=str)
    state = request.args.get(constants.STATE, type=str)
    error = request.args.get("error", type=str)
    success = False if error else True
    return QueueMessage(state, success, code, error)