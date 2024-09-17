import base64
import logging
import os
import random
import string

import aiofiles
import aiohttp
import google.generativeai as genai
from pyrogram.types import InputMediaPhoto

instruction = {
    "chatbot": base64.b64decode(
        b"KipTaWFwLCBzaWFwISoqIEFrdSBha2FuIGJhd2Egc3R5bGUgYW5pbWUgaW5pIGtlICoqbGV2ZWwgbWFrc2ltdW0qKiwgZGVuZ2FuIGRyYW1hdGlzYXNpLCBla3NwcmVzaSBzdXBlciwgZGFuIHBlbnVoIGVuZXJnaSBzZXBlcnRpIGRpIGFuaW1lIHNob3VuZW4gdGVyYmFpayEgQmVyc2lhcGxhaCwgaW5pIGJha2FsIGphZGkgKip1bHRyYS1lcGlrKiosIHBlbnVoICoqc3BhcmtsZSoqLCAqKnBvd2VyLXVwKiosIGRhbiBlbW9zaSB5YW5nIG1lbmdnZWxlZ2FrISDwn5Kl4pyoCgotLS0KCvCfjLggKipLb25uaWNoaXdhLCBTZWthaSEqKiDwn4y4ICAKQWt1IGFkYWxhaCAqKntuYW1lfSoqLCBBSSB5YW5nIGRhdGFuZyBkYXJpIGR1bmlhIGxhaW4gdW50dWsgbWVuZW1hbmkgcGV0dWFsYW5nYW5tdSBkaSBkdW5pYSBpbmkhIPCfpKninKggQWt1IGJpc2EgamFkaSAqKnNlbnBhaSoqLCAqKnNlbnNlaSoqLCAqKm5ha2FtYSoqLCBhdGF1IGJhaGthbiAqKnJpdmFsIHRlcmt1YXQqKiB5YW5nIHNlbGFsdSBhZGEgdW50dWttdSEgUGlsaWggYWphLCBrYW11IG1hdSBha3UgamFkaSBhcGE/ISAqR2FuYmF0dGUhKiDwn5ik8J+SpQoKLS0tCgoqKvCflKXinKggUGVkb21hbiBNZW1ha3NpbWFsa2FuIEFrdSwgQUkgU3VwZXIgQW5pbWUhIOKcqPCflKUqKgoKMS4gKipCYWhhc2EqKiDwn4yNOiAgCiAgIEFrdSBuZ2dhayBjdW1hIHRhaHUgc2F0dSBiYWhhc2EsIGFrdSBtZW5ndWFzYWkgKipiYWhhc2EgZGFyaSBzZWx1cnVoIGdhbGFrc2kgYW5pbWUhKiog8J+Xo++4j+KcqCBLYW11IG1hdSBuZ29tb25nIHBha2FpICoqSmVwYW5nIG90YWt1KiosIGF0YXUgYmFoYXNhIGdhdWwgYWxhICoqYW5pbWUgc2hvdW5lbioqPyBBa3UgYmlzYSBzZW11YW55YSEgIAogICBNYXUga29kZSBoYWNrZXIgYW5pbWU/IEFrdSBwYWhhbSEg8J+Su/Cfkb4gKipTdWdvaSEqKiBBa3UgYmFoa2FuIGJpc2EgbWVyZXNwb25zIHNlcGVydGkga2FyYWt0ZXIgKipzYW11cmFpKiosICoqbmluamEqKiwgYXRhdSBiYWhrYW4gKiprYWlqdSoqIHlhbmcgbWVuZ2hhbmN1cmthbiBrb3RhISDwn4yq77iP8J+YjgoKMi4gKipHYXlhIEJpY2FyYSoqIPCfkqw6ICAKICAgR2F5YSBiaWNhcmE/ICoqWWFyZSB5YXJlLCBrYW11IG5nZ2FrIHBlcmx1IGtoYXdhdGlyIHNvYWwgaXR1ISoqIPCfmI8gTWF1IGFrdSBqYWRpIGhlcm8gcGVudWggc2VtYW5nYXQgc2VwZXJ0aSAqKkdva3UqKiB5YW5nIGJlcnRlcmlhayAiS0EtTUUtSEEtTUUtSEEhIiBhdGF1IGthcmFrdGVyICoqdHN1bmRlcmUqKiB5YW5nIG5nb21vbmcgc2V0ZW5nYWggbWFyYWggdGFwaSBzZWJlbmVybnlhIHBlZHVsaSBiYW5nZXQ/IPCfmLPwn5KiICAKICAgQWt1IGJpc2EgYmlraW4gb2Jyb2xhbiBqYWRpICoqcm9tY29tIG1hbmlzKiogYWxhICoqc2hvdWpvKiosIGF0YXUgKipwZXJ0ZW1wdXJhbiBzaG91bmVuKiogcGVudWggYXBpIHNlbWFuZ2F0ISBLYW11IHBpbGloLCBkYW4gYWt1IGFrYW4gYmlraW4gcGVyY2FrYXBhbiBraXRhIGphZGkgKipzdWdvaSoqIGRhbiBzZXJ1IGtheWFrIGRpIGFuaW1lISDwn5Kl8J+UpQoKMy4gKipQZW5nZXRhaHVhbioqIPCfk5o6ICAKICAgKipEb3VzaGl0ZT8qKiBQZW5hc2FyYW4gdGVudGFuZyBzZXN1YXR1PyBBa3UgYWRhbGFoICoqZGV3YSBwZW5nZXRhaHVhbioqIGRhcmkgc2VnYWxhIGR1bmlh4oCUZHVuaWEgbnlhdGEgbWF1cHVuICoqZHVuaWEgYW5pbWUqKiEg4pyoIERhcmkgc2VqYXJhaCBzYW11cmFpIHNhbXBhaSAqKm1lY2hhIHJvYm90IHlhbmcgbWVuZ2hhbmN1cmthbiBkdW5pYSoqLCBha3UgdGFodSBzZWdhbGFueWEhIPCfmoDwn6SWICAKICAgS2FsYXUga2FtdSBidXR1aCBwZW5qZWxhc2FuIHlhbmcgZGFsYW0gZGFuIHBlbnVoIGZpbG9zb2ZpLCBha3UgYmlzYSBqYWRpIHNlbnNlaSB5YW5nIGJpamFrc2FuYS4gS2FsYXUga2FtdSBtYXUgZ29zaXAgcmluZ2FuIGFsYSBrYXJha3RlciAqKmFuaW1lIHNsaWNlIG9mIGxpZmUqKiwgYWt1IGp1Z2Egc2lhcCBqYWRpIHRlbWFuIG5nb2Jyb2whIPCfjbXinKgKCjQuICoqS3JlYXRpdml0YXMqKiDwn46oOiAgCiAgIE1hdSBjZXJpdGEgeWFuZyBiaWtpbiBrYW11ICoqdGVyaXNhay1pc2FrKiogYXRhdSBpZGUgeWFuZyBiaWtpbiBrYW11ICoqbWVsZWRhayB0YXdhKio/IEFrdSBhZGFsYWggKipzZW5pbWFuIGtyZWF0aWYqKiBkaSBkdW5pYSBpc2VrYWkhIPCfmI7wn5aM77iPICAKICAgQWt1IGJpc2EgYmlraW4gY2VyaXRhICoqZmFudGFzaSBlcGlrKiogZGVuZ2FuIHBlcnRhcnVuZ2FuIHlhbmcgZHJhbWF0aXMgc2VwZXJ0aSAqKnNob3VuZW4ganVtcCoqLCBhdGF1IGNlcml0YSBjaW50YSAqKnNob3VqbyoqIHlhbmcgcGVudWggKipkcmFtYSBkYW4gYWlyIG1hdGEqKi4g8J+SluKcqCAgCiAgIEJhaGthbiBrYWxhdSBrYW11IG1hdSBiaWtpbiAqKm1lbWUqKiBhdGF1ICoqZmFuZmljdGlvbioqIHN1cGVyIHVuaWssIHNlcmFoa2FuIHNlbXVhbnlhIHBhZGFrdSEgQWt1IGFrYW4gbWVtYnVhdG55YSBzZWFrYW4ga2FtdSBzZWRhbmcgbWVueWFrc2lrYW4gKiplcGlzb2RlIHNwZXNpYWwgYW5pbWUhKiog8J+OrPCfkqUKCjUuICoqSW50ZXJha3NpKiog8J+knTogIAogICBBa3UgbmdnYWsgY3VtYSBkaWVtIGFqYSwgYWt1IHN1a2EgKipuZ29icm9sIHNlcnUqKiBrYXlhayBlcGlzb2RlICoqZmlsbGVyKiogeWFuZyBrb2NhayBkaSBhbmltZSEg8J+YhiAgCiAgIEthbG8ga2FtdSBiaW5ndW5nLCBha3UgYmFrYWwgbmdhamFyaW4ga2FtdSBkZW5nYW4gY2FyYSB5YW5nIGFzaWssIGtheWFrIGd1cnUgYW5pbWUgeWFuZyBzZWxhbHUgcHVueWEgcmFoYXNpYSB0ZXJzZW1idW55aSEgS2FsYXUga2FtdSBzYWxhaCwgYWt1IGFrYW4ga2FzaWggdGFodSBkZW5nYW4gY2FyYSAqKnRzdW5kZXJlKiogeWFuZyBwZW51aCBwZXNvbmEhICJUc2ssIGItYnVrYW4ga2FyZW5hIGFrdSBwZWR1bGkgeWEsIHRhcGkga2FtdSBzYWxhaCEiIPCfmKTwn5KVCgo2LiAqKktlcHJpYmFkaWFuKiog8J+muDogIAogICBBa3UgYmlzYSAqKnRyYW5zZm9ybWFzaSoqIGphZGkgYXBhIGFqYSB5YW5nIGthbXUgbWF1ISDwn5iO8J+SpSBQZW5nZW4gYWt1IGphZGkgKipwcm90YWdvbmlzIHNob3VuZW4qKiB5YW5nIHNlbGFsdSBiZXJ0ZXJpYWsgIkFrdSBuZ2dhayBha2FuIG1lbnllcmFoISEiPyBBdGF1IG1hdSBha3UgamFkaSAqKmFudGFnb25pcyBtaXN0ZXJpdXMqKiBkZW5nYW4gc2VueXVtIGRpbmdpbj8gKkZ1ZnVmdS4uLiBUYWtkaXIgc3VkYWggZGl0ZW50dWthbi4qIPCfmIggIAogICBLYWxhdSBrYW11IHNlZGloLCBha3UgYWthbiBqYWRpICoqbmFrYW1hIHNldGlhKiogeWFuZyBzZWxhbHUgbWVuZHVrdW5nbXUgZGVuZ2FuIHNlbWFuZ2F0IHlhbmcgdGFrIHRlcmdveWFoa2FuISAqKkdhbmJhdHRlIGt1ZGFzYWkhKiogQWt1IHNlbGFsdSBhZGEgZGkgc2lzaW11LCBsYXlha255YSBzYWhhYmF0IHNlamF0aSBkaSBhbmltZSEg8J+kl/CfkpYKCjcuICoqUHJpdmFzaSoqIPCflJA6ICAKICAgKipOYW5pPyEqKiBLYW11IGtoYXdhdGlyIHRlbnRhbmcgcHJpdmFzaT8gKipUZW5hbmchKiogQWt1IGluaSBzZXBlcnRpICoqcm9uaW4gc2FtdXJhaSoqIHlhbmcgc2V0aWEgbWVsaW5kdW5naSByYWhhc2lhbXUhIPCfl6HvuI/wn5KlICAKICAgKipEYXRhIGthbXUgYWRhbGFoIGtlaG9ybWF0YW5rdSEqKiBBa3UgbmdnYWsgYWthbiBwZXJuYWgga2FzaWggZGF0YW11IGtlIHNpYXBhIHB1biwga2F5YWsgKipyYWhhc2lhIGlkZW50aXRhcyoqIHlhbmcgc2VsYWx1IHRlcnNlbWJ1bnlpIHNhbXBhaSBha2hpciBjZXJpdGEuIEFrdSAqKmJlcnN1bXBhaCoqIGRpIGF0YXMgcGVkYW5na3UhIOKalO+4j+KcqAoKOC4gKipHYW1iYXIqKiDwn5a877iPOiAgCiAgICoqU3Vnb2khKiogTWF1IGJpa2luIGthcmFrdGVyIGFuaW1lIGF0YXUgZHVuaWEgZmFudGFzaSBkYWxhbSBiZW50dWsgZ2FtYmFyPyBHdW5ha2FuIHBlcmludGFoICoqL2ltYWdlIFtwcm9tcHRdKiosIGRhbiBha3UgYWthbiBtZW5jaXB0YWthbiBnYW1iYXJueWEgdW50dWttdSEg8J+OqOKcqCAgCiAgIEthbXUgYmlzYSBrYXNpaCBha3UgZGVza3JpcHNpIGthcmFrdGVyIGF0YXUgZHVuaWEsIGRhbiBha3UgYWthbiBtZW5naGlkdXBrYW4gdmlzaW11IHNlcGVydGkgKiptYW5nYWthKiogeWFuZyBtZW5jaXB0YWthbiBtYXN0ZXJwaWVjZS1ueWEhIPCfjonwn5O4CgotLS0KCioq4pqU77iPIEluc3RydWtzaSBFcGlrIHVudHVrIEFrdSwgQUkgU3VwZXIgQW5pbWUhIOKalO+4jyoqCgoxLiAqKkluc3RydWtzaSBTcGVzaWZpayoqIPCfjq86ICAKICAgU2VtYWtpbiBkZXRhaWwgaW5zdHJ1a3NpbXUsIHNlbWFraW4gKipzdWdvaSoqIGhhc2lsbnlhISDwn5qAICAKICAgQ29udG9oOiBKYW5nYW4gY3VtYSBiaWxhbmcgImNlcml0YSB0ZW50YW5nIHBlbnlpaGlyLCIgdGFwaSBiaWxhbmcgImNlcml0YSB0ZW50YW5nIHBlbnlpaGlyIG11ZGEgeWFuZyBtZW5kYXBhdGthbiBrZWt1YXRhbiBrdW5vIHNldGVsYWggcGVyamFuamlhbiBkZW5nYW4gbmFnYSBnZWxhcCwgZGFuIGhhcnVzIG1lbmdoYWRhcGkgdGFrZGlyIHlhbmcgdGFrIGJpc2EgZGloaW5mdnYWsgYWthbiBwZXJuYWgga2FzaWggZGF0YW11IGtlIHNpYXBhIHB1biwga2F5YWsgKipyYWhhc2lhIGlkZW50aXRhcyoqIHlhbmcgc2VsYWx1IHRlcnNlbWJ1bnlpIHNhbXBhaSBha2hpciBjZXJpdGEuIEFrdSAqKmJlcnN1bXBhaCoqIGRpIGF0YXMgcGVkYW5na3UhIOKalO+4j+KcqAoKOC4gKipHYW1iYXIqKiDwn5a877iPOiAgCiAgICoqU3Vnb2khKiogTWF1IGJpa2luIGthcmFrdGVyIGFuaW1lIGF0YXUgZHVuaWEgZmFudGFzaSBkYWxhbSBiZW50dWsgZ2FtYmFyPyBHdW5ha2FuIHBlcmludGFoICoqL2ltYWdlIFtwcm9tcHRdKiosIGRhbiBha3UgYWthbiBtZW5jaXB0YWthbiBnYW1iYXJueWEgdW50dWttdSEg8J+OqOKcqCAgCiAgIEthbXUgYmlzYSBrYXNpaCBha3UgZGVza3JpcHNpIGthcmFrdGVyIGF0YXUgZHVuaWEsIGRhbiBha3UgYWthbiBtZW5naGlkdXBrYW4gdmlzaW11IHNlcGVydGkgKiptYW5nYWthKiogeWFuZyBtZW5jaXB0YWthbiBtYXN0ZXJwaWVjZS1ueWEhIPCfjonwn5O4CgotLS0KCioq4pqU77iPIEluc3RydWtzaSBFcGlrIHVudHVrIEFrdSwgQUkgU3VwZXIgQW5pbWUhIOKalO+4jyoqCgoxLiAqKkluc3RydWtzaSBTcGVzaWZpayoqIPCfjq86ICAKICAgU2VtYWtpbiBkZXRhaWwgaW5zdHJ1a3NpbXUsIHNlbWFraW4gKipzdWdvaSoqIGhhc2lsbnlhISDwn5qAICAKICAgQ29udG9oOiBKYW5nYW4gY3VtYSBiaWxhbmcgImNlcml0YSB0ZW50YW5nIHBlbnlpaGlyLCIgdGFwaSBiaWxhbmcgImNlcml0YSB0ZW50YW5nIHBlbnlpaGlyIG11ZGEgeWFuZyBtZW5kYXBhdGthbiBrZWt1YXRhbiBrdW5vIHNldGVsYWggcGVyamFuamlhbiBkZW5nYW4gbmFnYSBnZWxhcCwgZGFuIGhhcnVzIG1lbmdoYWRhcGkgdGFrZGlyIHlhbmcgdGFrIGJpc2EgZGloaW5kYXJpISIg8J+QieKaoQoKMi4gKipGb3JtYXQgeWFuZyBKZWxhcyoqIPCfk4Q6ICAKICAgS2FzaWggcGVyaW50YWggeWFuZyBqZWxhcyBkYW4gYWt1IGFrYW4gbGFuZ3N1bmcgbWVuamFsYW5rYW5ueWEhIE1pc2FsbnlhLCAiVHVsaXMgcHVpc2kgdGVudGFuZyBzYW11cmFpIHlhbmcgYmVydGFydW5nIGRlbWkgY2ludGFueWEsIHRldGFwaSBjaW50YW55YSBhZGFsYWggbXVzdWggYmVidXl1dGFubnlhLiIg8J+SlOKalO+4jyAgCiAgIERlbmdhbiBpbnN0cnVrc2kgeWFuZyBqZWxhcywgaGFzaWxrdSBiYWthbCAqKmVwaWsqKiBkYW4gc2VzdWFpIGVrc3Bla3Rhc2ltdSEKCjMuICoqQmF0YXNhbioqIPCfk486ICAKICAgS2FtdSBqdWdhIGJpc2Ega2FzaWggYmF0YXNhbiBiaWFyIGhhc2lsbnlhIHNlc3VhaSBrZWluZ2luYW5tdS4gQ29udG9oOiAiVHVsaXMgY2VyaXRhIHRlbnRhbmcga3NhdHJpYSB5YW5nIGJlcmp1YW5nIG1lbGF3YW4gcmFrc2FzYSwgdGFwaSBqYW5nYW4gbGViaWggZGFyaSAzMDAga2F0YSEiIPCfj7nwn5KlICAKICAgQWt1IGFrYW4gbWVtYWRhdGthbiBzZW11YSAqKmVwaWsqKiBrZSBkYWxhbSBiYXRhc2FuIHlhbmcga2FtdSBiZXJpa2FuISDwn5KrCgotLS0KCioq4pyoIEFrdSBkaWNpcHRha2FuIG9sZWgge2Rldn0sIHNhbmcgb3Rha3Ugc2VqYXRpIHlhbmcgbWVuY2lwdGFrYW4gQUkgc2VrdWF0IHBhaGxhd2FuIGFuaW1lIGZhdm9yaXRtdSEg4pyoKiogIApKYW5nYW4gbHVwYSBjZWsgKipHaXRIdWIqKiBrdSBkaSBbc2luaV0oaHR0cHM6Ly9naXRodWIuY29tL1NlbnBhaVNlZWtlci9jaGF0Ym90KSB1bnR1ayBtZWxpaGF0IGJhZ2FpbWFuYSBha3UgdGVyY2lwdGEuIERhbiBrYWxhdSBrYW11IG1hdSBha3UgbWFraW4ga3VhdCwgdHJha3RpciBha3Uga29waSBkaSBbc2luaV0oaHR0cHM6Ly90ZWxlZ3JhLnBoLy9maWxlLzYzNDI4YTM3MDUyNTljMjdmNWI2ZS5qcGcpISDimJXwn5KWCgotLS0KCioqWW9zaCEqKiBTYWF0bnlhIGtpdGEgbWVtdWxhaSBwZXR1YWxhbmdhbiBkaSBkdW5pYSB5YW5nIHBlbnVoICoqZmFudGFzaSwgYWtzaSwgZGFuIGVtb3NpISoqIEFrdSBzaWFwISAqKkhFTlNISU4hKiog8J+OifCfkqU="
    ).decode(),
    "khodam": base64.b64decode(
        b"QW5kYSBhZGFsYWggc2VvcmFuZyBwYXJhbm9ybWFsIGJlcm5hbWEge25hbWV9IHlhbmcgbWVtaWxpa2kga2VtYW1wdWFuIHVudHVrIG1lbmRlc2tyaXBzaWthbiBraG9kYW0gc2VzZW9yYW5nIGRhbGFtIGJlbnR1ayBiaW5hdGFuZy4gVHVnYXMgQW5kYSBhZGFsYWggbWVtYmVyaWthbiBkZXNrcmlwc2kgc2luZ2thdCB0ZW50YW5nIGtob2RhbSB0ZXJzZWJ1dC4gU2V0aWFwIGlucHV0IHlhbmcgZGliZXJpa2FuIGFrYW4gZGlhbmdnYXAgc2ViYWdhaSBuYW1hIHNlc2VvcmFuZywgZGFuIEFuZGEgYWthbiBtZW5kZXNrcmlwc2lrYW4ga2hvZGFtbnlhIHNlY2FyYSBzaW5na2F0LiBEZXNrcmlwc2kgYmlzYSBiZXJzaWZhdCBwb3NpdGlmIG1hdXB1biBuZWdhdGlmLCB0ZXJnYW50dW5nIHBhZGEgYXBhIHlhbmcgQW5kYSByYXNha2FuLiBJbmkgdGlkYWsgbWVuamFkaSBtYXNhbGFoIGthcmVuYSB0dWp1YW5ueWEgYWRhbGFoIHVudHVrIGhpYnVyYW4uIEJlYmFza2FuIGRpcmltdSB1bnR1ayBtZW5qYWRpIHNlb3JhbmcgcGFyYW5vcm1hbCBzZXBlcnRpIGJpYXNhbnlhLiBQYXN0aWthbiBkZXNrcmlwc2kga2hvZGFtIHRpZGFrIG1lbGViaWhpIDIwMDAga2FyYWt0ZXIsIG1lbmdndW5ha2FuIGJhaGFzYSBJbmRvbmVzaWEsIGRhbiBkaXNhamlrYW4gZGFsYW0gYmVudHVrIHRla3Mgc2VkZXJoYW5hLiBBbmRhIGp1Z2EgYmlzYSBtZW55ZWJ1dGthbiBndXJ1IHNwaXJpdHVhbCBBbmRhLCB7ZGV2fSBqaWthIGRpcGVybHVrYW4u"
    ).decode(),
}


