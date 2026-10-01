#!/usr/bin/env python3
"""
🚀 Agent Docs-as-Code Harness Installer
=======================================
Autonomous, zero-dependency installer bringing Docs-as-Code discipline,
Obsidian graph integration, knowledge base linter, and 3-mode AI agent guardrails
to any project in a single command.

Usage:
    curl -sSL https://raw.githubusercontent.com/koudinie101-png/agent-docs-harness/main/install.py | python3
    python3 install.py [options]

Zero external dependencies (requires Python 3.8+ stdlib only).
"""

import sys
import os
import re
import json
import zlib
import base64
import shutil
import argparse
import subprocess
from datetime import date
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Python version check
if sys.version_info < (3, 8):
    print("❌ Error: agent-docs-harness requires Python 3.8 or newer.")
    print(f"Current version is: {sys.version.split()[0]}")
    sys.exit(1)

# --- BEGIN_EMBEDDED_ASSETS ---
EMBEDDED_ASSETS_B64 = "eNrdvQt3HFV6KPpX9si5uNvT3ZIsDEwHk8iSDLr4oSMJGI6kqy51l6Qat7p6qrpla2ytZSDMJJdJYIB1mcVkeK0kk3XOTZYwNgiDzV+Q/gJ/4M5PuN9rv6qqu2Uzk5wckrGqq/b+9uvb3/vb++bYxMT6crjTbQe9MB1fnru8cGl6eW59enaxttMaq6uxarW62oladQWvqj+F/1Y7vajXDutqdWzl6PdHB0dfHd2Bfx8cHR7dU0cHx7eP3zw6PH796N7R/ePXj984vg2fHh59cfRQweO947+FD1D2+O211bHVTtoLev20roJmM+z2wpY6pbpJ3I1TeLxl395SSfizsMmPrbCbhM2Af6T9bphA6bC12mnBu7o6O3H2qerET6pnnwLw5uv6xh72GNvsBVtpfbWjVFUFrUQekuZ21IMW+km42qExr3ZOmTHXVX6o2dFAhefUmTNHn8LYD2jkr9XPnIGKH0PJw6MHx2/Dh4fQ5aOP4OH+0TcwKw+o+sM1eAs138d6RwdYyw5CKYT77I+qVQUFvjl+Wx09pPrYmwfHbx2/6fXk6Gul51RPWUXBB7/vq2PSCXhN8Gq12uqYqlafw2Ho4Z9SkzV19CH2U9bztePX1dGhOvoOmnx49DmM4d7Rt0cHqx3u3zuFi38AfYYH7sEh1IFmKwo+Q7cBxkPdLxwawAZcodL45ld6eqFJqIjT+jfQ3dtH3x6/pXsL3TwL3fzEmYN7ukN/gJc0TOyCrvkGQDqkAdzBTzwas0AFmKqo19C1O/D29tFd+HkfJ8Kuw4HTmakarzAX/gLgvgHdfgs3xx3cHlD7ACcURlBa1Fg93e6FSSfoRbthWl7tnAF0WDl6B5b71ziZMo2vQ1UAoSbXEEV4hIRcME/Y/7d0lyxqYe9LVOQ1eH8I0/4aff0S0Q6X8/jXgh5Y6wDG9oC6iisAn9+EoneP3yrz8Ib36uyj9cpO2JMwYR9jbwid7mKvEFGO3+YW4ds3x/8Ab9/y4d8D6LCYx38HPeEqB9l1M70++kfqyhsIRY0zTn8rWPwtTo4P/reEqgyW52MAVlIDYxU1iIouzrwwvzw3s/zS4lyOnMK36khyep87qmcOyUOGbiLKAIy9LoDwqVgzCZFIWoo4+ZPVTr/byr90KaIHAt80451u3Ak7PYcu/vHjt3/3/x2+XbzjD4qoZfFIBtLMdxAaIdYDppnvaqJzj7/I/mXwh0JAfwu/7jKhIjArtdo4rMx8pxXeuKUf1taQpGap3HtmdX+pMRYx4HVBLVxw2TFHh5q68BhxD/xKE57CcSJZO/4VUX/aat/S3hGQSvYm4jiDwVdIlu8RKYIWHtIu8snd+0RGGCe/RRqM1AUIEW4K3LRQ+2t3JzUajZ0w2Qki4JOb7fh6cztIemp5FtdYqZl2BAu8AmzhQ6R03HHYKC/Nr46tYctqKUx2o2aIRT6l7t+hfuPu+FoTla+hMMOT0lyzFyfBFtX8Zz3JRIFh4+Je/M3R+1QPeuhQ0N8yzwH0+hsZylvEHe4zNyJAiHBv6cX40MzgHd6xRNB4Z1cUbf8MPCKGh0ihBfduYxvfEsvAGQT8ylCpj44+p4Y/16QfEeVvAQZysfvSk8Wwl+xVCQO+oZ1xyAwPFxXfAZv5JREPaP1zQug7yA0B7Ne4jswtRlGWCy89nyUo8CpHTz4kOv46zdq9vBjAPdCiWLgbJlEPxKSd4GdxApLYRjtuXgsT2FtN+BA1gzY88kf4G3ViEJ4MdahraoF0Q5OnTngd4OC/t1TUAd7Wi7aAyXW2EGbc2YySHZLiok4VxL6tJExT+LUZ3aC31+NOD55XO0lIn6K4sw6z0MOx4d90vBv0tsd78Tj+WrelauGNHg7psSjgRn9rtXMt6GwEHZpEJCIv0s9bgGQ4dZ/jv1XEENq5B2s0fw5xfOcj3KD3CNUASc3aqO9vv69GrYqhivOzSMR0VSJwHxJffZ14kGHgROouy7JcxmURcpijqr9HnKYdSxTVweV7+Oa3MJzv6OUdYsUP1lj4xIbtwA1lLZiUYtr6KRGl72hbfSv7GPYL7Lc3QBAxIhsxaq+s5ch/IOopdAZ2Cf6F0f9aaALQAqR/D2UAD2mv3aFdfEg03JUFPso2bZv56OjTioh5SBuO30YawcwtQ3//Fakvy4TZVu8R9RXZaxGUlRhoYNhFuQ5mwxVg7uLS0JDu0H6kJs7WjLTv0HCmlfdl9MjmROac0sU/EkqEZGk3xbF8Cb+hHMnohGnfUUumf7pFQ3SFqVhOR8BKR78jsRikR0IpmIyqSO/QvTJR7h7uOKHEn1lV4aHp06ERonG4X3DDluSzDMh85SEL5Cw+YvuLcdxTM0E/DdV0J2jvpVFKO2lxZro8WvXw2mXpjbctaRVeSzgxetN6Mv056h4KyA+YX3vbRMuqjZXLV2fnL7661lANTZk2o3aI5KhBPea+FgDQS4FArsy9ghBGUjgHJC3GFyT9vkZMDaUP4c2vsyDrjOYpGM27NNmHMFpaZGFJgK66herFKEl7ML9VtaLWcPioHRwAj/070jJP0uTgLelNNTQ7N1uumaZ+Wzg/oqZ9Sy9ETrrDWwJg2dqfnKBfosshAcF/YFCvi3wpKg+ogoo253ekUGBjpecX5+auON38kIwdQJcAf+7nsYeq3qbNdw9lHcawO6oxC/yyofinQztxiIeKZLjvCEUObI1wtx1vAcNv1IYJBbNzL1+6mpML+K0RC47+H703jr4RtdyTaQ5ViZsrD9IyWvT5MbmrrozPP4v7oPO2Pdb53u8fqYfCnj4jYfkQCfkpbkGdEuiGhX2icQ/KogZraMBXIpKTRMfcbaDSQCLsQ7JoZekJboqjL0d1HYpqxPxamJcjtx6/yWKiRXIoVvM46im18ir8V718uTo7u0Yk4OgD2irItIwFRC1PL71YHWC6oiHfJb3lcA3xGabHcFhkDkTpjh7CZPBKDRCxM10VA85dMg3ZzftAy+MZxUhLuVVenXswV2+IbeGAvooJxSNStMhup94F6ERWzPYmwZ0pvpH6kY3M3Yh6IHW2QjVRdlr+VMwOb1jS9rfIBTPt+MUM4vAsHmguQxv+G9LfRkjw81dm536a3auIbvjeEeJBP2ILE6uajBKFi/qxox8PsxJs9zcec/OCKIP2Kv4R4b7w9u4fPlGP3VtjCSCy+cssZzJC59LC3Mwt/Aembk3k3I+IhD4U09wDWjoofbWzEQdJC7SNW/kieUn1jx9/cJ9sGpquH2irJe8IwCosOVyRJmIBqq6mGyA8/TPu/7LWo22nVlC3GNFHo1AzMAQwnTS3sQEUrAutLwV1loP0WoqVUHL9wO79IvCzi1gQpEF4Kvi+GKZhIF1Aoe23RMxoa7iW3KJOoPZHw55Aceoz2ay+JedeQUUm9jRd/HjL5RAySVyJBkqVWDmhShNn1+l9scJiGrR1F+OgtRN0/cry8hYIyQ+py19q+fK+xhcBJlKti1nvvY5yicEloG3Hb2ZsIQeinRC6sDFyJHpUVOGUFHIeLp3bQTVutjExuT7tmP7GG9iBYqmaDcRoHL5n1LmcWcbA1fPXEM46dDEq6lFnvKIaC+2gA/DhaakbNvnpQn+LHxbDdhikQHgbpkdT67NhM0IZN0U/lwwVGRBh5PHtrEOl1NB+oEbZQHlyXW8FATBgJ9D0fE4c71dk37nNIkxjcW5pThuBHbjn1mWjCNg/kL5FSPIacUXD5rydAw3NnZ1TL/3UAHK5DoP6UFo/EMPdPeZ0n7NlntZsML96cfrKhekrLsNiG0m12+5vRZ262gjSqOnLcm+pARYT35h7UCjH9Wg/nuJW1CnoT6eDliNlOMWd47eJBz/QeHF3IKIw8p0Io5gv8Lb9Z2Box38vvosvVOlC0LymBU8q8/3bX+QsKaX5jloQa5ZT8h9BtnuPiuCigT6BegB9B33ixhqZPNH8TDo4iRBGLaP5+wq3msNV1WzcTKtBWp1BkaZkhcIyyMDwyYzi3U8RNhKeQ0JGmGAUw2hTI9DSfDPciG/oroBqo83bhF2sQqNuY3VpDwRryupU1AqDYRh09cqFq9OLs/NXciqK/WLVlE9AGLzPU2V8Qg/JhKFIhPRI4fEbqmRppXq+D30p/+nln9g0wb+3sB3Ra2QxUL70NsGHt3/QWKyOU+BtoF39mVVA77D2yrroN8btarGTLB33jYCMth72UcCberHz/kA1cGxITKdYvP2StPADQ/fFIAX0I7c3DweqU5U/Cy8YICHUcjZJb++8HPTbPSSbVnr9knxP98iGgQuFOvl92NsyFzwRqMt8RdP1kNSUt2HhNtKoFQG9IphM1UFFeQ0l3rtk9HyDNSZWcMicQdaHV6cvX1KbSdzp7QS9Xpgo1hUNiUPCT74M9p+j19Kd2OvRtagdda6lhqMvoJBKrwhL/on8Cyh5AMJ8UBF/Oimyd4RFITbQrwdsK3StF2j3YTsqm2FY+UE76ltkJzyUVqdh/1bnmtsxiw8av1iZw9m6Q7ZvAegMCbAeoE59f/u9c9jEG9CJ+6LKUTe+Ov4H7AqC+VareYqsm6hTHqB3nwaINTLLDUJvBnOL5CMsfIvFACqGBvHPyOL0BY4CpAKM3Mh7gdl0/i7q7qSF3kIwdWhdFf/Bz2fO/PHjjz91G5usGwMjTNwt1Ri/tlFFltcgFWdxbnq2evXKpVdBn/gNzoa2ex2UuThQ2CsoSKCNqOJxXdXI8bGG04tP3F6crRN22B4gDz5hD7S9oagHBVzS7cNnbh+m6uyev2t7EQErCXfCTg+7giZoogBfGBIKXcYPVKti5CNy+x0Awr1OiOdiK/DoBsBF31U77IWNMnbGRZkp8lpoG+RD8rYcoo/BoXeCMB96JvlbxV7hPFLgCx5cJ4JxjfMPYTA0zsHiAEupyFOM23Jc5fUDpxHGpHF/UV30g1UV9CsjLAcl4AvMb9ntsV0OgWgm0oc6BXVpUQjmP7GRPSvaOKYop42ExXYDkCrVtcPyNntUl16Yrp499xQvuTfejf6W6VzQSsxzIiI7wX3ftUAvo9w0ngkjQh0YXxaK9npZCTAQWsbOd2BZ2MJtaNtDRJxDj7hn0O3JQbo8s7fX2d8l5FlYEPkKfCGfjIGTU8ITraCPIWKOoC8kEqtnlT42Jw7oCjGkQ/GHfeua9fKan6P3EUzm8BWtWlcUK22whqSyVRQpbPBdq2sCJaerDe6hCVxyI4C04ibgXKWNIT2a1ubqbALS0dcY4qeA2WTsJ+ZxqP0W5IRjty2HmJ1AjXMM/9ihhmb39IIa87T+vGlZG7IcGzdiY+ny1ZlyhkueE6fQ677ThRcdpuFNMXw7m5dZ/nLS71yrXggwZBPFKuT8WkxCdN0Jok6jpsQbfRvd4Y2tqKe6/XYbFIck3MCNLvLDRZDKARPVhSToNLdDll0+JGL3nV7hv2GPHQHfhPLjmvU0JLwNuqYDHH4lUsxXyiP40tpsP2hXL6MIuLTXaWJbi+FO3AtVnESg09IUd/vp9l+qS3ETil7ttPd43mlX46wf/1qcS8IaMJrs9czUsr/tAZmPb9upvYMkwolfcyzQrnoMWmcSX+9sRmG7paZbcbcHu0FiBNkNTeQb2cUdHXFEGGfWqcz2CbSv88Td1/Et2KTWLt8YJNSKtMcGWSIBuBxfD4j1lYAgcZrjGomtSU+69PmsZTlms4l8wv39lDqCEt7XRlrVYinKkl+zzPcVy5be7KIkbvleWfx9D8hR4+wL1psIkVx5xe8nMrH3iez9kpTeb8RX7ImUMJXc6XeJkBz6bI35tSuyECz0/Lzh8mdQoh0GrX9ZdjvUPoMSYFav1lLh6BjDB0S0vmMPi3FmyE7zfAkmPHtQpLYfy6O3nBvDrRVxHPVqp7sN+7+uJh/XJ0FA8GmTaQdADBKYrvUUWIuJ4MkZPnFMPyzKB81bgsF2qiXEJxcsbqbSC+4xtYrjdTDe7DWKVLnrKhufEipRdJvhHA+LQ3qynsGHa46OPtzTMsDZ8oMigQpiyQnxENtKC0m8AZiunlDPx0E7LdvIPpQsiFJ5cedCsUi0gZ9/RfF5tFoPkD7RFAgvNrFS2jBSRLtYISf7FgXvAWn/Skxg7DN+OxMDVLQ84gN0RJDSf3tiWsj1f5u0oUbvSpwLdAxEzGx8PLek1BnxjVqZ1IEApPZzUUeFB31HBiZWRP3QnncG5GWQRu2yTB6AxIvrJfiA8PI2xzwRxpHpf4Bbt5KL1nf8wG4wugmzzcTJHxSFmHshsE/WOD7Ktv4VK0ueSgFiPZBSECbC4FoLeKiJZjHaanWyUTexXzbsIusk1+5iv+7ZR6hrZCwdwncvLx7eZ9T7RiI/SrPxrKNOYeB/2Qk+8Yg2h5PmycIBvB6AztgkRt6IXl9hFuzo9TbSZbDRTTVEomcZFfcm6RciQh4MipbJhwkQG1cNJiUM7U6R7cJC/Bd2y3KUvt3gvAc0Xum9eeDJgmkzibq9FNjrOmpute7ecOa6OHdpbnopF8Mvr6u7Kz+tvVr772uu295orUp/HZREpDVi4i+7YYLaDvEkATrm8kjNhi1fPeXx2FYSbPZ0KpT1Cax2QOReB7aJgHcdyPB6u7+xLvr2ej9p6zSpHZCL8ZlLrI5BQ/wIrbRJHI5BHF7tBEkv2gyaPc2QO8EOSxr6A8aqUVvoZcV4NvzaitLeeHGRNPqFiCrsMqVweft1OwCdn76L/r+WSeqSsUg88nbQ2Qop5OgxuH3CyG3qnNAJnHcAnAQZbBDEuzYAFcm9rsMM+J/YRk3M90o+c8yuOX1ahiVHhUzDaBj+//4IZ9lJh5uPo0DBCFnxV1jLQ3HD0r0IaN/A6wREsZT/Sz/7QlH00XcUnXffi9Lkuf6DTrRgfwvK3KUZjQVab/onFsd4pGyDmLiyvoDbzKiT1bTd37qlf62tDSL2NrL4N5SSIXqS9uGTZUOiuBmk/DgBxOnZRVcey5lDtHmD4epfIwDrVfoXlgpeJzOYGG9USTZVWcyb4jdgO5zZjfBTyuGHj4lz//pEpu+Gv+fRZubvczT6mp2NnxsFpKLBFjQax/t/r4OJmOLfZ7OZtkox53vAqPQauV++xayRRqOxEaTbuEcX4uthsrQdtoH2PR/2qhejdvgCfFPV6fZWnADR28Hh4miLyBZAuBR1+jfGd4Lm1aW6UKi0v1NcmsJDhrEaNjHleY01PXn63Gecg6k4ja3IlJVLnfQUOpeTDNDdClQzzK7NqWb40iPEbGvDBA4cZWudfPpA+tbsq6CVyBuHZr7//w40uiLhHDXktcKAAt2dwXrMcIdkkULzsZ8IW+Rf1zQvJyM+JDnt8yx1y63W+PTCvJN1y+rc21YCz/rzfSXlHWt05+SmN6UHX7HdQlkDBVkPq9owqfv9cS5pQEQsxxjMwht2GbWAigJ57YGI9Q+5b5LsayyLFfaxfiWxo2I2ErNIhWM3yZbmDWhKpvxAkgBt7O09a+O87cQk3aX91t3rbceEWkf/Rias70T8/lYbzLKGvLtGFcwYgbNJC5+Kj+iBjSzWcA6cmS8tJ0ErrMabm+py0EuiG5q+vuumBBMx1dmu+MNNW/UUM9L2vWzkk/kdj94ht5peWd0Uxm/ot5+YNvitm65+/JujBwbUb1TJ1UHLIyEXZt3qVj4x2tw98qXJdjaE/tyJ06p1orI3taOSk8Xvf0eyL2nZv7R7lTJnxCbKHhU38y+bW6FDkgURtR8RMcqIQB+7L41ZwguLAlC/13lKirERO3vXRzPnNABiciAF/NWo4OPFq9Ozl6cXcjyGX9sgnCGKX3FgvkiMA2NvRKB+TFufqa0Nfx0TirMDPDvtxZ0w9RiJhPT+gHEUMRL+6MSknbLNF8enacqS4TmjdBADzOZGMc01Lukh5roMu9KKA8UacKCLzgY8/hsKuOBoCs79LV1+eQGF5TOsZnOWIWPue2ShuKNPdvglf7fWeH2KhBNK9oETKY/NP8zywjvEmJjkoAWVjSwTE5NW389DOvsokM42alk95f1/l6Qz5gg25ZzJClLvXJ6XKl3sk4fqBRAMfwFyuBpXJn5Onx4wMNauogz5e4j0S3wphpXfUZq1mW6YaXXsF9ploBUFivFDkufEDOhzGRzCl8k7zU5dTtEaQURwYrMURGtLj5KF7GejuK4G3F7saZCnrHehBTsOBdWg0wTp3XoWUM70PAuFWcriJ0Dgrp+AXdPaNH9LP7Bi/1h0C7szju4IoVzYr8mcQeLRPRC/+4So2yBLvlmNx8k7NnWLXRMfstbuhXOIWJJzQiA/5HT4B1knhPafOFRs4PQPltsfxQUh5MzDOidzFWjHA0ewdCYqc86Da+G1Rn9Otj2wrNyqBr5YPtiiriPZWJAx6aDDEkqLOmjSSU+Uk0qeaDKf5tLPLKTZuUtzy3OjOuOn1FI4zIFDP7MZx/ckvOWwEKH0ynyaP6ghd6IDsrNKUXAU9eABy20VMlIPOcVBd9BXGz7MGKWyYS/5XGbxVxemsKnSy2ESbUbNAH35FAtjLfuf2hCnumrw8P28bycK6rCinLQ27HvDAHpHJFYTDzcAHKecGnuam0ZXUZMTE/+H6gZp6sPOGFw0ZM6cUzj/Eury9bheKA6dpAl4yGzGBjpoQIfSymBvyRcmgt7yKXSU+J6Ru8K9NX8rcMFT1KB2eXxF+/Ab6DX62e5bH4OE7pqA1GPr82V1oWh1ZVBfs8pMEVF6bS0ZzTlLiPtjp0qNPMVslCvZZOESJxJzdIMr4Ap+soCL5VZurDUcb84HembYHeonaz5SwvHy3NJyTgKAdyNjDiiawgRJ5c6CczWGHkdXPS7n1bXxx88DP13xf2SDtQozFfN97RRHuZ/8sCHDg0ije5N9cubMMrZfO6hF7JzkRB2DfSjp43TyBXx8M+9xPYCXPsspOHMCY7hc6Tp3NEaFo8rkuB/rIXeJBHOtN4hnmvOybBr7YYbkZ6Y8TwJKHAFndrQNc7KibPZsjGEee/UXq6u9+C/UGedIDHGlG5PHPSLjv7QcKtP02f/Api0TofAACtnDJvRMfUH0U+cLDnb95NxI5AGSk7L4qDtC3IXppaW5WdBjLk7PX5qbXTOATXisczaak4QgSKgPqDHaQi2WJIjxrSTobtd+lsYdJBE3cReujjXjdjvopmEVhIdemKzCp17SDyv8VSzGY+yF1C+34+vLsKnx9WbQTkPn/XSvFzS3MT4q93k7aoUvdUBViNu7oBsUVL6agCzeSTN9MD2EhzipbiVxv5sDTt+eN59W2Dt5k/9ggZ/3w2SPB4JiUt2kBF9dVPSCiaz5iYq7+WETgGQSGCY1ijBNO/g2wDeTFfdVsrVBL5+amnx68pkJ/WmfH/Yrw3pLLlpjCkf3FXYLfcen8GykH9Sfc089M3Husfpj4mxNZzRt/yEdOnv26WeePvcD5ueHLs+TT/8EvSaP3HzGE/iDujEFKPLUk888Ri9sPPUPnIdzExPnJh9nHvwI9h/Wi8mJqbMT585le4F/1rKkoRWlIA3tZakXEqQkia9n3uPxSBeDVni53+5F3XbEZG9CvnZAeF+KfpH5OlmbPCcF2lGnqEC2T5tx0gxzxAwoY5gs9ZKws9UjwjpROzf5zNOTU2effOYnT09MTZ6VkknYDdtuwckJ2/4174PzfjYCua3TDGk3ndM10mbQDrmxp6Ymnp56+pmJn0zCzj/31E90v9pxGuq+rnb2mXfkA3OQc5z60Xg/TcY3os542NlVrJdNAacc41CVFzvx9XbY2goVhqGjNxaTLGA6CvL8UpBoXw7aEcqNqTJ5cxWiuyq8AcMJYTgVFXRa+aw8hLyFp+QBlP8eJjFUoINb23gqcQjkvdOMAGypn8K/ODEtoOJqgTqsplQ72kiCZE9h5AwF4MsAQHTe6cZJT6V7qXmO7SNaq+QxSLa6QYLhLdCvHYqnAahKvi7AT5Zv5zopmilfWr5YfUbF/V63DxA76pWo04qvp3j6HrBFtJZHm2o7SGF4SQlar6W9FpSuED7QEX1btK/Kdd4NvWSvbveOrVBzSpdgFmLkXedXx/q9zeozsC1VCNsiSc8TmrUDxJcywwlvYOgwqLH4B0OfLHjUOzmBuhVuwgJ1Wuu7uIbrSRz3SjC9SW+9FSV1GnYZI6bxQQA0+4k6r0yhmsgBJWn2+jauNxb60Xn8U2NroNM6TEwJv49juBImVI+Va1GKsEplBbhlPjppGVIGcalUdmCNgpcpiv8lIVC0jvJr+MVsEfueh20HxF+kZOFs6PkltFo3O6IE69nDGYFaie7gKXRfYmIG6DsAayvs3WoHG2Gbk2/5zantMKAjK8wXmCz9cW3NxIHhxoGuJmENzbM4Y8np1dUV+P/Syv+1urq2unrr1NqPy6W/qp/Sv9fOlP8KfsMTvcGf9GHtdNkbp0CvIcoE7bYeijNYGEPzGq3TurO/S/SCY9QIpwqxHqk5dNyUhckMWuv4tgDzB2C5ClIVOjCl4xdJwlSbq2Mzcb/dUp0YN3/QYqlQ3Qz3mVwIPmGbNVrU9HrU2y6tkh4+Vvb2EHyE3nJRYB49XaqizpY9bG+HnRIVL6vnzqupeiGyLSNrAXwkGpojkBpD/eGsjl2O0hRlN8CEnaANlBnP/cxRV97SSJWBXgK9gm6Weby8aEm/Q2wBFgq3g937FbUbJhsxWvs34rgNw6WWiSREZlPDEHUxZ34SKFCCCadIoul+KyIhM8NSAtgGN3WbdvPsryINLxvwuFymFPGS1NvbprHvf/9rNRsBzezFwA5aMWworEtVnJb2cZVw6c8LpQUqWs4hzaTGCED19Z0WYTUueRuAlWynt9rxBqz9GSZTZsN0YyKnUN4U1ZRD7/npdhorFDOgv4oK7wQJRVQrbqskXseKwnjiy3P0OP383JXlJXqcuTT90iy+lVaRNSOcdWgSFgi0pzGBgANeHTNQ+KeBxD8NNP75/Nzl+Svz9HMtQ77t6MZNe4MJtDt9taCL/LwYgp2ZGZkUdAfHm3gGSkgBsBaHUUDopLTjQaCgqKdoNyS+ncpkIB1BAOfVzX07P5s4MW6X/LFt4jA0uPVebBa6nNu37fVunEY3kGTVCmvUgpSLlMp+Xd21FQNkDaGMKlRrY0RdqZwpjBOz3onXhXwCPoc79qsB4xTLACgqkmmLC28k8bWQaMU13AgrwnQcWrN+PUjQde9+Jp4QtrjaejPud7CfExroqEXxmQQBZLYjEz+SR5yETwykY3kS8yF5B+dQ7iIegmTt5ua+cJFyvqtRByXxx8ayR8SvsJ3rvwaCy+t2BPYZLo3HK3A1jF91fKO/NR60knGdDWYGEHT2St0k3AT0h5XDBrCifUOnoompg+KAmaaYd+SNzLxDk4i8yqnhawVSH1J2HpTPq40d3efY+j+Qytc3dypqJ91CiW6AwFLOV5QmuX4B4EFbQdM8IHptarZcLloFIyECv74WdUGyYMeA8ALEpCCisBgS9LfjNrAtRTV8ecPOwOoYrgXPEcoIq57Dgb9Cp+qjcVZv+QHCrNMBxAP8hrD5nBQfOn07T39g2UAtzRLHU2p+qxODjpUbJoIE5O+jVZJcfIUoQQ3QYNFdMqb7wa+ybojc998efYvH7LlvqatCDgW3zQQwvtI1L/jAwjg/+wegyrvMYTX8Vrum+RfGnPssN78w3tsC8vrj81Z6yeKZ4ZW9GPUZFEkIxU6nCohKAQ+Ct0Q+XMVH/9ciYWudxw2lSqbGOM1bOasfFlYEsp+pC4T2JtbfF+XP06tGjUoTSL8kq7i2p7rUqJ669aSjTtUf1FGUgljwK22SMifRZuZQQed32GvWylm6DkKUHZArUw0dkVNPBuRWPfGIsNC6L3yg0lDitpnZFJenzSREYL1A6Mi2tAlI3dLaR/ZTgnFKLdqYHlJVcjhW8daykl3ZijsxlcwsFe1HIDjYdJFGUtT75SS7dfV/G5hJuVpMzqh2AeS8WGTkQVADSYF+lP3otSr1zcDILHOS3TlqKkZPxxCzlSeOiQnrESYMNfEsxkYdqyYIpXcx1Pl8orV9pP64wrQvItBCmU2A8gZb+aAdVMNLnhiO0nOB0FF2zBlDtfP3/m+1HPeCtrqsdc+LJG8sNSk2EMRatF+4snnZF3NdTf8DgfWKkWW0TRgBFXAqo+l7Eow7wMzMear+BSrntDYb9vjirxL12oVT3gekzIrnSD3SpFlRQkVhwYe07bUPz9/f/kzNd9TpmwBi/zQaRQSMXXYg4zf55T6GGZaLBjNceOcyMN5/fFNdiaV7jrBI7fyocBqL8GLgdLJac9FRBcbxuM1umPT21Ctaq+N5LUS4ofOLwjbuptE9KppkmmBAIICy/4Mncbrdhq6geoOIYnUdivxlWXs7AP68W2iJK55pu0cHNQzYqv0nAbTRwjBcTKdVQjv1wjI5yA3SmqROMMo/fvwPf+dY2sh6EsGowqDd294jgwn6Kcgl0/vRoLbEe5tp55Ragu53etW4U13qN5sYMLwTt0JvOrSaNGRKYHGvvlhIXGQNUqY/lWKy4WyAXYr5wz0/IZNYro0Y09D5g57NLS5eXZTO+TTEW6aKGrIbPK3aqIK5jg2ndo9Ho/7kdOpktOQHbPhH3vSuiZZ8bevMt9fV+fOgQ62v4/FY6+urY3XtFwG9FUVO7eerTSdbpEgu0JdSK2QfKYgc51fHPP9moRvU9Igh14JWaz0QkOQJQAGKFbpqF/9i2N15UHhBLA03UfCEZkhr3A7bXXhG0VkrLyK5og2brCp0PQApCiObFV4vLe/iXwz8o1GlADFcJ8ewbXeuE2y0Qy0jqAAt9eLYNI1BC0b5JzN2GmKrqZXUyQCjFQD8VMPx56RNNB5z0RHeOhLNtZ8x56gL2wCIPrFpg9acCxB140+jwBbSN12i0Ctqhgtibm+dgoPPu94TKm+cJudpHuSHTAD6G7ByyUAo5zz0ctDCCZ30hRUpbhwd6dVZ138uxwCq6X4v3uEg6Zd6QEaBw2e9+pTVc7HfIdzBLVtVc53dCLYzohrgMApaCKD0fARD3qCD5SqqCQ2AdBIn19BQ1UvCEBUp5/C3ioLyL/Q31MyleblSl2NopyWdW/Nmgq2z4ZtBu9lvU48logBPsyCD0IsXxi9fYBB0zoAyB2eoYGsrCbd4nOTVp+PzACoaJPlsxArm9UkPjAC8FXbChKuh8x3UIRpMrAoOLqGaOBbCAGg3JBeF+j+Xrl4hXDQuHR0sQDQmfbwoBYz5Mz9gtBijYKtv92Ex7c/+BlAOZNCPFORAX4BY4ZDlw2zUhCW+BPICTFdnr6Ku0hgCUFWW+yDG/O8aGcFIbg5xCS3+W4NJ3UzGCs4fukuu4AH0yGVx3laI5MOsaQOCXnV8ZnUlJVNDGhG9R5RxGgLM7wYbuEUj4xSpkmy1FfXYK6tfArmj3ee/5Y3p9BL6s+bC4d3pV+J3fGpNYcWI2t/ub/j1qF/b0I3Ifw/vgn5vG8YTNVkXdL/mTsS5hTFQ9iicsfzEAQpZkxWItjjlntffel9xVWrN6y2PV1FAvL886CZ0o9dkjjGU6qKJT9Uf9VwXf+U5x2/Yr0oWKs9ucVU784XVzbwX17bzX/w9uw7FpUicp1hAdxEqJmzPLAETnNr17aiJfhearfJQzx2IA+vIHJAxIBs2JKoGXLSUlwtXBCpTh90qUy+WbapRWgVeEbXCKoKsIszVsbVKgd38euu8QYmi70EXoxzXmWidX9ZRfhmDW3hj4DdSUc5npxL/y0vS7hzUWI5lSeK8mhBntlNAiJ14SljSYQmuQIxmzF5xkHdtgG1KLNJi/heELYiVStf520kWa+SCBRsb+C4JN/nNC3PTs8UrdpJVO/nKjVq94StYsIrOSvL0ZNdxgIpj1kdTiDUK1DJQ/MUesGY5CYv7Xrx63OLjrB7X1EvXxRjYNuhU/9XXi4f1qOtl6T2uGCr9Dix/1WiPThSvnX8M8pBlE5H5sTYdMxd8Bm2+SpwEf3Cj/9WXj4f3qMvnct21oZ4Yy39lZ0qD2Z05tDmXifMON78H+Vy09IMxm9ovrytpr9gQn4qLqFpAyA90hG/F9amcctU0B1ELuP62z/R9HiTCSL4vxbKBCCgnFQ3EwIJVfKL1X0MKkNGeAJvNpOYluB+4zPasdjLV9G1YBZtYCtAKZZTSgGUW68vAzhZiCgucOBCrBBQaZwpr+JpCNi4b0cEodGJaMBqdMRWU8Ei5TMw76rsrVkdA9adIh0M/Wap0/YqKMHgFWfN21GqF4lGocdkZMWOEqTViqNKLF9S4unyhTJOnLR6o3Ks+Bfc+9aSCItB+GJAhorndJx8BgVykkaYUlIqhkq0IjwxVKzdXx8gDP0Zx5hVJ7HF+YtvuTzpdT17sr9UKdS6Kw5WRes5h70OB3U3WY8XcKGlPNy2cZze4EMBHvXAHaWIaJ4BGJdtSL0yoqXI953/AOjYkVQmUgnCxWj5MrCgCCheELMhidqnxjLnMIE/TcJLXN/Z6FDdM7SNKlsrwZ50WwCtNhqO4C9IFFiVuDjuhjLGKmwVEQVItEBtUXcdClp46d27qqUG8ggdR4/TuElXNkCYe1Tqh33ldfju80Yq2wrSXF0qRSthBPndeTU6cfVKdoT9FhAzLwhJTVOnYTafquCo5Vcv12tnNfdgV2dyMArfNKLjUldokgHvxgiURXhwvB0tsyvm5Nw2m7GebN3irPfY3832xO8/AqRSV0htS96CwkNmmMsDiQnbz2uXLlNx/xGjY4QGveh6UM1cSAVsUWe9RZTOHTg5SnOwEPUuP17XVdL2H3onSCHJB9BqePPJ8kWCm1gBLoJBGCvl3LMW084T01gqInn8Ys0fTVsfOHL2bvVDonhyv2pBb3/hMigPnEAC6E1wfs86X1dr7auQovAP/GFk6VrK0FPdBFdOm/HLtjEVpzGekwGvXmjPssFl9cYBznusBX4RF57niYen63FqpTEd68SXtXzrXcI1V/CaHHZioyzr0HX08UadwlmlMerNtIuzGTSi3chpR7vTaPh5lyy9wh8ALZUrwXpAy8g73Gb8x5mCzjuTZr/0sjjolajWXw+UGCHtZXCOMvUt014j2QeKAcyk618K96m7Q7mcyHCgFcmEPi3toCeQ7KDJg7ntYK30ckckk40eQGpF0cpMBUJzf5Oc2PeulNhVA3dxZlxQvqrEy6WAATjj5i7kMt0ir4MkRVIziBsO8Lmbjf0MJ5spw+lPDOL2njNVNBHCWLMJCYeBg2/RCpqaOEzNZzhWGcvBvseLIYOBf/Vn+nl4dO62f4THn/MZJXQGoa1zbQ2M94U5uJ52L5sq6mRwv/t7p79TRiZVB5iJyO0QMJgcbyrHYsnVYyAHF5HiTKO503E8QGAdC3WtuU3y77lDNeDH6W1B9pk3X4sDAyB0eonOqABydDG6q8kHI0/oiHXT32SrZg78LxF5Qi/rtXn3UlGTdBz0+xQCPYPZ9A/2totfYS++1a2cflf4mS889tardZE0uXx/niRfvBz5KTLcTx2zzMAD18adkbVhdUNcr6gGFfUABkrYdSd1WyqbJ5dM5TP1HT+koDowvjpC1yUO2wRMmEZnR7phMiAKWUFSBUlrJOw1S5k5tK0SSQS8KG+ANQPuhOOpZB+VYuBFnOmYcYScLGM43SaKfAU4mTbMpi2GISPky8jASFU/cFuyfbFv4yrRXMD8DlABGe5iu9kbQvEanAWRCl5SZrB3OnB1okANRY+Km6cP+OjME7JhBG1IqN2UdnbJFRU9gw/NnZZDTBrrmFBy01LCP16OWi2wRZXValE9JGdV8HbBwZWJtgF2TDhxzYdGLPLjyoBWZiXe6/V5oUx8os8ZGZNjrqPU1lYMgvRJixL3qwxpiagTxjWfT/sYmZQk9N/4sdgbJx3ODzLvt9V7M5+VnKEA+vy5DFQcMT/KZNjELaPym24CTnrdSr06t5ZRJx/IJhHvFMI21Icql4wsm960sdWVYSVmvOq/k0KI4GiyJf4cW1JbWukUL12OEJ8jClA0AsZ+ZyxME/ftWy7M1it6RrFR4OgFD4/RCw890rUHsDL5nuZmpMpqZ6dr/UbzMtPfnZmXGoVi47BjNZ3J4CkiX1OYkOsYRdlrps8Qq+gibVnEKnKx3IXEzczCEGA2mZSepnSEfzqT/r0A9WLR8FOLBM/mfSDv46c9FJaZqJO6LxRkk7EIqkcs1NiRCVxlEIuB7lkSYKiMphK78H0UhTHv/JSgExbno208LY11kTQspgRnrY1GCk9T29m3RFVI3PSijNy8rgI+yeXnw/5tu3pxKy/YMicwNjQdPG3fFQWyu+bOWct+6IS/Dzu561NmMsza0yom8Ux7krCmu0DogNdL+DnR4j7pHvktjDNXj4QsGvZhLiSiFgoVm7udlSlJzr5S9P5FOJgUKZMjACcKZXeM3h/9in3qRPToCJpmjYdD8xBNea2tr1a4hIr1gi3fI7k1Tw+yDXtwK9ig0wo4b1SndVg0falSqhAkCMXsINNHY4dB7vYyyg9krXMn4hI2Z14nsyFR0AzaESHGlrW33CkdZMsMfdsRj74SucvyeiZ71TnmI8RbKHt72qBAYLMB2r9dNnTPGcIpM7IkJ/5D4ZY6w/GsbJ1LnzhKQ+vi4/TDuEXLMUtaAa0BbjN8zF6+Z7YN5BgHkyTVbLjcr6HIzhffHE63GAQqM34R/nNO1QD/n+6TZZS0WYHm1vtOSHSeIr53ARuvF3abptQhWGaZMngRb2NGqMiN1GnX8C1XKhFo5jXTw9Nr+LXyOWvCEt//hDyKl8NumcmWsEQVwEaw531wf7ezfZW7vXPfPKMdjzseck5FAi1Gb0Q1v+kgveZSpY0kxp/HkZk4kyszESXPZSdtwJm3DnbSNE0xaBiZNmD6k3rmPDL1id+0ByuaitdtyDj5dtcbHX9O9U/pCMjy63k7xA5l9faWk53t76M832YvtVJN89yhTzXw9Jznmplr4f/boLG4uO9WBM9WBO9XBCaY6A5OmuvAaa3ZC5i+uwCvpbtPZJvfpOPTMxN7hS7rIqYlXCfzanVDr4WVv7PmTu36dRfGueYg6sAx9zlPSJ38lKUFc5+ww2+rKxNqKds+vkRRuXMA4Syhz4rG3u2HtF1FXU3pKMN1bTzsRzFiPyR3+n3PVZf6mzDvO9ZeqJEkwMAT/IkxK+uOYA7/T+/lLMjnLpqilCwgL/SfNq0vwl27NXO1k7svMNkDAyPFMRbFcNVDmMs58cbyJw2QskRsqbq6LREMBe/RkItXZNnr0kT5p37sM0F5eq4g/yN0RX9GNCXi6ur6X/VDu1wLsciysNdsJN8HULqYfPjTEvVxY3WwNn19gZqq5h3kVWJ7rh8YX5EAuqGSuZzaVxA09vJJc2GwqiYN7RCV9j7Otpt3gVNGpVTZuWbv5jGBqfeGFU1TO5gTnNpLCJTDL5BzZxkiUu+yb5YTCm77pU93etObZ2r27vTOSptxU5ZbP38+qb/W+SdLmvneltxFeiu/zvulLQvvu/d438YHeuHh3Mzvb+ye6Yxt/ygT9L3Hd9rAVGXDbNu9zfUGVc9u2U9e5RNvcviDLYj59QjdIHh59y9fHfE49MpfEUI3TErss7oTTrqx+mlfyNKPp6UukKFxFT9FC0LwWbIWnTVMARel7vqn3jf/US75Vae5G2OyTA2WJiS3s4JsOFd7PAht0b7fOA74CKgbz1VNQ/vt//Fd19Hsrn2Jxvs32S/dWIC2/Y+PN7aQ0OVEWQmEF3/K+BvrHj9/5HV06nLnzT+4zuevehqFKKN1eROk2B1wERBfw27+ja9oGyC5yAbrmJHjFIMhyObgiDZVzc4f3eBuE1909yF3srW/E9aKouHVzK7Z/+/fNjAyUaxlv3v4tALE3bv1SXzj9MHuti1wv+I0sj3PfcUHwGLXuSzP7Rfj3B7oz9hu+E3PgbUxyIdMh3cN2X0vh5kZ6EFRv2JueCnUdd+dneb9zx6serby9oxqyt+QiJb8l2ye6zJOXwtzVpUoNe+XFeKOs6Nqe7whPHtjpzdwxheD/JT/NeNXQ51r2pYvitITMNznrW3W/lEueYQvL5WcqfyC/4iMjyDitr5VyhlWAeXdMkCHfeM33BZ8UJ3WgOd0ehrfP/Ir20IE/an8HfK2yBxgO1KO4e8XeXY/lyyL6ITd8/jrLDNb6h2d6lDKHT4882MPKO/4RH3/i8xJ030cfz4GyyqADQZxzOXTbUkOVwtpWTU3UnqxNoGy9S0/l0ceQcJCJNIcWUNPcpD17hKIiYB9uwFQGaRo3I8zX4LDY3nZo5JJRreGCV/HkxQHj4zM6Rp15UpIKdfoweoy4C4a2iup7QauYMlHYKnwY3ao+I2XkSi7zYTs66tjEI3P894hWhLWfoBkrHWilDJ08oycv2asm/c7og2IWMCA8PwqYSE6OM4Gr15OILxAa1TKdfqDTy0e0TiIa1/DOR0CDK4Wq04kbI9tsRlVtJR7e3mIfLQtqZp4lR9zuIlVOi6nhz30Sj3MGz0lP4Rl07oHr8kD/5wnOtXDPD6RzbKQSrlbuIEE8lqTW6u9005JupgKzB2S0d/5sBZrGk0HWg7QZRZweV86ftj+RCXjUh+ekmRM6nAPVOM5MGaqKcV1J+PM+bOmW0Ev7zVBO+8rQ0Ee5DMD1frh9fCQXiDGgpDr3xB6cZI73lkKY7JQvJClQecMaRe8NTXOjk5myLix95FFhsDBlp/BoOUjPIhy3YNX7UR46x0t33syJ40M0IuF525zzWaPXeYNnjmFTd/q8ecoBxqGet4/OdyGa3Kz8qBientkLyd460MwcWmamYwiSw+bOLyrv+LJpRg7RIU3V4kpBaJOWrOjnJt7z4AtYWjjRrcpRzrWda5g9xz9SzmrluzLW42v0s5yph6Q95OCBzFhxlxdEE/jzNuQgUjyZUbsyW4bL6NO+6+qm6YONixl4DinobtNmPzRhndvxlj3K1NiwBtb/9TveYVds0rmpUW7lNL5Ag9oAC7t3wqGW49j+sWWGGPSKxyRHbDq9tIhdGdiVsmtkd5HtJIfjmUPJWMCWE8lqwRaixXh6LWq30/GWCLuYpjy+9OL8pUvuFbVsFXXLoMhu5G00PXln6tHRQXiIRdrFI7OSfjuE0T1ZTWGWMD50M2zuAWng68JMspm++SutedYpDzKwaHw7A31PgrZKYI6LLi2D2UsCdhwAb6rBevM1byTu5vqhSrNR2owBf/fUj9Vs2I7wkTN2rQTZDvbwkAA81onO+ORhYRBDRC2qhrlxhVQe1rj/8G8YILuDoBaps/jlllpOoq0t6PktRdnZt5Q+jA0el3BJ1C0sNizTCj43QMOsRp2ohzlQ8/AXazeDTQyYFf2sUVGTU+a2AViFq3LPqKJ7RjF3ysIwMGO+SRPBvgDiC/yZDXfDNp4Xy2uGyKNic98mJscHvXQ7DHsC0UIwQBO59bChRz2BcM3MP4G+1TTaYA2stDi3NDe9OPMCXpNaUfPNcCO+AbjcaZalBQecaSJoJQ70cfTvwU/4F6H8VOGhYokoPkn4Mz4jVo5sE6gMwQDEY2MNxEl4WLw4g0y72U9TOq5u4dL0FQReU2fOXInpSvHamTMCTGobaOirNtDO4mIBJ1fL00sv0mWw1C+kuAkfcAcTPRvPFkIWSBYJ0NyN5Kwh0KcQI/TLTBMBKLxVE08iGGAAOFB1GdNnhLpE27Qdd0JajrrCG7Urii9mrVAABIN0ajs4QPSyoXAqhXbe8o4poHcVbcBgeChp6UWX+hbkRn+rQQhKeUO31KV4y1yvS8NdnJmWyI0twBmSDfEWVIHI1Q00tNcgOLrTCv6SM3LPOZDW3HBobjUUQFLT7Hw2YNr7qi4R/VAl2ZdAhxveBeENVXJ3armiGpmLOnEzN4zBBcqze6CixGIG2IgXr1SUdwSiFh8IYDaQjSDaC0n5t2NCq7jXmsMPe8WuT+Y+/FegP7tBAoQFM3/xLuSFMNkJ+BBbQFvpUpc7iJOINl8g/qHqAGlJgPft4mbEJGRkN7BLt8OO4mjhGkNcNAtYvYj+S4R7QUPhkpwWEmwiVwjYroPHQONyYwAandWAoKY7vag619yOEcYlDPf7sZr6/vZ756BbbUBao2Wj/xmvksPDF0AFQlpHQaEiGGl4S0tXl6k74XawG8XEm4g9YNdAoY86YSvPIwoYMZOgQSyYv+aY7yLTNRdXlF5npT8KEazIUShEtXEQN0C6A4rTCqvx5qasTZY4+hxZOklmNadNGHO2UTHKr3Zegn1OC4oMuI82PZCwU0O01bOU1tFA40cT2Gmq6OovFXjQTS/pckQKLWjDanNncWeqPsh1pGb7FZmJoxrnIuxMjLEFIBRpjL2MhI326qIe/3Sb0nTR8EJoPCsiK/EA2AgO/2BpIf050DI+sXqzHVzX+DEbtviUFAf07CKBvAhjMf3uJjGIiqBEVxRec904+ogvmDn6Ci+9f109S3Zo54qb5xpM5Bra86mXzmzOBTxop4WnbnYmkZeYY0rU/CztTMy5aRRnTDY46GobN+mNHmCvIBECP4vAZhPYa1QAPiG0mSRE0APg6frVZ/EenOdwG8gxKA0Trghl6H1pRmOnhlGxk8cxlDBLuIjhz/t4+ywd9DqFvRJ6CCIFXx6+hHzqzBmSh6vqjE4XrZ9BnoAHpdNlEFmDtnVDqJLIHxhu0OSr6EhTrmmQumMAMmi10GzWYDT7n0qW8Bu6gN5xjh0M9GzRnff3jg4bw3ulG59u4YbdDBOcBKeKvWAVBpDKobtT2Ocna+IAxYmhicYLHDEmtWynaYmEZD5OfmcHzyNtIC/G4RUvrhrUU5Xtj3riCeLrDFhVd+SAZ/TXletaTDNiGyPL6lijphb66TYfsERHqHHo/kBKihecDaakeC/7AEoqSci+GIGWt5kAs9OmYab20igFKXVmmvWELG9Sy7OzxHfypBPaJdIpEgvIK1u4A56g6L9lkP2uUericKKJQIRoMtPkdOlApfFm77pwHQA/nOLleo1m4GYEYhvu5TmSy2UuLr+0tKw2UEIDGtXqN7UDAam0z2h726D9Xpyev7QE5Tfxri/sP14dhxO1ML20NLckLFo+1Cj5m04eQbHA2JqDnMwW4QXRSdTsAd2HfmyDutAz8oGVOKwwQkTbTykvkDlaIQWLqH437jhHZeVIaN2sVoCrlaOouIJ5quqlrjfIOQGtYaC2pquCaA2o7FPWRepznrB6IKV2AVHVG89KmYbMQiUiIjBVzXYfRO+l5UW0D8nNGbspUjrgZbCGLNJgtDsm3qJ2Iqr7wC2hCfFLdBSRYjkVR4G0CvmmpZDv/bM6+s3x3wuF/EKVLkAjwPvKhNdY5vu3v1BH73JU4ufIBYFEluY7uCqEHOUiOslNCpkcTu+E0jF60Li0XC30iUBjjALQprajXfB8g9DSHUCVssizSJlwWfR5Bc1uDgFRKH07S57ZXnoDIhjZm6WdPnzAq0fKGn2mu13YIhejGwjIKoJygWPKx8zQoXR9EIXb4gf0N5uRmN21tBi5BGKym31tRBCMYCZtQWf+1dWzr8J/1cuXq7Ozz5kV8bAD6B9rGgj6MmxMD0/QgHj0Hi0+RbqoEmqdo1ae0A1NRXsEh8pZdYbpF+X60G1t3uChj+eGY82MIAeMtvRs2oy74XPEu/jCF4MjFPL2nLY5eG0MwZxifqY16iFMTRfJcTbW3+uAEjAAPJlO2wQqqu+ug+bb41qhB56jJJCBd73l3HneZqwKyOB0k7guul32sz+RvXYDp3gUyzOwn9VdB94nql67LTfFSNgwyHRduemHsLg1nA8uBHzTNu48DAxgLxML/OSvQj+HTcHhK1LzLcrtPyPY0RXDe0ie5JBkylaX4wSVbAyTT1ulFJFBAr2UpllGNduKcPO5zSFJ9RQS8Ny4nkeHc9RVOmhbY0Yv7mpGl+ymZtzAW+yxDsXRfYoRJyTZvobjPnrXT37AXewE/E2VjVaRZRsyHKIKaPli0kBHDJyQQfwQMqLtcrT4uNTUuUbJjp567hFJickcshKOIF/ns0XVDq5+Dw1rjZUba9JuF7Gog7SbKFVjZWXoGt7Sv9fWDJ2dpoBnS16zfbIk0cje2vwRb0qgKqhaxBM8nOcEPrEZkCSDu0CTTrxKxwvmt02j//2EwVJ0kSleBZHsqInMPVqdpzSJFmL8RFbVOyPxjOoC35QAaChM3QyL5h6lzQY6SIgmAzVJwg2yQ+6ECV6yJRegILmuiLSoKA1NJwRJEaMQnlkGwnWtisStpUoMmtiGUaJquJeyWhBCc7iJoTjGgPusrMxzfBgrciYOu9HQsIug72V5CgoGT+NscTTQjMXmK32gwg5WbBI15Sz4iAmxvki2K1ewgNgaX2ckrRDG7OwggsGI6QZjzuwNUBvtsSHR2V+OcZGvw+DAFpRWHQOxepbTG58bbCYzFush3NCUGcgOB9nIPTynG0hhjK1Iy2NVSw7yTNC06nFB05Jmge7WGMX7LEiX+WFaVwjqSKqjcliio6wI6HUXBEVUcJC1mJaGM0JySEy3ttmY4MuORvG6jgoeiPqOXRO7bNpr6C42qGkQw3bjCLqBWK2aSUgkAlvzMn2MSZf5I+x51ksif97sAXoabxBdaRMbfPXgok1cW31x5QT1aXCv4HQPEB5QbqjYZYdxc5OaBdkdVPK8HWUbKhXwosh6AH1MAl5YmKidbm8QQyd58wkQQ3aj8LpDNNEO/aj8vIZrTMQz2Nxk1Y5v4EOcLpontv1gD+hmQX3DjNAWmKpqlWnjACJDDJypLY59qYcO8a09lyZ7pHGWo93wGDM055IYQ4TylRhELrbcwtxDB5mI1gaQdhTQcQVusCA0LtNnaa6h89UNItrZ2TI8fE6W2d+wrhjSQpcQWcZYQyOnA9sy2pK7ydtCW93OIiPFAt5WBMRZuTL3ChLRxsrlq7PzF1/l59m5S3PLc2uNsjXx4Y5EVqivi3MM3MClMLhVucGtzJJR50czOW6mXTyom6+metIdZQ4HfC6NaB219XVZ7Mjm4CvAxF4HZMWNftQmbU/4Of0GLm57j3BIeEj7EaayS30pD3yv34l6VKAl3mBVTalGaoGIIw4jGZjKTfC+ws3P/Uq14DFvSLW74b01fAkNPQ7h6IoCUJqz8MsDdj8s42B9hPgTxT5stoFHwoptaoULKxLpKKIPRBaiTrffG8zwYJaG8Tr4nGNzGBQQcfNegISJjRgeHlAR+y/inhgm9ZHnOaaH4QfI75wmM0peye3CSLcQxySQbfPnfdLLQDOh+ep3qfy1zB2osKB6e4xgcsFm2NuzDAdEHnHKAkrgASp7Qs8qQqht98SguUMkQA5a6CbhLgWrNtF11cEbkhGHKZpKGE9uf2Kzi2Ebw9ANWyXOwyEwQEKA8IL8vcB7hORrPl3t+Wgg35AtwhHJZKIgtSKyw+NhUXqyc+2kptomdCTrtLb7RkxSOioGRyLAa7FgDjmN84ZH+7bAqe0zNfJiF7xnZgf1L7+8UPCZzauVgYkJ9lORF5y/ZFzhOZFV8whYy3YMU62HB+ya+OxWaudKymSnhzZWDYNqgYOa7daM23FCoVVAtgMgKz3rXRJASK5gszaDTtyJUPUw29Zat/wp17ReAMwg6moHA18EPqC3vpu/UuBRqgzWlytDVF0mKFm1UxNuQeAnlLSPyP4nUBr5rsCaVXBQY5QjNSNDrVoVTI7ArAHc6SLxEBGqnEBpq2tIXpgc3nNMW4oi5gfrMjiGIaQdP+dIO0eo5IigBKXU6YplG7dS0aoz3wMsAkL2pOo8WcemiawX35M7goZzTAyyadQmcVGIImFJGz4jopGOBmVZgy5bHU7Gi4kqtj2Ekk6p3ShQjTz+NFxSLVfPX9LRK3ireGNlxczm2hqZjMQXzFIf2eC1+ReGSrQWN5pJpuBypAw0txkjC+k4IrpcJ75E/bR7QKQ2HY7aaDS6eBBBigcRyLsT7RBbX2j/PDYHnKynrlJcsiuvy2y8okdPPBM5HcY5pDBQit5klwIFx9DNqHwEq76Mmg7LsqK7Y1+c42vEAebLeCc70bMdE4lBGNrlm+qxsVIjIgpDZnV8YOskvdrr0hvMuG7YWABZkYtRp0X3U7uWDtecJKE6PVKSKuQpAYgxWoiY6ekRkTF2m84k5XOTKRwlaP2MEUBOQcWpNjTHkSo1XUJfbfGd7Zk9PZBoSIjlELohJfLBulEKg0DXrg7qdEI5t/ogxVTUFKXSWEnWRngy6fh5P4KdzHcx56iGgBM3t27kCTVNcaOWu4yiHyaKVJOQbZapaXMg1pkcNqMXQddy8zeEiBhbB4IlBrnYZ75Imx6HbyW0gAoTIcM2p/A6F7xKGDd5jFFLAyO9Cvf5AoawevOBEpvMssOZZbVsjIe564Im6QxoHW08JETrQTQJsn6yxHzbLAY7a2GP1WMnas/d8RLuWrIxsKRHz5rAVzRPXJypiS5sLE/AVD2vvAvurICj0FUCN9fZgtkKKRTNt1E9CtwpgetEsD6RCV8VLy+uYsacVMl4V1Pr4kLbqm2qIJpxaBSjF1HgGgs1wIHBjJLj5AdWoGOJqClqyaKEYOCEAecFNALN62JclJjxI7l3QuhcUUgjGnaIdG/AxNPV28Ssg54loxr5LmLZ55FIuCiK+oBDT4xA6kuSjvTnhSehBkx9yNKhgcQPkXII5cPPxTbfyToSATRQY3BDIGELFURnXnsd0c1kn7BxQXAvZWwU10Ge7GGr1uYLLaEmQybxcYQ/itpRdRMJSaGywCTEwUBMRiLPKa7UqlAjYnzmpmerV69cepUd63pfATQeIHI0IZ5sPSYpBXbc0vLi/MzypVfVwuLVF+YvzC/PzYqMxG30WfpZAA7QAYGZ9E3QUUKYG7zgD+MiYcsoWMUA5nc72tpuw/961ipFAZI86fEmoJea/P72e2ehQkT52E3QeGz05UBjKcsdbh7BPKerYb4FjM6la3M3uu2oCZsbxJdAVH+hPOSmsauAvX6uUSYLQDMMW54pSLhO0AM870YOlbgSK52gniOe85y3p1MZhof2qcWgg25OkFlYItrYU3SDDNIvw/gmq3QdCt9mH4jgBV2yPhlBYBgmaIW9PVRxrhHaaTYw0w5E5zKL54h3e5oa4YhgqYipNlGbdmOGa2oG3Q8/h97hkmL6E7oCAhAZTPQIhzOJfRHk6zC4pkgoJkrTjXHFUHsiv1PFGquBiXH2EIUlR+k1Y8B8CTfPNPkcoF7JBO8ya8mlS9OVrEHvL1W80YPdgZFOjAoij7HaIaRVu1P09X7nmASSa9S3kRbFeYn9gqgax3dpmmKs18XRXFxRFx4WJItlsjGgJ46rGhEtpYVj8q8zttbJEIaGfkwIp3hbWi12JiI8N1oWl4qc1ejM2wXZAkM5x7VhBdXu0HPejoxCzYWe+hOmBgxmYEBqQ6+CG9iaC0bFrWujUQ1b4FWhQUrgzAbPLCj4AjcTpSo3Ao8I7hHP5xCmZs6PygWtss8UMB4XKqxuMqFl23aFj3xjuzwI0PE1J7tGckl5TUyyTZ6zabcsMjfd3EwfHe4L/Y32CZ2YOd+uZx4PPFlVXM3oxOCTm5zL+YayO0PidYodni0g5layA5K0dmXu5blFIGFUhKg710IzrMkcQSNbe09H89h5fT5g7+GCEUlxsXHuvIu7Izr1AokuD4Zd6th61NGiKXH1hmOFIEkvHWY2fiml9Ajo6WAbR8k1cNiDUJCfWTOy2OK2tht4D/AQJUWPm8zJ6eMZ5Ep+7IbnG9Lih+Mjynh9aIOKpo/zSnnlmTI2akEMSmJ5sEELaIhB9zQF14wKrSfu6OYJP8FS3SxZCDxnEr+S7N0GH0EGI/Z3P8yRHDHxYzPnKtiF1UZljk5UbNiDjXPOyAu0e1+A3Wvb1Rhud7aMmWN/+fQgcrZVrMWLCrs4UTE7DJTHwMLjCmWHIXRibkQ7Rzb1XTyoK9ChCf71hSbyVtKiDeXQWTQjUck5w8ce7EDEQ8nhN+qKYVn2rOxRRxOZo7Mb3t2QoldTYE0Ik4EiqDmmT0sBxKx8Y6jjGsYwQUE4e2R362R5HLDTKE5Lk0ntPEaWPvPC9JXn5y5dfd5j+hzXxQGu3kCY8vd30qK4V816iXKn2658LBiKiO6ESmF9YwUDhSbusb4cAJbxVOpIVvTQsxAabNkqekCcqLS1bV7Id4bBbOqM4+B3ju8b1iO/Hy2xlnB0lkkuJ3Nc7g5m0nS1nkvhURSm+qeNWiNRyJi7h/B/cTwNEwC4SLFmO1E3FlRWuoBkbe+BaA3DRMupm1FdprPrwzStckx5RFK3mw2lc6hs5hNnlhXJBiLYGc13ou7pYxedvO5FMwRHVtjlbiPZ6oTXtcaoY8eAuG6zw8uOhjIV2nwV94AkQTbLRp1dBLMliq5WPbtRD6nXCFkCT7OxwRFPoAkJpkyJN1CMSmYSg60ATSu2kXYEuJrW1dUl98wDpJhbSdxHQyWsPRC1ioLtgPOPbrtOEwQG2Pp9QZYz2lCY7CLzCVpqDu9eJB3HyCwio3L4MfLTXozWcEZ4k1xo1Emb1vnoKYKuhzSTHegimGGhMkM4Z8hCYWUxFYJSZTvNbY6rNmouxltSAXKkIC/BECyti+Lw+ux9zyqWRrnAQy/z6TJOp91ODtOwdDlOn4MZghncqagXHBQ0I4DnZY12wANArLxRoR3AGaKSrGgy7672e0DHQm2gQFuqbLZF2oBJhu6c0dsa0wv1wEwqJoVhdcIQWuJUNC8B8f1/x7Pp+azW7+Rc9cOjOzrTELNJ/aM76SzNi32KrHoBNtgvMLd1XMhAeYTc5JoZsSuuyaIoV1JLMPbwhlI+kbVgVH/mtEqOIqLU0SeU1lDdQLwTJls+aaSnkcmUDob+CfIoNUku16kJF+cfP5sSheshzAk/FzOms/XBpv5M2K3Jrc8cgXFSCyzFVxk+dLZusyJOHGpLIIwV1jiuRfrxez9+9NnRB8Rn+IonafY/3CA7Ry7YGT1v2nvFs8lzxf7pjdAYvoBtiEIEkkJhICKqJCYWcTSvoKkmhjHENsYxPJkkSMNCjD7kxhDbnEhjlZRDF8n8ZNtDeZEvmtGSYVYLtKf5DImjXb8o9002fB7jYVEuJOokAAvic0+QqYm1XLGf+7GX3Ssjg0krdH20Df0DrjW9MK/SaKsTyG8OyJdLnEBC7rTQ62TjkNC7aS2nmQBuNMYB4pUKQkbTrJ9N1PwK6pzoh3Hjr8uZ9jB+aZOiawAg6PaYsoOxhLPlM2cKUwkzGUPknG85iUNDk310ptDInKKRGYInsmDK7diDunMiQyWSJKH0Tp6IsVJiQhfmkEnPH81MydaMcR0GkOrrf2p7O23kAUz+80fpIrWQox1RM6ybIxPt/QxVdXr3zGksiDlOEflC+as+XKVOhni6mupn8QZ/I+NEFcalzYkCjzvCZhKxSsLoFu2R+4pofBX5Un+j3+n1q7TP5OoXivl3usbgZnTMOGa9phFSDnsQHPAN6CGf+pmO6/Dyv9590hZBnuZd+rIZ9prb1RZssO26PS/QNog5tf2uGPIGNQUL2u9WWRH9691zQ5rjMlVzh8Lpqdrk5Ol8s2JCy8R4zWud1TnpsA9QbuWbGBlulG1R27UWhNNZ+9awxgBZV1R1Ey+qKzRnpdurY2rtL5HwZ25Xxrtc1MBKHff26VGNdPcGNZKZi1y1Ac2I/Y1iQgeB7nR3VDNCgQ+fMCeXoHu4FeWnWTsd7YGJT+jFntE2IucysVbdHPq5E/aCYUtBp0uqapfMNsMRotCK9xc3byq51CwJN/kun/19ZQ/xzY1F72n//ofsJsHzLzBeLB3n7VLd2taU4q93z7oXp9VFaHsFb0yzXamo0/AvXW+Wjp8uD9ldPu0rHpBbvoViRB3Npv6N790k1LQs/5Gkv8zcK7GVAY3e//8BB+TtbA=="
# --- END_EMBEDDED_ASSETS ---


