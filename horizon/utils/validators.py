# Copyright 2012 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import re

from oslo_utils import netutils

from django.core.exceptions import ValidationError
from django.core import validators
from django.utils.translation import ugettext_lazy as _

from horizon import conf


def validate_port_range(port):
    if not netutils.is_valid_port(port):
        raise ValidationError(_("Not a valid port number"))


def validate_icmp_type_range(icmp_type):
    if not netutils.is_valid_icmp_type(icmp_type):
        if icmp_type == -1:
            return
        raise ValidationError(_("Not a valid ICMP type"))


def validate_icmp_code_range(icmp_code):
    if not netutils.is_valid_icmp_code(icmp_code):
        if icmp_code == -1:
            return
        raise ValidationError(_("Not a valid ICMP code"))


def validate_ip_protocol(ip_proto):
    if ip_proto < -1 or ip_proto > 255:
        raise ValidationError(_("Not a valid IP protocol number"))


def password_validator():
    return conf.HORIZON_CONFIG["password_validator"]["regex"]


def password_validator_msg():
    return conf.HORIZON_CONFIG["password_validator"]["help_text"]


def validate_CHN_id_no(id_no):
    CHN_ID_NO_PATTERN = re.compile(u"(^[1-9]\d{5}(18|19|([2-9]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|(^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{2}$)")
    return bool(CHN_ID_NO_PATTERN.match(id_no))

#YYYY-MM-DD
def date_validator():
    return u"((^((1[8-9]\d{2})|([2-9]\d{3}))-(10|12|0?[13578])-(3[01]|[12][0-9]|0?[1-9])$)|(^((1[8-9]\d{2})|([2-9]\d{3}))-(11|0?[469])-(30|[12][0-9]|0?[1-9])$)|(^((1[8-9]\d{2})|([2-9]\d{3}))-(0?2)-(2[0-8]|1[0-9]|0?[1-9])$)|(^([2468][048]00)-(0?2)-(29)$)|(^([3579][26]00)-(0?2)-(29)$)|(^([1][89][0][48])-(0?2)-(29)$)|(^([2-9][0-9][0][48])-(0?2)-(29)$)|(^([1][89][2468][048])-(0?2)-(29)$)|(^([2-9][0-9][2468][048])-(0?2)-(29)$)|(^([1][89][13579][26])-(0?2)-(29)$)|(^([2-9][0-9][13579][26])-(0?2)-(29)$))"

def phone_validator():
    return u"^((\+)|(00))?[0-9]{3}[0-9]*$"

def validate_port_or_colon_separated_port_range(port_range):
    """Accepts a port number or a single-colon separated range."""
    if port_range.count(':') > 1:
        raise ValidationError(_("One colon allowed in port range"))
    ports = port_range.split(':')
    for port in ports:
        validate_port_range(port)


def validate_metadata(value):
    error_msg = _('Invalid metadata entry. Use comma-separated'
                  ' key=value pairs')

    if value:
        specs = value.split(",")
        for spec in specs:
            keyval = spec.split("=")
            # ensure both sides of "=" exist, but allow blank value
            if not len(keyval) == 2 or not keyval[0]:
                raise ValidationError(error_msg)

# Same as POSIX [:print:]. Accordingly, diacritics are disallowed.
PRINT_REGEX = re.compile(r'^[\x20-\x7E]*$')

validate_printable_ascii = validators.RegexValidator(
    PRINT_REGEX,
    _("The string may only contain ASCII printable characters."),
    "invalid_characters")