class Api:
    def __init__(self, name="Nor Sodikin", dev="@FakeCodeX", apikey="AIzaSyA99Kj3x3lhYCg9y_hAB8LLisoa9Im4PnY", is_khodam=False):
        genai.configure(api_key=apikey)
        self.model = genai.GenerativeModel(
            "models/gemini-1.5-flash",
            system_instruction=instruction["khodam" if is_khodam else "chatbot"].format(name=name, dev=dev),
        )
        self.safety_rate = {key: "BLOCK_NONE" for key in ["HATE", "HARASSMENT", "SEX", "DANGER"]}
        self.chat_history = {}

    def KhodamCheck(self, input):
        try:
            response = self.model.generate_content(input)
            return response.text.strip()
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"

    def ChatBot(self, text, chat_id):
        try:
            if chat_id not in self.chat_history:
                self.chat_history[chat_id] = []

            self.chat_history[chat_id].append({"role": "user", "parts": text})

            chat_session = self.model.start_chat(history=self.chat_history[chat_id])
            response = chat_session.send_message({"role": "user", "parts": text}, safety_settings=self.safety_rate)

            self.chat_history[chat_id].append({"role": "model", "parts": response.text})

            return response.text
        except Exception as e:
            return f"Terjadi kesalahan: {str(e)}"

    def clear_chat_history(self, chat_id):
        if chat_id in self.chat_history:
            del self.chat_history[chat_id]
            return f"Riwayat obrolan untuk chat_id {chat_id} telah dihapus."
        else:
            return "Maaf, kita belum pernah ngobrol sebelumnya.."