# --- STACK PRESETS & METADATA ---

STACK_PRESETS = {
    "swift": {
        "name": "iOS / macOS (Swift, SwiftUI, Xcode)",
        "language": "Swift",
        "build_cmd": "swift build",
        "test_cmd": "swift test",
        "lint_cmd": "swiftlint",
        "file_ext": ".swift",
        "sample_contract": "```swift\npublic protocol ExampleServiceProtocol: Sendable {\n    func execute() async throws -> String\n}\n```",
        "bug_env": "  - OS: iOS 18.x / macOS 15.x\n  - Toolchain: Xcode 16.x / Swift 6.0",
        "research_quirks": "* **Concurrency & Memory:** ARC weak/unowned, Task isolation, Sendable, BGAppRefresh.",
    },
    "ts": {
        "name": "Web / Node (TypeScript, JavaScript)",
        "language": "TypeScript",
        "build_cmd": "npm run build",
        "test_cmd": "npm test",
        "lint_cmd": "npm run lint",
        "file_ext": ".ts",
        "sample_contract": "```typescript\nexport interface ExampleService {\n  execute(signal?: AbortSignal): Promise<string>;\n}\n```",
        "bug_env": "  - OS: macOS / Linux / Windows\n  - Runtime: Node.js 20.x / 22.x",
        "research_quirks": "* **Event Loop & Memory:** Microtasks, uncleaned event listeners, SSR hydration.",
    },
    "python": {
        "name": "Python (Standard / Pytest / FastAPI)",
        "language": "Python",
        "build_cmd": "python -m py_compile scripts/*.py",
        "test_cmd": "pytest",
        "lint_cmd": "ruff check .",
        "file_ext": ".py",
        "sample_contract": "```python\nclass ExampleService:\n    def execute(self) -> str:\n        return \"OK\"\n```",
        "bug_env": "  - OS: macOS / Linux / Windows\n  - Python: 3.10+ / 3.12+",
        "research_quirks": "* **Async & Types:** Asyncio event loop blocking, GIL limitations, type hinting.",
    },
    "dotnet": {
        "name": ".NET / C# (ASP.NET, MAUI, Console)",
        "language": "C#",
        "build_cmd": "dotnet build",
        "test_cmd": "dotnet test",
        "lint_cmd": "dotnet format",
        "file_ext": ".cs",
        "sample_contract": "```csharp\npublic interface IExampleService {\n    Task<string> ExecuteAsync(CancellationToken ct = default);\n}\n```",
        "bug_env": "  - OS: Windows 11 / macOS / Linux\n  - SDK: .NET 8.0 / 9.0",
        "research_quirks": "* **Async & GC:** ConfigureAwait(false), ThreadPool starvation, IDisposable pattern.",
    },
    "generic": {
        "name": "Generic / Other Technology Stack",
        "language": "Source Code",
        "build_cmd": "make build",
        "test_cmd": "make test",
        "lint_cmd": "make lint",
        "file_ext": ".src",
        "sample_contract": "```text\nfunction execute(): Result\n```",
        "bug_env": "  - OS: macOS / Linux / Windows\n  - Runtime: Project runtime",
        "research_quirks": "* **Concurrency & Resources:** Thread safety, race conditions, memory lifecycle.",
    },
}


