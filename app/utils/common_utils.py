"""
Common Utils
"""
import logging
import datetime
import random

logger = logging.getLogger(__name__)


class CommonUtils:
    """
    Commn Utilitie
    """

    @staticmethod
    def type_cast_value(value, data_type):
        """
        Cast value by type
        :param value:
        :type value:
        :param data_type:
        :type data_type:
        :return:
        :rtype:
        """
        try:
            if data_type == 'integer':
                if not isinstance(value, int):
                    value = int(value)
            elif data_type == 'float':
                if not isinstance(value, float):
                    value = float(value)
            elif data_type == 'boolean':
                value = bool(value)
            else:
                value = str(value)
            return value
        except Exception as e:
            import traceback
            logger.error("CommonUtils-type_cast_value-exception: %s, %s", e, traceback.format_exc())
            return value

    @staticmethod
    def get_name_from_display_name(display_name):
        """
        Get queryable name from display name
        :param display_name:
        :type display_name:
        :return:
        :rtype:
        """
        import re
        remove_special_chars = display_name.translate({ord(c): " " for c in r"!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
        return re.sub(' +', '-', remove_special_chars).lower()

    @staticmethod
    def generate_booking_id():
        timestamp = int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())
        return ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ'.lower()) for i in range(3)) + str(timestamp)