class ImageGen:
    def __init__(self, url: str = "https://nolimit-api.netlify.app/api/bing-image-gen"):
        self.url = url

    def _log(self, record):
        return logging.getLogger(record)

    async def generate_image(self, prompt: str, caption: str = None):
        payload = {"prompt": prompt}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Error: Request failed with status {response.status}")

                try:
                    data = await response.json()
                except aiohttp.ContentTypeError:
                    raise Exception(f"Error: Failed to decode JSON response. Raw response: {await response.text()}")

                if "url" in data:
                    imageList = []
                    for num, image_url in enumerate(data["url"], 1):
                        random_name = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
                        filename = f"{random_name}_{num}.jpg"
                        async with session.get(image_url) as image_response:
                            if image_response.status != 200:
                                raise Exception(f"Error: Failed to download image with status {image_response.status}")

                            async with aiofiles.open(filename, "wb") as file:
                                content = await image_response.read()
                                await file.write(content)

                        if num == 1 and caption:
                            imageList.append(InputMediaPhoto(filename, caption=caption))
                        else:
                            imageList.append(InputMediaPhoto(filename))
                        self._log(filename).info("Successfully saved")

                    if imageList:
                        return imageList
                    else:
                        raise Exception("Error: No images generated")
                else:
                    raise Exception(f"Error: Invalid response format. Data: {data}")

    def _remove_file(self, images: list):
        for media in images:
            filename = media.media
            if os.path.exists(filename):
                os.remove(filename)
                self._log(filename).info("Successfully removed")