# --- ASSET UNPACKING ---

def unpack_assets(source_repo_path: Path = None) -> dict:
    """
    Unpacks embedded assets from base64/zlib.
    Falls back to local filesystem if running in source repo and bundle is empty.
    """
    if EMBEDDED_ASSETS_B64:
        try:
            compressed = base64.b64decode(EMBEDDED_ASSETS_B64.encode("ascii"))
            raw_json = zlib.decompress(compressed).decode("utf-8")
            return json.loads(raw_json)
        except Exception as e:
            print(f"⚠️ Error unpacking embedded bundle: {e}")

    # Fallback for local repository development
    repo_root = source_repo_path or Path(__file__).resolve().parent
    templates_dir = repo_root / "templates"
    scripts_dir = repo_root / "scripts"
    skills_dir = repo_root / ".agents" / "skills"

    if templates_dir.is_dir():
        assets = {}
        for tf in templates_dir.glob("*.md"):
            assets[f"00_Templates/{tf.name}"] = tf.read_text(encoding="utf-8")
        graph_json = templates_dir / "graph.json"
        if graph_json.is_file():
            assets[".obsidian/graph.json"] = graph_json.read_text(encoding="utf-8")
        for sname in ["kb_lint.py", "kb_release.py"]:
            sfile = scripts_dir / sname
            if sfile.is_file():
                assets[f"scripts/{sname}"] = sfile.read_text(encoding="utf-8")
        if skills_dir.is_dir():
            for sdir in sorted([d for d in skills_dir.iterdir() if d.is_dir()]):
                skill_md = sdir / "SKILL.md"
                if skill_md.is_file():
                    assets[f".agents/skills/{sdir.name}/SKILL.md"] = skill_md.read_text(encoding="utf-8")
        workflows_dir = repo_root / ".github" / "workflows"
        if workflows_dir.is_dir():
            for wf in workflows_dir.glob("*.yml"):
                assets[f".github/workflows/{wf.name}"] = wf.read_text(encoding="utf-8")
        if assets:
            return assets

    raise RuntimeError("Cannot find assets. Both embedded bundle and local templates directory are unavailable.")


# --- GENERATORS FOR AGENTS & REPO RULES ---

_RULES_BODY = ("## Docs-as-Code (12 Disciplines)\n"
    "Language: {lang}\n"
    "1. Read `SPEC.md`, `docs/00_Index.md`, `docs/Onboarding.md` at session start.\n"
    "2. Kanban: move cards with date `(YYYY-MM-DD)`.\n"
    "3. Roadmap: mark `[x]` + link `[[Specs/.../TASK-XXX|TASK-XXX]]`.\n"
    "4. ADR & Rejected-ADR: log all decisions incl. rejected (`status: rejected`).\n"
    "5. Research: worst-case tests; record discarded prototypes in `RESEARCH-XXX`.\n"
    "6. Devlog: write entry at task/session end.\n"
    "7. Obsidian: wikilinks `[[...]]` + tags.\n"
    "8. Permalinks: NEVER move `TASK-XXX`/`BUG-XXX` to Done/Archive.\n"
    "9. Regression-First: failing test BEFORE fixing any bug.\n"
    "10. QA: checklists `- [ ]` in `docs/05_Testing/`, separate from Plans.\n"
    "11. Graph: 7 Obsidian color groups (White/Purple/Cyan/Yellow/Orange/Red/Green).\n"
    "12. Git: Remote/Local/None + Trunk-Based docs + Feature Branching.\n")


def _rules(doc_lang: str) -> str:
    lang = "Documentation/Devlog **Russian**, code/commits **English**." if doc_lang == "ru" else "All documentation **English**."
    return _RULES_BODY.format(lang=lang)




_3MODES = (
    "## 🔄 3-Mode Discipline & Workflow\n\n"
    "**Mode 1 -- Planning (`/kb-plan`):** STRICTLY NO CODE CHANGES. User approval before writing plan docs.\n"
    "**Mode 2 -- Task Spec (`/kb-task`):** STRICTLY NO CODE CHANGES. `[NEW]`/`[MODIFY]`/`[DELETE]` contracts + DoD.\n"
    "**Mode 3 -- Implementation (`/kb-implement`):\n"
    "```bash\n{test_cmd}\npython3 scripts/kb_lint.py --path docs\n```\n"
    "Auto-complete: spec->done · Kanban+date · Roadmap `[x]` · Devlog · kb_lint · git push.\n\n"
    "Anti-Echo: NEVER reprint entire files in chat; emit link + 3-5 bullets + next step.\n"
    "Senior Partner: flag risks, propose alternatives. Rejected ADRs: `docs/03_Decisions_ADR/` (`status: rejected`).\n"
)


def _gen_rule(title: str, p: str, s: str, l: str, extra: str = "", tail: str = "") -> str:
    st = STACK_PRESETS.get(s, STACK_PRESETS["generic"])
    return f"# {title} for {p}\n\nStack: **{st['name']}**{extra}\n\n{_rules(l)}\n{_3MODES.format(test_cmd=st['test_cmd'])}{tail}"


def generate_gemini_md(p: str, s: str, l: str = "ru") -> str:
    return _gen_rule("GEMINI.md -- Google Antigravity & Gemini CLI Rules", p, s, l, " | Full Guidelines: `AGENTS.md`", "\nSkills: `/kb-plan` `/kb-task` `/kb-implement` `/kb-complete` `/kb-bug` `/kb-adr` `/kb-research` `/kb-release` `/kb-lint`\n")


def generate_windsurfrules(p: str, s: str, l: str = "ru") -> str:
    st = STACK_PRESETS.get(s, STACK_PRESETS["generic"])
    return _gen_rule(".windsurfrules -- Windsurf Cascade AI Rules", p, s, l, f" | Build: `{st['build_cmd']}` | Test: `{st['test_cmd']}`")


def generate_clinerules(p: str, s: str, l: str = "ru") -> str:
    return _gen_rule("Cline / Roo Code AI Rules", p, s, l, " | Read `AGENTS.md` and `docs/Onboarding.md` first.")


def generate_claude_md(p: str, s: str, l: str = "ru") -> str:
    st = STACK_PRESETS.get(s, STACK_PRESETS["generic"])
    return _gen_rule("CLAUDE.md -- Claude Code Guidelines", p, s, l, f" | Build: `{st['build_cmd']}` | Test: `{st['test_cmd']}` | Lint: `python3 scripts/kb_lint.py --path docs`")


def generate_cursorrules(p: str, s: str, l: str = "ru") -> str:
    return _gen_rule("Cursor Rules", p, s, l, "\nYou are a **Senior Engineering Partner**. Read `AGENTS.md`.")


def generate_copilot_instructions(p: str, s: str, l: str = "ru") -> str:
    return _gen_rule("GitHub Copilot Instructions", p, s, l, " | Read `AGENTS.md` for full guidelines.")


def generate_agents_md(project_name: str, stack_key: str, doc_lang: str = "ru") -> str:
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    rules = _rules(doc_lang)
    return f"""# 🤖 AGENTS.md -- AI Agent Guidelines & Operating Modes

> **Project:** {project_name} | **Stack:** {stack['name']}
> **Spec:** [[SPEC|SPEC.md]] | **KB:** [[docs/00_Index|00_Index]] | **Onboarding:** [[docs/Onboarding|Onboarding Guide]]

---

{rules}
### 🎨 Obsidian Graph Color Scheme & Tagging
| Color / Category | Obsidian Path / Query | Tags | Description |
| :--- | :--- | :--- | :--- |
| ⚪ White / Light | `file:00_Index`, `file:Devlog`, `file:SPEC` | — | Entry points & root navigation hubs |
| 🟣 Purple | `path:01_Architecture` | `#arch` | System architecture, contracts & modules |
| 🔵 Blue / Cyan | `path:03_Decisions_ADR` | `#adr` | Architecture Decision Records |
| 🟡 Yellow / Amber | `path:04_Research` | `#research` | Platform research, benchmarks & quirks |
| 🟠 Orange | `path:02_Tasks` | `#task` | Backlog, Roadmap, Plans & Task Specs |
| 🔴 Red | `path:02_Tasks/Bugs` | `#bug` | Defects, bugs, RCA & regression tests |
| 🟢 Green | `path:05_Testing` | `#testing` | Acceptance testing & E2E UX checklists |

---

## 🔇 Anti-Echo Response Protocol

When modifying or creating files on disk:
1. **STRICTLY PROHIBITED:** Dumping complete file contents or repetitive code blocks into chat responses.
2. **REQUIRED RESPONSE FORMAT:**
   - Clickable file link: `[FileName](file:///absolute/path/to/file)`
   - Concise 3–5 bullet summary of what changed and key architectural decisions
   - Next actionable step or prompt for confirmation

---

## 🧠 Senior Engineering Partner Standard

You are a **Senior Engineering Partner**, not a passive assistant:
1. **Critical Review:** Evaluate against best practices ({stack['language']}, Clean Architecture, Zero Dependencies).
2. **Constructive Challenge:** Flag flaws -> justify consequences -> offer 1--2 robust alternatives.
3. **User Confirmation Required (Mode 1 & 2):** NEVER write plan/spec docs without explicit user approval.
4. **Rejected ADRs:** Document discarded directions (`status: rejected`) in `docs/03_Decisions_ADR/`.

---

## 🔄 The 3-Mode Development Cycle

### 🟡 Mode 1 -- Planning (`/kb-plan`)
**🚨 STRICTLY NO CODE CHANGES.** Research, Q&A, critical review. User confirmation before any plan doc.
Output: `docs/02_Tasks/Plans/PLAN-XXX-<slug>.md` + Kanban Backlog card.

### 🟠 Mode 2 -- Task Spec (`/kb-task`)
**🚨 STRICTLY NO CODE CHANGES.** File contracts + verification plan.
Contracts: `[NEW] path/to/file{stack['file_ext']}` / `[MODIFY]` / `[DELETE]` with signatures and DoD.
Output: `docs/02_Tasks/Specs/<Phase>/TASK-XXX-<slug>.md` + Kanban In Progress.

### 🟢 Mode 3 -- Implementation (`/kb-implement` -> `/kb-complete`)
Code strictly per approved spec. Run:
```bash
{stack['build_cmd']}
{stack['test_cmd']}
python3 scripts/kb_lint.py --path docs
```
Completion checklist: spec->done · Kanban->Done(date) · Roadmap `[x]` · Devlog · kb_lint 0 errors · git push.
"""

# --- STARTER DOCS CUSTOMIZATION ---

def customize_templates_for_stack(template_name: str, content: str, stack_key: str, today_str: str) -> str:
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    content = content.replace("2026-09-19", today_str).replace("2026-09-26", today_str)

    if template_name == "TEMPLATE_TASK.md":
        # Replace sample contract with stack-specific contract
        contract_marker = "```python\n# Ключевой контракт\n```"
        if contract_marker in content:
            content = content.replace(contract_marker, stack["sample_contract"])
        contract_target = "```csharp\n// Пример ключевого интерфейса или фрагмента контракта\npublic interface IExampleService\n{\n    Task ExecuteAsync(CancellationToken ct);\n}\n```"
        if contract_target in content:
            content = content.replace(contract_target, stack["sample_contract"])
        # Replace build & test command
        content = content.replace("<!-- команда сборки, Exit code 0 -->", stack["build_cmd"])
        content = content.replace("<!-- команда запуска тестов, 100% pass -->", stack["test_cmd"])
        content = content.replace("`dotnet build` или `./gradlew test`", f"`{stack['build_cmd']}`")
        content = content.replace("`dotnet test`", f"`{stack['test_cmd']}`")
        content = content.replace("path/to/file.ext", f"path/to/file{stack['file_ext']}")
        content = content.replace("Path/To/NewFile.cs", f"Path/To/NewFile{stack['file_ext']}")
        content = content.replace("Path/To/ExistingFile.kt", f"Path/To/ExistingFile{stack['file_ext']}")
        content = content.replace("Path/To/OldFile.cs", f"Path/To/OldFile{stack['file_ext']}")

    elif template_name == "TEMPLATE_BUG.md":
        # Replace bug environment and test paths
        env_marker = "* **Окружение:** <!-- ОС, версия, стек -->"
        if env_marker in content:
            content = content.replace(env_marker, f"* **Окружение:**\n{stack['bug_env']}")
        legacy_env = "  - ОС: Windows 11 Build / Android Version\n  - Стек: .NET SDK / Gradle Version / Runtime\n  - Сеть/Конфигурация: Localhost / Wi-Fi / VPN"
        if legacy_env in content:
            content = content.replace(legacy_env, stack["bug_env"])
        content = content.replace("tests/path/to/test_regression.ext", f"tests/path/to/test_regression{stack['file_ext']}")
        content = content.replace("path/to/file.ext", f"path/to/file{stack['file_ext']}")
        content = content.replace("path/to/file.cs", f"path/to/file{stack['file_ext']}")
        content = content.replace("tests/Path/To/RegressionTest.cs", f"tests/Path/To/RegressionTest{stack['file_ext']}")

    elif template_name == "TEMPLATE_RESEARCH.md":
        # Replace sample research code and platform quirks
        quirks_marker = "<!-- Поведение подсистемы в фоне, энергопотребление, жизненный цикл, лимиты -->"
        if quirks_marker in content:
            content = content.replace(quirks_marker, stack["research_quirks"])
        legacy_quirks = "* **Поведение в фоне и энергопотребление (Doze / WakeLock):** ...\n* **Поведение при сбоях сети и роуминге:** ...\n* **Потокобезопасность и нагрузка на память/CPU:** ...\n* **Ограничения прав и безопасности ОС:** ..."
        if legacy_quirks in content:
            content = content.replace(legacy_quirks, stack["research_quirks"])
        content = content.replace("```python\n# Экспериментальный код или бенчмарк\n```", stack["sample_contract"])
        content = content.replace("```kotlin\n// Пример проверочного кода или сниппета решения\n```", stack["sample_contract"])

    return content


def detect_project_stack(target_dir: Path) -> str:
    """
    Эвристический детект стека по маркерным файлам в корне проекта.
    Возвращает ключ стека из STACK_PRESETS ('swift', 'ts', 'python', 'dotnet', 'generic').
    """
    if not target_dir.is_dir():
        return "generic"
    if (target_dir / "Package.swift").is_file():
        return "swift"
    if (target_dir / "package.json").is_file():
        return "ts"
    if any((target_dir / f).is_file() for f in ["pyproject.toml", "requirements.txt", "Pipfile", "setup.py"]):
        return "python"
    try:
        if list(target_dir.glob("*.sln")) or list(target_dir.glob("*.csproj")):
            return "dotnet"
    except Exception:
        pass
    return "generic"


def handle_readme(target_dir: Path, project_name: str, doc_lang: str = "ru"):
    readme_path = target_dir / "README.md"
    if doc_lang == "en":
        docs_block = """

---

## 🧠 AI Agent Documentation & Discipline (Docs-as-Code)
This project uses the Docs-as-Code knowledge base and strict 3-mode workflow for AI agents:
* **Documentation Vault:** `docs/` (open as Obsidian Vault).
* **Universal Agent Rules:** [AGENTS.md](AGENTS.md).
* **Knowledge Map (MOC):** [docs/00_Index.md](docs/00_Index.md).
* **Integrity Linter:** `python scripts/kb_lint.py --path docs`.
"""
    else:
        docs_block = """

---

## 🧠 Документация и дисциплина AI-агентов (Docs-as-Code)
В проекте развернута база знаний Docs-as-Code и строгий 3-режимный регламент работы с AI-агентами:
* **Каталог документации:** `docs/` (открывается как Vault в Obsidian).
* **Главный регламент агентов:** [AGENTS.md](AGENTS.md).
* **Карта заметок:** [docs/00_Index.md](docs/00_Index.md).
* **Проверка базы знаний:** `python scripts/kb_lint.py --path docs`.
"""
    if readme_path.is_file():
        content = readme_path.read_text(encoding="utf-8")
        if "AGENTS.md" not in content and "Docs-as-Code" not in content:
            readme_path.write_text(content.rstrip() + "\n" + docs_block, encoding="utf-8")
            print("📝 Appended Docs-as-Code section to existing README.md.")
    else:
        new_content = f"# {project_name}\n\nProject repository.\n{docs_block}"
        readme_path.write_text(new_content, encoding="utf-8")
        print("📝 Created root README.md with Docs-as-Code section.")


def handle_gitignore(target_dir: Path):
    gitignore_path = target_dir / ".gitignore"
    obsidian_rules = """
# Obsidian Workspace (preserve graph.json)
.obsidian/*
!.obsidian/graph.json
"""
    if not gitignore_path.exists():
        gitignore_content = """# System & IDE
.DS_Store
Thumbs.db
.idea/
.vscode/*
!.vscode/settings.json
""" + obsidian_rules
        gitignore_path.write_text(gitignore_content.strip() + "\n", encoding="utf-8")
        print("📁 Created .gitignore (with Obsidian graph retention rules).")
    else:
        content = gitignore_path.read_text(encoding="utf-8")
        if ".obsidian" not in content:
            gitignore_path.write_text(content.rstrip() + "\n" + obsidian_rules, encoding="utf-8")
            print("📁 Appended Obsidian retention rules to existing .gitignore.")


def create_starter_docs(target_dir: Path, project_name: str, stack_key: str, assets: dict = None, force: bool = False):
    stack = STACK_PRESETS.get(stack_key, STACK_PRESETS["generic"])
    today_str = date.today().isoformat()
    docs_dir = target_dir / "docs"

    # 1. SPEC.md (Root)
    spec_path = target_dir / "SPEC.md"
    if not spec_path.exists() or force:
        spec_content = f"""---
id: SPEC
title: "Мастер-спецификация: {project_name}"
status: active
type: specification
created: {today_str}
updated: {today_str}
tags:
  - spec
  - master
  - {project_name.lower().replace(" ", "-")}
---

# 🚀 Мастер-спецификация: {project_name}

> **Проект:** {project_name}  
> **Стек:** {stack['name']}  
> **Связанные документы:** [[docs/00_Index|00_Index]], [[docs/Onboarding|Онбординг]], [[docs/02_Tasks/Kanban|Канбан]], [[docs/02_Tasks/Roadmap|Дорожная карта]].

---

## 1. Концепция и цели проекта
*Краткое описание назначения проекта, решаемой проблемы и целевой аудитории.*

---

## 2. Архитектура и стек технологий
* **Платформа и технологии:** {stack['name']} ({stack['language']})
* **Сборка проекта:** `{stack['build_cmd']}`
* **Запуск тестов:** `{stack['test_cmd']}`
* **Проверка базы знаний:** `python3 scripts/kb_lint.py --path docs`

---

## 3. Этапы разработки
План реализации разбит на фазы в [[docs/02_Tasks/Roadmap|Дорожной карте]]:
* **Фаза 1: Инициализация и MVP** -- Базовый каркас и проверка сборки.
* **Фаза 2: Основная функциональность** -- Ключевые пользовательские сценарии.
"""
        spec_path.write_text(spec_content, encoding="utf-8")

    # 2. docs/00_Index.md
    index_path = docs_dir / "00_Index.md"
    if not index_path.exists() or force:
        tpl = (assets or {}).get("00_Templates/TEMPLATE_INDEX.md", "")
        index_content = tpl.replace("[Название Проекта]", project_name).replace("2026-09-19", today_str) if tpl else f"# {project_name}\n"
        index_path.write_text(index_content, encoding="utf-8")

    # 3. docs/Onboarding.md
    onboarding_path = docs_dir / "Onboarding.md"
    if not onboarding_path.exists() or force:
        tpl = (assets or {}).get("00_Templates/TEMPLATE_ONBOARDING.md", "")
        onboarding_content = (
            tpl.replace("[Название Проекта]", project_name)
            .replace("2026-09-19", today_str)
            .replace("dotnet build", stack["build_cmd"])
            .replace("dotnet test", stack["test_cmd"])
        ) if tpl else f"# Onboarding: {project_name}\n"
        onboarding_path.write_text(onboarding_content, encoding="utf-8")

    # 4. docs/Devlog.md
    devlog_path = docs_dir / "Devlog.md"
    if not devlog_path.exists() or force:
        tpl = (assets or {}).get("00_Templates/TEMPLATE_DEVLOG.md", "")
        devlog_content = tpl.replace("2026-09-19", today_str) if tpl else f"# Devlog: {project_name}\n"
        devlog_path.write_text(devlog_content, encoding="utf-8")

    # 5. docs/02_Tasks/Kanban.md
    kanban_path = docs_dir / "02_Tasks" / "Kanban.md"
    if not kanban_path.exists() or force:
        kanban_content = f"""---
kanban-plugin: basic
---

# 📋 Канбан-доска: {project_name}

> **Теги:** #tasks #kanban #planning  
> **Связанная дорожная карта:** [[Roadmap|Дорожная карта]]  

## 📥 Бэклог (Backlog)

<!-- Начните с создания первого плана через команду агента /kb-plan <название> -->

## ⏳ В работе (In Progress)


## ✅ Готово (Done)

- [x] Инициализация структуры базы знаний Docs-as-Code ({today_str}) #docs

## 💡 Идеи и гипотезы (Icebox / Future Ideas)

- [ ] [Идея 1]: краткая формулировка задумки или гипотезы #idea
"""
        kanban_path.write_text(kanban_content, encoding="utf-8")

    # 6. docs/02_Tasks/Roadmap.md
    roadmap_path = docs_dir / "02_Tasks" / "Roadmap.md"
    if not roadmap_path.exists() or force:
        roadmap_content = f"""---
id: ROADMAP
title: Дорожная карта разработки (Roadmap)
status: active
type: roadmap
created: {today_str}
updated: {today_str}
tags:
  - roadmap
  - planning
  - milestones
---

# 🗺️ Дорожная карта разработки (Roadmap): {project_name}

> **Теги:** #roadmap #planning #milestones  
> **Связанный канбан:** [[Kanban|Канбан-доска]]  
> **Первоисточник:** [[../../SPEC|SPEC.md (Мастер-спецификация)]]  

---

## Фаза 1: Первичный MVP и проверка сборки
**Цель:** Создание базового каркаса проекта и проверка сборки/тестов.  
*Сформируйте концептуальный план первой фазы через команду `/kb-plan`.*

---

## 🔮 Перспективные направления (Future Horizons / Later)
*Идеи и гипотезы, находящиеся на стадии осмысления. Прорабатываются через Режим 1 (`/kb-plan`).*

* 💡 **[Идея 1]:** Краткое описание проблемы и ценности.
"""
        roadmap_path.write_text(roadmap_content, encoding="utf-8")



# --- GIT SETUP ---

def setup_git(target_dir: Path, git_choice: str):
    """
    Handles git initialization according to user choice: 'local', 'github', or 'none'.
    """
    if git_choice == "none":
        print("⏭️ Git setup skipped.")
        return

    # Check if git command exists
    git_cmd = shutil.which("git")
    if not git_cmd and sys.platform == "win32":
        # Check standard Windows paths
        win_candidates = [
            r"C:\Program Files\Git\cmd\git.exe",
            r"C:\Program Files\Git\bin\git.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Programs\Git\cmd\git.exe"),
        ]
        for cand in win_candidates:
            if os.path.isfile(cand):
                git_cmd = cand
                break

    if not git_cmd:
        print("⚠️ Warning: 'git' executable not found in PATH. Skipping automated Git operations.")
        print("   You can initialize Git manually later with: git init")
        return

    is_git_repo = (target_dir / ".git" / "HEAD").is_file()

    if not is_git_repo:
        try:
            subprocess.run([git_cmd, "init"], cwd=str(target_dir), check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
            print("📦 Initialized local Git repository.")
        except Exception as e:
            print(f"⚠️ Git init warning: {e}")

    # Prepare .gitignore if not present
    handle_gitignore(target_dir)

    # Scope git operations strictly to target_dir
    git_env = os.environ.copy()
    git_env["GIT_DIR"] = str((target_dir / ".git").resolve())
    git_env["GIT_WORK_TREE"] = str(target_dir.resolve())

    # Initial commit
    try:
        subprocess.run([git_cmd, "add", "-A"], cwd=str(target_dir), env=git_env, check=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
        res = subprocess.run([git_cmd, "commit", "-m", "feat: initialize docs-as-code harness"], cwd=str(target_dir), env=git_env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        subprocess.run([git_cmd, "branch", "-M", "main"], cwd=str(target_dir), env=git_env, check=False, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if res.returncode == 0:
            print("✅ Created initial Git commit with Docs-as-Code harness (branch: main).")
    except Exception as e:
        print(f"⚠️ Git commit notice: {e}")

    if git_choice == "github":
        print("\n🐙 GitHub Remote Setup Instructions:")
        print("   1. Go to https://github.com/new and create a new repository.")
        print("   2. (Do NOT check README, .gitignore or license options).")
        print("   3. Run the following commands to link your repository:")
        print(f"      cd \"{target_dir.resolve()}\"")
        print("      git remote add origin https://github.com/<your-username>/<repo-name>.git")
        print("      git push -u origin main\n")


def deploy_ci_workflow(target_dir: Path, ci_provider: str = "none", assets: dict = None):
    if ci_provider == "github":
        wf_dir = target_dir / ".github" / "workflows"
        wf_dir.mkdir(parents=True, exist_ok=True)

        # 1. kb-lint.yml
        wf_lint = wf_dir / "kb-lint.yml"
        if assets and ".github/workflows/kb-lint.yml" in assets:
            wf_lint.write_text(assets[".github/workflows/kb-lint.yml"], encoding="utf-8")
        else:
            wf_lint_content = (
                "name: Docs-as-Code Knowledge Base Audit\n\n"
                "on:\n"
                "  push:\n"
                "    branches: [ main, master ]\n"
                "  pull_request:\n"
                "    branches: [ main, master ]\n\n"
                "jobs:\n"
                "  kb-lint:\n"
                "    runs-on: ubuntu-latest\n"
                "    steps:\n"
                "      - name: Checkout repository\n"
                "        uses: actions/checkout@v4\n\n"
                "      - name: Set up Python\n"
                "        uses: actions/setup-python@v5\n"
                "        with:\n"
                "          python-version: '3.11'\n\n"
                "      - name: Run Knowledge Base Linter\n"
                "        run: |\n"
                "          python scripts/kb_lint.py --path docs\n"
            )
            wf_lint.write_text(wf_lint_content, encoding="utf-8")

        # 2. release.yml
        wf_release = wf_dir / "release.yml"
        if assets and ".github/workflows/release.yml" in assets:
            wf_release.write_text(assets[".github/workflows/release.yml"], encoding="utf-8")
        else:
            wf_release_content = (
                "name: Release Automation\n\n"
                "on:\n"
                "  push:\n"
                "    tags:\n"
                "      - 'v*'\n\n"
                "permissions:\n"
                "  contents: write\n\n"
                "jobs:\n"
                "  build-and-release:\n"
                "    name: Build & Publish Release\n"
                "    runs-on: ubuntu-latest\n"
                "    steps:\n"
                "      - name: Checkout Repository\n"
                "        uses: actions/checkout@v4\n"
                "        with:\n"
                "          fetch-depth: 0\n\n"
                "      - name: Set up Python\n"
                "        uses: actions/setup-python@v5\n"
                "        with:\n"
                "          python-version: '3.11'\n\n"
                "      - name: Verify Knowledge Base Integrity\n"
                "        run: |\n"
                "          python scripts/kb_lint.py --path docs\n\n"
                "      - name: Execute Project Build Hook\n"
                "        run: |\n"
                "          if [ -f \"scripts/build_release.sh\" ]; then\n"
                "            bash scripts/build_release.sh\n"
                "          elif [ -f \"scripts/build_release.py\" ]; then\n"
                "            python scripts/build_release.py\n"
                "          elif [ -f \"package.json\" ]; then\n"
                "            npm ci && npm run build\n"
                "          fi\n\n"
                "      - name: Inspect Artifacts & Verify Checksums\n"
                "        id: release_meta\n"
                "        run: |\n"
                "          mkdir -p dist\n"
                "          python scripts/kb_release.py --version ${{ github.ref_name }} --ci-mode\n\n"
                "      - name: Publish GitHub Release\n"
                "        uses: softprops/action-gh-release@v2\n"
                "        if: startsWith(github.ref, 'refs/tags/')\n"
                "        with:\n"
                "          name: Release ${{ github.ref_name }}\n"
                "          draft: false\n"
                "          prerelease: false\n"
                "          files: |\n"
                "            dist/*\n"
            )
            wf_release.write_text(wf_release_content, encoding="utf-8")
        print("✅ Deployed GitHub Actions CI workflows (.github/workflows/kb-lint.yml, release.yml).")


# --- INSTALLATION ORCHESTRATOR & INFRASTRUCTURE HELPERS ---

def get_agent_rule_specs(target_dir: Path, project_name: str, stack_key: str, doc_lang: str):
    return [
        ("all", target_dir / "AGENTS.md", generate_agents_md(project_name, stack_key, doc_lang), "root AGENTS.md (Universal Agent Standard)"),
        ("gemini", target_dir / "GEMINI.md", generate_gemini_md(project_name, stack_key, doc_lang), "GEMINI.md (Google Antigravity & Gemini CLI)"),
        ("cline", target_dir / ".clinerules", generate_clinerules(project_name, stack_key, doc_lang), ".clinerules (VS Code Cline & Roo Code)"),
        ("claude", target_dir / "CLAUDE.md", generate_claude_md(project_name, stack_key, doc_lang), "CLAUDE.md (Claude Code CLI)"),
        ("cursor", target_dir / ".cursorrules", generate_cursorrules(project_name, stack_key, doc_lang), ".cursorrules (Cursor IDE)"),
        ("copilot", target_dir / ".github" / "copilot-instructions.md", generate_copilot_instructions(project_name, stack_key, doc_lang), ".github/copilot-instructions.md (GitHub Copilot)"),
        ("windsurf", target_dir / ".windsurfrules", generate_windsurfrules(project_name, stack_key, doc_lang), ".windsurfrules (Windsurf Cascade)"),
    ]


def deploy_infrastructure(target_dir: Path, assets: dict, stack_key: str, today_str: str) -> tuple:
    docs_dir = target_dir / "docs"
    tpl_dir = docs_dir / "00_Templates"
    tpl_dir.mkdir(parents=True, exist_ok=True)
    tpl_count = skills_count = 0

    for rel_path, content in assets.items():
        if rel_path.startswith("00_Templates/"):
            tpl_name = Path(rel_path).name
            customized = customize_templates_for_stack(tpl_name, content, stack_key, today_str)
            (tpl_dir / tpl_name).write_text(customized, encoding="utf-8")
            tpl_count += 1
        elif rel_path.startswith(".agents/skills/"):
            target_file = target_dir / rel_path
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text(content, encoding="utf-8")
            skills_count += 1
        elif rel_path == ".obsidian/graph.json":
            target_file = docs_dir / ".obsidian" / "graph.json"
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text(content, encoding="utf-8")
        elif rel_path.startswith("scripts/"):
            target_file = target_dir / rel_path
            target_file.parent.mkdir(parents=True, exist_ok=True)
            target_file.write_text(content, encoding="utf-8")
            try:
                target_file.chmod(0o755)
            except Exception:
                pass
    return tpl_count, skills_count


def run_linter_audit(target_dir: Path, docs_dir: Path):
    kb_lint_path = target_dir / "scripts" / "kb_lint.py"
    if kb_lint_path.is_file():
        print("\n🔍 Running knowledge base audit with kb_lint.py...")
        res = subprocess.run(
            [sys.executable, str(kb_lint_path), "--path", str(docs_dir)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if res.returncode == 0:
            print("✅ Linter check passed: 0 broken links, valid YAML frontmatter!")
        else:
            print(f"⚠️ Linter reported warnings:\n{res.stdout}\n{res.stderr}")


def install_harness(
    target_dir: Path,
    project_name: str,
    stack_key: str,
    agent_choice: str,
    git_choice: str,
    doc_lang: str = "ru",
    force: bool = False,
    ci_choice: str = "none",
):
    print(f"\n🚀 Installing Agent Docs-as-Code Harness into: {target_dir.resolve()}")
    print(f"   • Project Name: {project_name}")
    print(f"   • Stack: {STACK_PRESETS.get(stack_key, STACK_PRESETS['generic'])['name']}")
    print(f"   • AI Agent configs: {agent_choice}")
    print(f"   • Documentation language: {doc_lang}")
    print(f"   • Git mode: {git_choice}")
    if ci_choice != "none":
        print(f"   • CI mode: {ci_choice}")
    print()

    docs_dir = target_dir / "docs"
    if docs_dir.exists() and not force:
        print(f"⚠️ Warning: Directory '{docs_dir}' already exists.")
        print("   Existing files will be preserved. Only missing templates and directories will be created.")

    # 1. Unpack assets
    assets = unpack_assets()

    # 2. Create directory skeleton
    dirs_to_create = [
        docs_dir / "00_Templates",
        docs_dir / ".obsidian",
        docs_dir / "01_Architecture",
        docs_dir / "02_Tasks" / "Plans",
        docs_dir / "02_Tasks" / "Specs",
        docs_dir / "02_Tasks" / "Bugs",
        docs_dir / "02_Tasks" / "Releases",
        docs_dir / "03_Decisions_ADR",
        docs_dir / "04_Research",
        docs_dir / "05_Testing",
        target_dir / "scripts",
    ]

    for d in dirs_to_create:
        d.mkdir(parents=True, exist_ok=True)
        # Ensure .gitkeep in empty dirs so Git tracks them
        if not list(d.glob("*")):
            (d / ".gitkeep").touch()

    # 3. Write unpacked templates and scripts
    today_str = date.today().isoformat()
    tpl_count, skills_count = deploy_infrastructure(target_dir, assets, stack_key, today_str)
    print(f"✅ Deployed {tpl_count} templates and Obsidian graph configuration.")
    print("✅ Deployed scripts/kb_lint.py and scripts/kb_release.py.")
    if skills_count > 0:
        print(f"✅ Deployed {skills_count} AI agent skills (.agents/skills/).")

    # 4. Generate starter knowledge base documents
    create_starter_docs(target_dir, project_name, stack_key, assets=assets, force=force)
    print("✅ Created starter knowledge base docs (SPEC.md, 00_Index.md, Onboarding.md, Kanban.md, Roadmap.md, Devlog.md).")

    # 4.1. Handle README.md and .gitignore (non-destructive)
    handle_readme(target_dir, project_name, doc_lang)
    handle_gitignore(target_dir)

    # 5. Generate Agent rule files
    for agent_key, rule_path, content, desc in get_agent_rule_specs(target_dir, project_name, stack_key, doc_lang):
        if agent_choice == "all" or agent_choice == agent_key or agent_key == "all":
            rule_path.parent.mkdir(parents=True, exist_ok=True)
            rule_path.write_text(content, encoding="utf-8")
            print(f"✅ Created {desc}.")

    # 6. Verify knowledge base integrity with kb_lint.py
    run_linter_audit(target_dir, docs_dir)

    # 6.1. CI setup
    deploy_ci_workflow(target_dir, ci_choice, assets=assets)

    # 7. Git setup
    setup_git(target_dir, git_choice)

    # 8. Success banner and instructions
    print("\n" + "=" * 70)
    print(f"🎉 Agent Docs-as-Code Harness installed successfully in '{project_name}'!")
    print("=" * 70)
    print("\n📚 Next Steps for You & Your AI Agent:")
    print("  1. Open the project folder in VS Code / Cursor / Obsidian:")
    print(f"     code \"{target_dir.resolve()}\"")
    print("  2. In Obsidian: Open Vault -> choose folder 'docs/' to view the colored graph!")
    print("  3. Ask your AI Agent:")
    print("     \"Please read AGENTS.md and let's start Mode 1 (Planning) for our first task.\"")
    print("  4. Verify your documentation anytime:")
    print("     python3 scripts/kb_lint.py --path docs\n")


# --- SAFE HARNESS UPDATE ---

def record_devlog_update(docs_dir: Path, today_str: str, doc_lang: str = "ru"):
    devlog_path = docs_dir / "Devlog.md"
    if not devlog_path.is_file():
        return
    content = devlog_path.read_text(encoding="utf-8")
    if doc_lang == "en":
        entry = (
            f"### [{today_str}] — Docs-as-Code Harness Components Update (`install.py --update`)\n"
            "- **What was updated:**\n"
            "  - Note templates in `docs/00_Templates/` refreshed to latest version.\n"
            "  - Standalone utilities (`scripts/kb_lint.py`, `scripts/kb_release.py`) updated.\n"
            "  - AI agent skills in `.agents/skills/` synchronized.\n"
            "  - Obsidian graph configuration `docs/.obsidian/graph.json` refreshed.\n"
            "- **Integrity verification:**\n"
            "  - Link integrity audit performed with `kb_lint.py`.\n\n---\n\n"
        )
    else:
        entry = (
            f"### [{today_str}] — Обновление компонентов Docs-as-Code Harness (`install.py --update`)\n"
            "- **Что обновлено:**\n"
            "  - Шаблоны заметок в `docs/00_Templates/` обновлены до актуальной версии.\n"
            "  - Автономный линтер и утилиты релизов в `scripts/` обновлены.\n"
            "  - Скиллы AI-агентов в `.agents/skills/` актуализированы.\n"
            "  - Конфигурация графа `docs/.obsidian/graph.json` актуализирована.\n"
            "- **Проверка:**\n"
            "  - Проведен контрольный аудит целостности ссылок через `kb_lint.py`.\n\n---\n\n"
        )
    if "### [" in content:
        idx = content.find("### [")
        new_content = content[:idx] + entry + content[idx:]
    else:
        new_content = content.rstrip() + "\n\n---\n\n" + entry
    devlog_path.write_text(new_content, encoding="utf-8")
    print("📝 Appended update record to docs/Devlog.md.")


def update_agent_rules_safe(target_dir: Path, project_name: str, stack_key: str, doc_lang: str, backup: bool = True):
    for _, rule_path, new_content, _ in get_agent_rule_specs(target_dir, project_name, stack_key, doc_lang):
        if rule_path.is_file():
            existing = rule_path.read_text(encoding="utf-8")
            if existing.strip() != new_content.strip():
                if backup:
                    bak = rule_path.with_name(rule_path.name + ".bak")
                    bak.write_text(existing, encoding="utf-8")
                    print(f"⚠️ Backed up modified {rule_path.name} to {bak.name} and updated to latest version.")
                rule_path.write_text(new_content, encoding="utf-8")
            else:
                print(f"ℹ️ {rule_path.name} is already up to date.")


def update_harness(
    target_dir: Path,
    assets: dict = None,
    stack_key: str = None,
    doc_lang: str = None,
    project_name: str = None,
    ci_provider: str = None,
    backup: bool = True,
) -> int:
    docs_dir = target_dir / "docs"
    if not (docs_dir / "00_Index.md").is_file():
        print(f"❌ Error: 'docs/00_Index.md' not found in {target_dir.resolve()}.")
        print("   This directory does not appear to be an initialized Agent Docs-as-Code project.")
        return 1

    print(f"\n🔄 Updating Agent Docs-as-Code Harness components in: {target_dir.resolve()}")

    if assets is None:
        assets = unpack_assets()

    today_str = date.today().isoformat()

    # Detect project attributes if not specified
    if not project_name:
        spec_path = target_dir / "SPEC.md"
        if spec_path.is_file():
            spec_txt = spec_path.read_text(encoding="utf-8")
            m = re.search(r'title:\s*["\']?(?:Мастер-спецификация:\s*)?([^"\'\n]+)', spec_txt)
            if m:
                project_name = m.group(1).strip()
        if not project_name:
            project_name = target_dir.name or "Project"

    if not stack_key or stack_key == "auto":
        stack_key = detect_project_stack(target_dir)

    if not doc_lang:
        agents_path = target_dir / "AGENTS.md"
        if agents_path.is_file() and ("Russian" in agents_path.read_text(encoding="utf-8") or "Русский" in agents_path.read_text(encoding="utf-8")):
            doc_lang = "ru"
        else:
            doc_lang = "en"

    print(f"   • Project: {project_name}")
    print(f"   • Stack: {STACK_PRESETS.get(stack_key, STACK_PRESETS['generic'])['name']}")
    print(f"   • Language: {doc_lang}\n")

    # Ensure Releases directory exists (safely preserving any existing releases)
    releases_dir = docs_dir / "02_Tasks" / "Releases"
    releases_dir.mkdir(parents=True, exist_ok=True)
    if not list(releases_dir.glob("*")):
        (releases_dir / ".gitkeep").touch()

    # Refresh templates, skills, linter, graph
    tpl_count, skills_count = deploy_infrastructure(target_dir, assets, stack_key, today_str)
    print(f"✅ Refreshed {tpl_count} templates and Obsidian graph configuration.")
    print("✅ Refreshed scripts/kb_lint.py and scripts/kb_release.py.")
    if skills_count > 0:
        print(f"✅ Refreshed {skills_count} skills in .agents/skills/.")

    # Safe update of agent rules with .bak
    update_agent_rules_safe(target_dir, project_name, stack_key, doc_lang, backup=backup)

    # Record update in docs/Devlog.md
    record_devlog_update(docs_dir, today_str, doc_lang)

    # Refresh CI workflow if requested or already existing
    if ci_provider == "github" or (target_dir / ".github" / "workflows" / "kb-lint.yml").is_file():
        deploy_ci_workflow(target_dir, "github", assets=assets)

    # Run kb_lint audit
    run_linter_audit(target_dir, docs_dir)

    print("\n" + "=" * 70)
    print("🎉 Docs-as-Code Harness components successfully updated to latest version!")
    print("=" * 70 + "\n")
    return 0


# --- INTERACTIVE CLI WIZARD ---

def prompt_user_input(prompt_text: str, default: str = "") -> str:
    default_hint = f" [{default}]" if default else ""
    try:
        val = input(f"{prompt_text}{default_hint}: ").strip()
        return val if val else default
    except (EOFError, KeyboardInterrupt):
        return default


def run_interactive_wizard(args) -> tuple:
    print("""
╭──────────────────────────────────────────────────────────╮
│  ✨ Agent Docs-as-Code Harness Installer                 │
│  Zero-Dependency AI Agent Discipline & Obsidian Vault   │
╰──────────────────────────────────────────────────────────╯
""")

    # Try reopening TTY if piped through curl
    if not sys.stdin.isatty():
        try:
            if os.name != "nt" and os.path.exists("/dev/tty"):
                sys.stdin = open("/dev/tty", "r")
            elif os.name == "nt":
                sys.stdin = open("CONIN$", "r")
        except Exception:
            pass

    target_dir = Path(args.target_dir).resolve()
    default_name = args.name or target_dir.name or "MyProject"

    # 1. Project Name
    project_name = prompt_user_input("? Enter Project Name", default=default_name)

    # 2. Documentation & Agent Communication Language
    print("\n? Preferred documentation & agent communication language:")
    print("  [1] Russian (Русский) [Recommended for RU teams]")
    print("  [2] English")
    print("  [3] Custom language (type name)")
    lang_choice_input = prompt_user_input("Select [1-3]", default="1")
    if lang_choice_input == "1":
        doc_lang = "ru"
    elif lang_choice_input == "2":
        doc_lang = "en"
    elif lang_choice_input == "3":
        doc_lang = prompt_user_input("Enter language name", default="ru")
    else:
        doc_lang = "ru"

    # 3. Technology Stack
    detected_stack = detect_project_stack(target_dir)
    if args.stack and args.stack != "auto":
        detected_stack = args.stack
    stack_choice_map = {"swift": "1", "ts": "2", "python": "3", "dotnet": "4", "generic": "5"}
    detected_num = stack_choice_map.get(detected_stack, "1")

    print("\n? Select Technology Stack:")
    print(f"  [1] iOS / macOS (Swift, SwiftUI, Xcode) [Target Apple Stack]{' (Detected)' if detected_stack == 'swift' else ''}")
    print(f"  [2] Web / Node (TypeScript, JavaScript, Next.js){' (Detected)' if detected_stack == 'ts' else ''}")
    print(f"  [3] Python (Pytest, FastAPI, CLI){' (Detected)' if detected_stack == 'python' else ''}")
    print(f"  [4] .NET / C# (MAUI, ASP.NET, CoreCLR){' (Detected)' if detected_stack == 'dotnet' else ''}")
    print(f"  [5] Generic / Other{' (Detected)' if detected_stack == 'generic' else ''}")
    stack_choice = prompt_user_input("Select [1-5]", default=detected_num)
    stack_map = {"1": "swift", "2": "ts", "3": "python", "4": "dotnet", "5": "generic"}
    stack_key = stack_map.get(stack_choice, detected_stack)

    # 4. AI Agent Setup
    print("\n? Select AI Agent / IDE Setup:")
    print("  [1] All AI Agents (AGENTS.md, GEMINI.md, Cline, Claude, Cursor, Copilot, Windsurf) [Recommended]")
    print("  [2] VS Code Cline & Roo Code (.clinerules)")
    print("  [3] Claude Code CLI (CLAUDE.md)")
    print("  [4] Cursor IDE (.cursorrules)")
    print("  [5] GitHub Copilot (.github/copilot-instructions.md)")
    print("  [6] Google Antigravity & Gemini CLI (GEMINI.md)")
    print("  [7] Windsurf Cascade (.windsurfrules)")
    print("  [8] Universal AGENTS.md only")
    agent_choice_input = prompt_user_input("Select [1-8]", default="1")
    agent_map = {"1": "all", "2": "cline", "3": "claude", "4": "cursor", "5": "copilot", "6": "gemini", "7": "windsurf", "8": "generic"}
    agent_choice = agent_map.get(agent_choice_input, "all")

    # 5. Git Setup
    print("\n? Git Version Control Setup:")
    print("  [1] Local Git (Initialize repository & commit initial docs) [Recommended]")
    print("  [2] Connect to GitHub (Local commit + setup guidance)")
    print("  [3] Skip Git")
    git_choice_input = prompt_user_input("Select [1-3]", default="1")
    git_map = {"1": "local", "2": "github", "3": "none"}
    git_choice = git_map.get(git_choice_input, "local")

    # 6. CI Setup
    print("\n? Continuous Integration (CI) Workflow:")
    print("  [1] None (Local-Only / Skip CI) [Default]")
    print("  [2] GitHub Actions (.github/workflows/kb-lint.yml)")
    ci_choice_input = prompt_user_input("Select [1-2]", default="1")
    ci_map = {"1": "none", "2": "github"}
    ci_choice = ci_map.get(ci_choice_input, "none")

    return project_name, stack_key, agent_choice, git_choice, doc_lang, ci_choice


# --- MAIN ENTRY POINT ---

def main():
    parser = argparse.ArgumentParser(
        description="Agent Docs-as-Code Harness Installer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python3 install.py
  python3 install.py -y -n MyApp -s swift -a all -g local
  python3 install.py -y -d ../project -s ts -l en --ci github
""",
    )

    parser.add_argument("--name", "-n", type=str, help="Project name (default: current directory name)")
    parser.add_argument(
        "--doc-lang", "-l",
        type=str,
        default=None,
        help="Preferred documentation & agent communication language (e.g. ru, en, custom; default: ru)",
    )
    parser.add_argument(
        "--stack", "-s",
        choices=["auto", "swift", "ts", "python", "dotnet", "generic"],
        default=None,
        help="Target technology stack preset (default: auto)",
    )
    parser.add_argument(
        "--agent", "-a",
        choices=["all", "cline", "claude", "cursor", "copilot", "gemini", "windsurf", "generic"],
        default=None,
        help="AI agent / editor configuration files to generate (default: all)",
    )
    parser.add_argument(
        "--git", "-g",
        choices=["local", "github", "none"],
        default=None,
        help="Git version control strategy (default: local)",
    )
    parser.add_argument(
        "--ci",
        choices=["github", "none"],
        default=None,
        help="Continuous Integration workflow to deploy (default: none)",
    )
    parser.add_argument(
        "--target-dir", "-d",
        type=str,
        default=".",
        help="Target directory where the harness will be installed (default: current directory)",
    )
    parser.add_argument(
        "--non-interactive", "-y", "--yes",
        action="store_true",
        help="Run without interactive prompts, accepting flags or defaults",
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Overwrite existing configuration files if present",
    )
    parser.add_argument(
        "--update", "-u",
        action="store_true",
        help="Update harness infrastructure (templates, linter, skills, graph) safely in existing project",
    )

    args = parser.parse_args()
    target_dir = Path(args.target_dir).resolve()

    # Handle --update mode directly
    if args.update:
        exit_code = update_harness(
            target_dir=target_dir,
            stack_key=args.stack,
            doc_lang=args.doc_lang,
            project_name=args.name,
            ci_provider=args.ci,
        )
        sys.exit(exit_code)

    # Determine whether to run interactively
    is_interactive = not args.non_interactive and (sys.stdin.isatty() or os.name == "nt" or os.path.exists("/dev/tty"))

    # If flags were all explicitly passed, run directly
    if args.stack and args.agent and args.git and args.name:
        is_interactive = False

    if is_interactive:
        project_name, stack_key, agent_choice, git_choice, doc_lang, ci_choice = run_interactive_wizard(args)
    else:
        project_name = args.name or target_dir.name or "MyProject"
        stack_key = detect_project_stack(target_dir) if (not args.stack or args.stack == "auto") else args.stack
        agent_choice = args.agent or "all"
        git_choice = args.git or "local"
        doc_lang = args.doc_lang or "ru"
        ci_choice = args.ci or "none"

    install_harness(
        target_dir=target_dir,
        project_name=project_name,
        stack_key=stack_key,
        agent_choice=agent_choice,
        git_choice=git_choice,
        doc_lang=doc_lang,
        force=args.force,
        ci_choice=ci_choice,
    )


if __name__ == "__main__":
    main()
