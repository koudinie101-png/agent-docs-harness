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
EMBEDDED_ASSETS_B64 = "eNrdfYt2HFV26K+ckXNxt9PdkmwMjIJJZEkGXfyKJGC4kq661F2SCreqeqq6ZWtsr2UgzCSXSWCAdZnFzPBaSSbrrpssYWwQBptfkH6BH7jzCXe/zququlu2J08ysaqrznOfffb77HN9bGJibSnc7naCXpiNL81duHx+emlubXp2obHdHptSY/V6fSWO2lMKXtV/Av+txL2o1wmn1MrY8sHvDvYOvj64Df/eP9g/uKsO9g5vHb51sH/4xsHdg3uHbxy+eXgLPj04+PLggYLHu4d/DR+g7OE7qytjK3HWC3r9bEoFrVbY7YVtdUx106SbZPB4w769odLwtbDFj+2wm4atgH9k/W6YQumwvRK34d2UOjlx8qn6xI/rJ5+C5s3XtfVdHDH22Qs2s6mVWKm6CtqpPKStragHPfTTcCWmOa/Ex8ycp1RxqvnZQIXn1IkTB5/B3Pdo5q9PnTgBFT+BkvsH9w/fgQ8PYMgHH8PDvYNvASr3qfqDVXgLNT/Aegd7WMtOQils99kf1esKCnx7+I46eED1cTT3D98+fMsbycE3SsNUg6ym4IM/9pUxGQS8pvYajcbKmKrXn8Np6OkfU5MNdfARjlPW8/XDN9TBvjr4Hrp8cPAFzOHuwXcHeysxj+/d0sXfgzHDA49gH+pAtzUFn2HY0MYDPS6cGrQNuEKl8c0vNHihS6iIYP0rGO6tg+8O39ajhWGehGF+6sDgrh7Q7+ElTROHoGu+CS3t0wRu4yeejVmgEkxVNGoY2m14e+vgDvy8h4Cw67DnDOZUg1eYC38J7b4Jw34bN8dt3B5Qew8BCjOoLGisnu70wjQOetFOmFVX4hOADssH78Jy/xKBKWB8A6pCE2pyFVGEZ0jIBXDC8b+th2RRC0dfoSKvw/t9APvr9PUrRDtczsNfCnpgrT2Y230aKq4AfH4Lit45fLvK0xs+qpMPNyoLsCcBYJ/gaAid7uCoEFEO3+Ee4du3h38Hb9/2278LrcNiHv4NjISr7OXXzYz64Lc0lDexFTXOOP2dYPF3CBy/+V8TqnKzDI8BWEkdjNXUICq6MPPC/NLczNJLC3MFcgrf6iPJ6T0eqIYckocc3USUgTZ2u9CET8VaaYhE0lLEyR+vxP1uu/jSpYheE/imlWx3kziMew5d/MMn7/zm/+2/U77j98qoZflMBtLMd7E1Qqz7TDPf00TnLn+R/cvN7wsB/TX8usOEippZbjTGYWXm43Z47YZ+WF1Fkpqncu+b1f25xljEgDcEtXDBZccc7GvqwnPEPfALTXhK54lk7fAXRP1pq31He0eaVLI3Ece5GXyFZPkukSLo4QHtIp/cfUBkhHHyO6TBSF2AEOGmwE0Ltb9xd1Kz2dwO0+0gAj650UmutraCtKeWZnGNlZrpRLDAy8AWPkJKxwOHjfLS/MrYKvasFsN0J2qFWOQzGv5tGjfujm80UfkGCnN7Uppr9pI02KSa/6CBTBQYNi7uxV8dfED1YIQOBf018xxAr7+SqbxN3OEecyNqCBHubb0YHxkI3uYdSwSNd3ZN0fbPtUfEcB8ptODeLezjO2IZCEHArxyV+vjgC+r4C036EVH+GtpALnZPRrIQ9tLdOmHAt7Qz9pnh4aLiO2AzPyfiAb1/QQh9G7khNPsNriNzi1GU5exLz+cJCrwq0JOPiI6/QVC7WxQDeARaFAt3wjTqgZi0HbyWpCCJrXeS1pUwhb3Vgg9RK+jAI3+Ev1GcgPBkqMOUphZINzR5isOr0A7+e0NFMfC2XrQJTC7exDaTeCNKt0mKi+I6iH2baZhl8GsjukZvryZxD55X4jSkT1ESrwEUejg3/JuNd4Pe1ngvGcdfa7ZUI7zWwyk9EgVc72+uxFeCeD2ICYhIRF6knzcAyRB0X+C/dcQQ2rl7qwQ/hzi++zFu0LuEaoCkZm3UD7c+UKNWxVDF+VkkYroqEbiPiK++QTzIMHAidRdkWS7gsgg5LFDV3yFO044liurg8l1882uYzvf08jax4vurLHxix3bihrKWAKWctn5GROl72lbfyT6G/QL77U0QRIzIRozaK2s58u+JegqdgV2Cf2H2vxSaALQA6d8DmcAD2mu3aRfvEw13ZYGP813bbj4++KwmYh7ShsN3kEYwc8vR339C6ssyYb7Xu0R9RfZaAGUlARoYdlGuA2i4AswdXBqa0m3aj9TFyYaR9h0azrTynswe2ZzInKd08Y+FEiFZ2slwLl/BbyhHMjph2vfUkxmf7tEQXWEqltNRY5WD35BYDNIjoRQAoy7SOwyvSpS7hztOKPHnVlV4YMa0b4RonO6X3LEl+SwDMl95wAI5i4/Y/0KS9NRM0M9CNR0Hnd0symgnLcxMV0erHl6/LL3xtiWtwusJAaM3rSfTn6bhoYB8n/m1t020rNpcvnBpdv7cq6tN1dSUaSPqhEiOmjRiHmtJA3opsJGLc69gCyMpnNMkLcaXJP2+TkwNpQ/hzW+wIOvM5imYzXsE7H2YLS2ysCRAV91D/VyUZj2Ab10tq1WcPmoHe8Bj/4a0zKN0OXhLeqCGbudmqw3T1a9L4SNq2nf0QuSk27wloC1b+9MjjEt0OSQg+A9M6g2RL0XlAVVQ0eb8nhQK7Kzy/MLc3EVnmB+RsQPoEuDPvSL2UNVbtPnuoqzDGHZbNWeBXzYV/3RoJ05xX5EM9z2hyJ6tEe50kk1g+M3GMKFgdu7l85cKcgG/NWLBwf/We+PgW1HLPZlmX1W4u+ogLaNNnx+Ru+rK+Pxa0gedt+Oxzvd/91AjFPb0OQnL+0jIj3EP6pi0bljYpxr3oCxqsIYGfC0iOUl0zN0GKg0kwj4gi1aenuCmOPhq1NChqEbMb4R5OXLr4VssJlokh2INj6MeU8uvwn/1Cxfqs7OrRAIOPqStgkzLWEDU0vTii/UBpiua8h3SW/ZXEZ8BPIbDInMgSnfwAIDBKzVAxM4NVQw4d8g0ZDfvfS2P5xQjLeXWeXXuAqzeFNvCHn0VE4pHpGiR3UG9B60TWTHbmwR3pvhG6kc2Mnct6oHU2Q7VRNXp+TMxO7xpSdtfIxfM9eMXM4jDUNzTXIY2/Lekv42Q4Ocvzs79JL9XEd3wvSPEg37EFiZWNRklShf1E0c/HmYl2OqvP+LmBVEG7VX8I8J94e3d33+qHnm0xhJAZPPnec5khM7Fy3MzN/AfAN2qyLkfEwl9IKa5+7R0UPpSvJ4EaRu0jRvFIkVJ9Q+ffHiPbBqaru9pqyXvCMAqLDlckSZiAaquphsgPP0D7v+q1qPtoJZRtxgxRqNQc2PYwHTa2sIOULAutb6U1FkKsisZVkLJ9UO798uan13AgiANwlPJ94UwCwMZAgptvyZiRlvDteSWDQK1P5r2BIpTn8tm9S05d0sqMrEncPHjDZdDCJC4Ek2UKrFyQpUmTq7R+3KFxXRo6y4kQXs76PqV5eUNEJIf0JC/0vLlPY0v0phItS5mvf8GyiUGl4C2Hb6Vs4XsiXZC6MLGyJHoUVOlICnlPFy6sIMa3G1zYnJt2jH9jTdxAOVSNRuI0Th816hzBbOMaVfDrymcdehi1NTDQrymmpc7QQztw9NiN2zx09n+Jj8shJ0wyIDwNs2ITq3Nhq0IZdwM/VwyVWRAhJGHt/IOlUpT+4GaVdPKk2t6K0gDA3YCgecL4ni/IPvOLRZhmgtzi3PaCOy0e3pNNoo0+3vStwhJXieuaNict3Ogo7mTc+qln5iGXK7DTX0kve+J4e4uc7ov2DJPazaYX704ffHs9EWXYbGNpN7t9DejeEqtB1nU8mW5t9UAi4lvzN0rleN6tB+PcS/qGIwnjtFypAynuH34DvHg+xov7gxEFEa+I2EU8wXetv8ADO3wb8V38aWqnA1aV7TgSWV+eOfLgiWlMh+ry2LNckr+FmS796kILhroE6gH0HfQJ66tkskTzc+kg5MIYdQygt/XuNUcrqpmk1ZWD7L6DIo0FSsUVkEGhk9mFu99hm0j4dknZAQAoxhGmxobrcy3wvXkmh4KqDbavE3YxSo06jZWl/aaYE1ZHYvaYTAMgy5dPHtpemF2/mJBRbFfrJryKQiD9xhUxif0gEwYikRIjxQevqkqllaq5/swluofX/5JTBf8exP7Eb1GFgPlS28TfHTrseZidZwSbwPt6s+tAnqbtVfWRb81bleLnWTpuGcEZLT1sI8C3kyVO+/3VBPnhsT0FIu3X5EWvmfovhikgH4U9ub+QHWq9q/CCwZICI2CTdLbOy8H/U4PyaaVXr8i39NdsmHgQqFOfg/2tsCCAYG6zNcErgekprwDC7eeRe0I6BW1yVQdVJTXUeK9Q0bPN1ljYgWHzBlkfXh1+sJ5tZEmcW876PXCVLGuaEgcEn7yZbD/HL2WLmCvRleiThRfyQxHv4xCKr0iLPl78i+g5AEI82FN/OmkyN4WFoXYQL/us63QtV6g3YftqGyGYeUH7ahvk51wX3qdhv1bn2ttJSw+aPxiZQ6hdZts39KgMyXAemj11A+33j+NXbwJg7gnqhwN4+vDv8OhYDPfaTVPkXUTdco99O7TBLFGbrlB6M1hbpl8hIVvsBhAxdAg/jlZnL7EWYBUgJEbRS8wm87fQ92dtNAb2MwU9K7K/+DnEyf+8Mknn7mdTU4ZAyMA7oZqjl9ZryPLa5KKszA3PVu/dPH8q6BP/Aqhoe1ee1UuDhT2IgoSaCOqeVxXNQt8rOmM4lN3FCenCDvsCJAHH3EE2t5QNoISLumO4XN3DKem2D1/x44iAlYSbodxD4eCJmiiAF8aEgpDxg9Uq2bkI3L77QHCvUGI52Ir8OgmtIu+q07YC5tVHIyLMqfIa6FtkA/I27KPPgaH3gnCfOSZ5G+Ue4WLSIEveHJxBPMa5x/CYGieg8UBllKRpxi35bgq6gdOJ4xJ4/6iuugHqyroV8W2HJSALwDfqjtiuxzSogGk3+opqEuLQm3+PRvZ86KNY4py+khZbDcNUqUp7bC8xR7VxRem6ydPP8VL7s13vb9pBhe0U/OcishO7X7gWqCXUG4az4URoQ6ML0tFe72s1DAQWsbOd2FZ2MJtaNsDRJx9j7jn0O3JQbo8s7c32N8l5FlYEPkKfCGfjIGTp4QnWkEfQ8QcQV9IJFbPK31sThwwFGJI++IP+8416xU1P0fvozaZw9e0al1TrLTBGpLKVlOksMF3ra5JKwVdbfAITeCSGwGkFTdpzlXauKWH09pcnU2adPQ1bvEzwGwy9hPz2Nd+C3LCsduWQ8yOoMY5hn8cUFOze3pBnXlaf9G0rA1Zjo0bsbFy4dJMNcclT4tT6A3f6cKLDmB4SwzfzuZllr+U9uMr9bMBhmyiWIWcX4tJiK7bQRQ3G0q80bfQHd7cjHqq2+90QHFIw3Xc6CI/nAOpHDBRnU2DuLUVsuzyERG77/UK/xV77KjxDSg/rllPU8LbYGg6wOEXIsV8rTyCL73N9oNO/QKKgIu7cQv7Wgi3k16okjQCnZZA3O1nW3+mzictKHop7uwy3GlXI9QPfynOJWENGE32Rg607G+7T+bjWxa0t5FEOPFrjgXaVY9B60yTq/FGFHbaarqddHuwGyRGkN3QRL6RXdzWEUeEcWadqmyfQPs6A+6ejm/BLrV2+eYgoVakPTbIEgnA5fhmQKyvBASJ0xzXSGxNGugy5pOW5ZjNJvIJj/czGghKeN8YaVWLpShLfsMy39csW3rQRUnc8r2q+Pvuk6PG2ResNxEiufKKP05kYh8Q2fs5Kb3fiq/YEykBlDzo94iQ7Ptsjfm1K7JQW+j5edPlz6BEOwxa/7Lsdqh9BiXAvF6tpcLRMYb3iWh9zx4W48yQneb5Ekx49qBIbT+WR285N4ZbK+I465W4uwX7f0pNPqpPghrBpw2mHdBikAK41jJgLSaCp2D4xDk9XpQPmrcEgy2oJcSnECxuQOkF95ha5fE6GG/2OkWq3HGVjc8IlSi6zXCOB+UhPXnP4INVR0cf7mkZ4Gx5rEigklhyQjzEtsrlNFkHTFdPqOeToJNVbWQfShZEqby4c6FYJNrAzz+n+DxarftInwgEwotNrJQ2jJTRLlbIyb5FwXtA2r8WExj7jN/JxQCVLY/4AB0RpPKXT0wLuf7LSRtq9J7EucDAQMTMx8dzT0qdEN+olUmdFoDUfiHqqPCg78nAxIqoH9rz7oBzGaRRuyyTJyDx4noJPiS8vMUxT4RxZPof4NatFaL1HT+wG4xuwmxzcfJ7ZSHmXgjskw2Oj7K9f83KkqdSgFgPpBSEiTC40gYeaqJZjLZan2xOmdgvG3aRd5Jrd7Ff9+RD1DUylg7hu1sUD+8x6n0rkR+V2WTWUacw8L/qBJ94RJvDSYtkYQ9eD0Bn7BIjb0SvrzELdvR6G+ky2OimmiLRs4yKe5P0CxEh9wZFyxTDBIiNqyaTEm7tdpntwrb4j+yW5Sh9u8F5D2i80ntzz5MFs1YadXsZsNc11Nwa3d3hzHVh7vzc9GIhhl9e13eWf9J4tfE/Vl23vdFalf466BCR1oiJv+yEKWo7xJOk0TGXR2o2bPnqMY/HttNgo6ePQlmfwEoMIvcasE1seMdpGV5v9dfXRN9e66cdfUxqG+RifOYSK2PQET9CLx0ShxMQh1fiIO1FG0GrpxlyHGyzpKE/YKwa9YVeVoxnw6/tKOuNlxfJop+JqMIuUwqXt1+3AtD56bvo/6u5Q10yF4lH3grizZBCjh6B26eM3KbOEZ3ARQfAUZDBBkG8ZwNQkdzrOsyA/55t1MR8LxZPjtk1p09LsOSokOk2mob/fzDCWXbU6RbjKFAwQlb8NdbyUNywdC8C2jfwOgFRLOX/3D99oSj66HuKzrvnRWkyrH+vD1qwvwVl7sqMxgKtN/09i2M8U7ZBTFxcu4zbzKiT9azT37yhf62uDiL2NrL4V3QkQ/Qk7cMny4ZEcXOT8uMILU7PLrjyWMEcos0b3K7+NaJhvUr/yFLBG2QGE+ONqsimqop5U/wGbIczuxF+Sjn88Alx7l8eyfTd9Pc82sz8fY5GX7Oz8XOzhFQ02YJG8/jgb3UwEVP8e2w201Yp5nz3GZVeJ/fLd3hqpNlsrgfZFu7Ry8nVMF3cCjtA+54Pe/VzUSd8Ab6p+nRnM0mB6G3jdHG2ZWQLWjgfxf1r49tB69LilFCorL9dXprCQ4axGjYxFXmNNT15+tznfAZT8TG2MlNW4eikp9C5nGSA7laimuHp2oJqhi89Qsy2NjzAgbNsr5FPH0jfqn0VtFN549DMD/7vQKMrEs5RU14tDSjQwxmsxwx3SJYpNJ/4B2HL/Oua5hVkxAckp32Rp26F1RqfvjzvnLplde4dK4Hn/fm+kvKuNbrz4aa3ZARfs91CWQMFWQ/r2jCpx/1J4dCAiFiOMZiFNxwyagE1BfLafRHrH/DY5LCvsSzW2Mf6tcSOitlIzCI1jt0kW5o3oVMC8j05BGhjb+9aG+ctJybpDu237m5vKyHUOvhnMmF9L+L3d9pgljfk3TGqYM4InD+08Jn4iO7byGLdzp4D+cpSGrTDerKxoS4EvTS6punre+6RYCKm+rQr/nCPrXqKGWn73mnko/kdD94lt5peWd0Vxm/ot5+aPvite1z98FcH901Tv1IVVwetjmy59NSt7uVTo83dJV+abGdD6E8f+Vi1PqjsgXbU4WTx+9+W05e07F/ZvUonZ8Qmyh4V9+Rf/myFDkkWRNR+RMQoIwJ94r40ZgkvLAqa+p0+p6QYG3Gwd3w0c7IBEJMDKeDPRwUfL1yanr0wfbnAY/i1DcIZoviVB+aLxDgw9kYE6ke09Zna2vAXm1CcbeDZWS+Jw8xjJBLS+xjzKGMk/NGJSTtmuy+PT9OUJcdzRukgpjF7NopprnFJDzHX5diVVhwo1oADXfRpwMO/ooALjqbgs7+VCy9fRmH5BKvZfMqQMfd9slDc1pkdfs7frTVeZ5FwQsk+dCLlsfsHeV54mxgTkxy0oLKRZWJi0ur7xZZOPkxLJ5uNvJ7ywb/IoTPmCPbIOZMVpN6Fc16qcq5PHqoXQDD8GcjhalyZ+DmdPWBgrF1NGfL3AOmX+FIMK7+tNGszwzBgdewX2mWgFQWK8UOS58QM6LwMDuHLnTvNg66gaI0gIgjYPAXR2tLDnEL2T6O4rgbcXuxpkKe8d6ENOw4F1SBugfRuPQsoZ3qehdJTyuInwMZdPwG7prVp/oZ+YMX+kegWDmcc3RFCuXBckwWDxMN7IH7zKVG3QZZ8sxqPcu7Y1C13TXzEWrsXziFiScEJgfyQj8PfzzshtP/EoWIDwT9Ybn8YF4SQMw/rnJOrQDvuO4KlA6hcngfXwmuN/nzYds+ycqsa+GL5YIu6jmRjQcYcBx12oLRsgOY46ZHOpJInmsynheNntqXZufNzS3OjBuMfqaVwmD2HfuZPHN+V8Jb9UoTSK/NZMVFDIaMDsrNaWXAUjeA+y201MlIPyeKgB+irDR/ljFL5sJfiWWbxV5ceYVOVl8M02ohaAfryKRbGWvY/syFOU6rJ0/fPfTtRUPs15Rxrw7E3TUPvisRq4uEGNMdHTo09zT1GV1OTExP/TXWDLPPbzhlcdMt8ck4h/CXU5ZtxvVAcOkkAeMBsxgY66Ib2pZfB3pIvTQS95VPoKPE9I3eEe2v+VuKCp6hB7fL4mvbhtzBq9LPdsz4GCd01AamH1ufL6kLZ6sqkvmGVmSKi9NpaMlpwlhD3x0FVmkWK2azW8oeFK3yQmKMbXAFX8JMFXCy3fG216XhzPtSQYXeof1jzoQ4cL80tLhUkAHg3MuaAoilMkFQhF5yrMfQ4uupROa+ujT9+GvjHFf9PPlir9KRicaxxeZT70ZMNGR5EGt1b7JMzOcvYfu2gFrFzkhN1DPa+HB+nzBfw8a2ix3UPXvospyTnBMZwudJ1ITVGjaPKJN2P9ZC7RIK51pvEM02+LHuMfT9H8nMgL5KACkfAmR1tw5ysKJvPjTHMY6/+ZGWll/yJOuGkxBBXujF53CUy/nPLoXJdn/w37NoyEQoPoJA97EJD6kuin/q84GDXT8GNRB4gyZTFqe4IcS9PLy7OzYIec256/vzc7Kpp2ITHOrnRnEMIgoQ6QY3RFhqJHIIY30yD7lbjtSyJkURcx124MtZKOp2gm4V1EB56YboCn3ppP6zxV7EYj7EXUr/cSq4uwabG1xtBJwud99O9XtDawviowuetqB2+FIOqkHR2QDcoqXwpBVk8znJjMCOEhyStb6ZJv1tonL49bz4ts3fyOv/BAj/th+kuTwTFpClzJPjSgqIXTGTNT1TczQ97AEiAwG1Sp9im6QffBvhmsua+SjfX6eVTpyafnnxmQn+6yQ83a8NGSy5aYwpH9xUOC33HxzA30mON5/RTz0ycfqTxmDhbMxhN2x9nQCdPPv3M06cfAz6PuzxPPv1j9Jo8dPc5T+BjDeMUoMhTTz7zCKOw8dSPCYfTExOnJx8FDn4E++ONYnLi1MmJ06fzo8A/q3nS0I4ykIZ289QLCVKaJldz7zE90rmgHV7od3pRtxMx2ZuQrzEI74vRz3JfJxuTp6VAJ4rLCuTHtJGkrbBAzIAyhuliLw3jzR4R1onG6clnnp48dfLJZ3789MSpyZNSMg27YcctODlh+7/ifXDez0Ygt8WtkHbTaV0jawWdkDt76tTE06eefmbix5Ow808/9WM9rk6ShXqsK/FN5h3FwBzkHMd+NN7P0vH1KB4P4x3Fetkp4JRjHKryYpxc7YTtzVBhGDp6Y/GQBYCj5JxfBhLty0EnQrkxU+bcXI3orgqvwXRCmE5NBXG7eCoPW97ELHnQyv8I0wQqUOLWDmYlDoG8x60Imq30M/gXAdMGKq4u04DVKdWJ1tMg3VUYOUMB+DIBEJ23u0naU9luZp4T+4jWKnkM0s1ukGJ4C4xrm+JpoFUlXy/DT5Zv5+IMzZQvLZ2rP6OSfq/bhxZj9UoUt5OrGWbfA7aI1vJoQ20FGUwvrUDvjazXhtI1wgdK0bdJ+6o6xbuhl+5O2b1jKzSc0hWAQoK868zKWL+3UX8GtqUKYVuk2RlCs06A+FLldsJrGDoMaiz+wdAn2zzqnXyAuh1uwALF7bUdXMO1NEl6FQBv2ltrR+kUTbuKEdP4IA20+qk6o0yhhsgBFen26hauNxb60Rn802BroNM7AKaC38cxXAkPVI9VG1GGbVWqCnDLfHSOZUgZxKVK1WlrVHu5ovhfGgJFi5Vfwy9mi9j3PG07If4iJUuhoeFLaLVmdkQF1rOHEIFaqR7gMXRf4sEM0Hegrc2wd6MTrIcdPnzLb45thQGlrDBfAFj64+qqiQPDjQNDTcMGmmcRYunxlZVl+F9l+X+urKyurNw4tvqn1cqfTx3Tv1dPVP8cfsMTvcGf9GH1eNWbp7TeQJQJOh09FWeyMIfWFVqnNWd/V+gFx6gRTpViPVJzGLgpC8AM2mv4tgTzB2C5CjIVOm3KwM+RhKk2VsZmkn6nreIEN3/QZqlQXQ9vMrkQfMI+G7So2dWot1VZIT18rOrtIfgIo+WiwDx6ulRNnax62N4J4woVr6rnzqhTU6XItoSsBfCRaGiBQGoM9aezMnYhyjKU3QATtoMOUGbM+1mgrrylkSoDvQR6BcOs8nx50dJ+TGwBFgq3g937NbUTpusJWvvXk6QD06WeiSREZlPDFHUxBz4pFKgAwCmSaLrfjkjIzLGUALbBdd2n3Tw3V5CGV03zuFymFPGSzNvbprMffvdLNRsBzewlwA7aCWworEtVnJ5u4irh0p8RSgtUtFpAmkmNEYDqa9ttwmpc8g40VrGD3uwk67D2J5hMmQ3TTYicQnlTVFMOveenO1miUMyA8SoqvB2kFFGtuK+KeB1rCuOJL8zR4/TzcxeXFulx5vz0S7P4VnpF1oztrEGXsECgPY1JCzjhlTHTCv80LfFP0xr/fH7uwvzFefq5miPfdnbjpr/BBNoFXyPoIj8vb8FCZkaAgu7gZANzoIQUAGtxGAWEOKMdDwIFRT1FOyHx7UyAgXQEGzijrt+08NlAwLhD8ue2gdPQza31ErPQ1cK+7ax1kyy6hiSrUVqjEWRcpFL16+qhLZtGVrGVUYUaHYyoq1RzhREwa3GyJuQT8Dnctl9NM06xXANlRXJ9ceH1NLkSEq24ghthWZiOQ2vWrgYpuu7dz8QTwjZXW2sl/RjHOaEbHbUoPpOgBpntCOBH8oij8ImBdKxIYj4i7+Acyl3EQ5CsXd+4KVykWhxqFKMk/shY9pD4FXYK49eN4PK6A4F9hkvj8QpcDeNXHV/vb44H7XRcnwYzEwji3Uo3DTcA/WHlsAOsaN9QVjQxdVAcMNMU8468kbl3aBKRVwU1fLVE6kPKzpPyebWxo/scW/8HUvnaxnZNbWebKNENEFiqxYrSJdcvaXjQVtA0D4heh7qtVstWwUiIwK+vRF2QLNgxILwAMSmIKCyGBP2tpANsS1ENX96wEFgZw7VgGKGMsOI5HPgrDGpqNM7qLT9AmHUGgHiA37BtzpPit07fztAfWDZQS/PE8Zia34wT0LEK08QmAfn7aJUkF18pSlAHNFl0l4zpcfCrvBui8P3XB99hmj33LQ1VyKHgtgEA4ytd84IPLIzzs58AVd7lktXwW+2a5l8Yc+6z3OLCeG9LyOufnrHSSx7PDK/sJajPoEhCKHY8U0BUSngQvCXy4So++r82CVtrPG8oVTE1xglu1bx+WFoRyH6uLhDa61j/pih/nl41alaaQPolWcW1I9WlRo3UrScDdao+1kBRCmLBr7JBypxEm5mkgs7vsNdqVPN0HYQoOyFXpho6I6eeTMiteuQZYaE1X/hApaHCfTOzKS9Pm0mIwFqJ0JHvaQOQuq21j/ynFOOU2rQxPaSqFXCs5q1lLb+yNRcwtRyUyvYjEBzsukwjKRv9Uprfuvq/dTxJuVJOzqh2SctFscjIg6AGkgL9MPvR61Xqm4mRWeYou3MUKEaDY4jZyhPHxIT1EABDTTyPsVFs1QSh9C6GOp+PtLYPNR5XmPZFBFooswlQ3mArH/SDanjFE8NRei4ROqqOOWOodv7+/1JLSS/oqAta9zxH8sZii2IDQaxF+4Urm1d9MdfV9D+Utl4xsoy2CWNDJZzKaPqeBONOMAc5T9U/S+Wc3mbDHl/8VaFRu+1UbwJS5sVzpB5Z2qopoaKw4EP69vqH5x9ufa7mY3X8OjRx8zgaRaQZu+xAxq/zy5sYZlgtm8xw4Z3LwHx/+5a6mMjwHGGR+vlRKRjL8GIgOFmtOeeoAuOYbrMbpr1d9YrW6hiupQg3FL4obONuGj2iMiATgAGBoJWbjw3E6U4HhoLqDSKK1XUo8pdl7a0A+PNOqSWuHNJ2jw7qGLBV+08C6KONYbh4nFYJ7dQLy+SgMElrkjrCLP/wyd/9jWNpI+tJBLMKg05va5cMJuinIJdM70eD+hLvba6fY2oRhh/36klcX+y3WhgwvJ20Qw8cWk0aAhJY3EsvlhIXWYOM6U+tnGw4G2CHYv5wz08IEKuNEXMaCj8Y2dzCwqUFGZxPQ7xlqqkhu8HTqo0qWBjYcGr3aDTqj06njkZLHmPDP/Smd0205GtbY769ps6cAR1qbQ3TY62trYxNab8I6K0ocmo/X2M63SRF8jJ9qbRD9pGCyHFmZczzb5a6Qc2IuOVG0G6vBdIkeQJQgGKFrt7Fvxh2dwYUXhBLww0UPKEb0hq3wk4XnlF01sqLSK5owyarCl0PQIrCyG6F10vPO/gXA/9oVhm0GK6RY9j2OxcH651QywgqQEu9ODZNZ9CDUf7JjJ2F2GtmJXUywGgFAD81cP4FaRONx1x0hLeORHPtZyw46sIONESf2LRBa84FiLrxp1HNltI3XaLUK2qmC2Jub42Cg8+43hMqb5wmZwgO8kMAgP4GrFwxLVQLHnpJtHBEJ31pRYobR0d6fdb1n0saQDXd7yXbHCT9Ug/IKHD4vFefTvWc68eEO7hl62ou3olgOyOqAQ6joIUNVJ6PYMrrlFiuplrQAUgnSXoFDVW9NAxRkXKSv9UUlH+hv65mzs/LlbocQzstx7k1b6a29Wn4VtBp9Ts0YokowGwWZBB68ez4hbPcBOUZUCZxhgo2N9Nwk+dJXn1KnwetokGScyPW8FyfjMAIwJthHKZcDZ3voA7RZBJVkriEauJcCAOg35BcFOq/L166SLhoXDo6WIBoTPZoUQoY82d+wGwxRsFW3+rDYtqf/XWgHMigHyrIgb4AscIpy4fZqAVLfB7kBQBXvFtTl2gOAagqS30QY/6rRkYwkpskLqHFf2swmTLAWEb4obvkIiagRy6LcFsmkg9Q0wYEver4zOpKRqaGLCJ6jyjjdASY3w3WcYtGxilSJ9lqM+qxV1a/BHJHu89/yxvTGSWMZ9Vth3enX4nfcdaa0ooR9b/VX/fr0bi2YBiR/x7eBf3eFswnarEu6H4tZMS5gTFQNhXOWBFwgELWZAWiLYLc8/pb7yuuSqN1te3xKgqI95cH3YRu9JrAGEOpzpn4VP1Rw7r8K8Mcv+G4avlWGbrlVS3kS6sbuJfXtvAv/55fh/JSJM5TLKC7CDUTtmeWgAlO4+pW1EK/C0GrOtRzB+LAGjIHZAzIhg2JagAXrRTlwmVplanDTp2pF8s29SirA6+I2mEdm6xjmytjq7USu/nV9hmDEmXfgy5GOa4x0TqzpKP8cga38NrAb6SinMmDEv8rStIuDBosx7IkcUZNiDPbKSDETjwlLOmwBFciRjNmLzvIuzrANiUWaTH/C8KWxEpla/ztKIs1csGC9XV8l4Yb/OaFuenZ8hU7yqodfeVGrd7wFSxZRWclGTz5dRyg4pj10RRilQK1TCv+Yg9Ys4KExWMvXz3u8VFWj2vqpetiDGwHdKr/7OvF03rY9bL0HlcMlX6nLX/VaI9OlK+dnwZ5yLKJyPxIm46ZCz6DNl8nToI/uNP/7MvH03vY5XO57upQT4zlv7IzpcP8zhzancvEeYeb34N8Llr6wZhN7ZfXlbRXbIhPxUVULSAUJzrCt+L6VI65apqDqCVcf8tn+j4PEmGkOJZy2UAElKOKBmJgwSo+0frPIQXIbI+AzQaoRQnuMZfZ5monU03fhlWwiaUErVBGqQxYZrG+DBxsKaawwIkTsUpAqXGmtIavKeTjshEdjEInpgWj0RlTQQVTyuVi3lHfXbY6Aqo/ZToc+skypevXVITBK8iat6J2OxSPQoPLzogZI8ysEUNVXjyrxtWFs1UCnrZ4oHKv+hTc+9STCopA/2FAhojWVp98BNTkAs00o6BUDJVsR5gyVC1fXxkjD/wYxZnX5GCP8xP7dn9Sdj15cXO1UapzURyuzNRzDnsfSuxush7L5kZJm920FM5ucCE0H/XCbaSJWZICGlVsT70wpa6qUwX/A9axIalKWikJF2sUw8TKIqBwQciCLGaXBkPMZQZFmoZAXlvf7VHcMPWPKFmpwp81WgCvNBmOki5IF1iUuDnshCrGKm6UEAU5aoHYoKZ0LGTlqdOnTz01iFfwJBp8vLtCVXOkiWe1Ruh3RpffCq+1o80w6xWFUqQSdpLPnVGTEyefVCfoTxkhw7KwxBRVOnbdqTquKk7V6lTj5MZN2BX5sxklbptR7dJQGpPQ3ItnLYnw4ng5WGJD8udeN5hyM9+9wVvtsb9eHIvdeaadWlkpvSH1CEoLmW0qEywvZDevXb5cyZsPGQ07POBVw0E5sJII2LLIeo8qGxg6Z5CSdDvoWXq8pq2maz30TlRGkAui1/Dkkedz1GZmDbDUFNJIIf+OpZh2npDeRgnR85MxezRtZezEwXv5C4XuSnrVptz6xjkp9pwkAHQnuE6zzpfV2vtqJBXenp9GltJKVhaTPqhi2pRfbZywKI3nGSnw2rXmDEs2qy8OcPK57vFFWJTPFZOl67y1UplSevEl7V8513CN1fwuhyVM1GUd+o4+niguhTLNSW+2DWy7eR3KLR9HlDu+ehNT2fIL3CHwQpkSvBekjLzDfcZvjDnYrCN59huvJVFcoV4LZ7jcAGHvFNcIY+8i3TWifZA44cIRnSvhbn0n6PRzJxzoCOTlXSzuoSWQ76DMgHnTw1oZ44iTTDJ/bFIjkj7cZBooP9/kn2161jvaVNLqxvaaHPGiGsuTDgYgwMlfzGW4R1oFT46gYhQ3GBZ1MRv/G0owV47THxvG6T1lbMpEAOfJIiwUBg52zCgENFMImMlqoTCUg3/LFUduBv7Vn+Xv8ZWx4/oZHgvObwTqMrS6yrU9NNYAd852Ul40V9bNnfHi73F/ewqdWDlkLiO3Q8RgcrChHIs9W4eFJCgmx5tEcWfj/gGBcSDUvdYWxbfrATWMF6O/CdVnOnQtDkyM3OEhOqdKmqPM4KYqJ0Ke1hfpoLvPVskn/i4Re0Et6nd6U6NAkncf9DiLAaZg9n0D/c2y1zhK77VrZx91/E2WnkdqVbvJhly+Ps6AF+8HPkpMtxPHbM9hAOrjTzm1YXVBXa9sBBT2AQVI2nYkdVspf0yueJzD1H/4Ix3lgfHlEbL28JDt8IiHiMxst81JiBKWUFaBjrSSdxqkzO3GZogkg16UdsAbgPZDedSzDsqx7UZ80jHnCDtawHCxSxL9TONk0jSbsrwNESlfRh5GouKR+4L9k+8LX5n+SuAzQAlgtAdwddaD1hXKBpALXVIGWNt8cnagQQ5EjYnrZgw315gh4MAM2pBSuSHr6JQtK3oEG54PlUFOGxiaU3DQUsM+XovaLrJFdKrTonxGyqjm64CFyxOrA+yalHDMbYteFJurDlqRmWS72++F9ugDnayxERn2Omp9TeWgll4JMeJe9WEN8WgE8Y1ns/76Bp0Sem78WRwMko/nBpl3O2u9hPPl5yhA8XxdjioOmJ6cZ9rAU0Dj190OnON5y1P1U6sFZdKxfALhXjZMY3WIcun4gsl9K0tdG1ZS1muKV3JoUZwNlsS/QwtqS+uURQvXY4QZZAFkA5q4mYPlEYL+favlyQZF78ipVHg6AkPj44WGn+lag9gZfM9zM1NlNDPTtf+teJnp71+blRmHYumyYzSfOcNTQrqkNh+iYxxhp5XOJVbTKWza5UfgZL1LiZuBwRBiNJiWHaV2jnw4QP+PQD1YtHwY4sGQ/HekHfz0r0UlTjVI3BeLM0jYpVSicNbYkAhdZRCJgO95EmGqjKQQuvK/FYUw/f2noBAU56JvPy2NdZE1LaUEZq6PRAmOUtvbt2VXSF33Whm9eVkBfJjNy5P/L7p5Cyot2zMkMjc0Hjxt3BUHsbnmz1rKfeuGvAzjnbUo3kjyNrTakbxTXst5U1ypdUBqZP1tGPAuDY98l8YYqufDFwx6MZcSUQoFS83czwtIMnOvlL0/kTKTAgUyZOAI4cyu8ZvDf3FMvcimjgAgczQMmp8Y4I2OtlbtGCLSCzZ5h+xcNzXMPugl7WCXQiPsvFGd0n018KFBpSp4QCBhD4EmGtsceq+XUXYwe4VrOZ+wMfM6kR25im7AhhAprrS55V7hKEtm+MO2eOyd0FWO3zPRs16WhwRvoezhbY8KG4MF2Or1upmTYwxBZGJPTPiHxC9zhOVf2DiRKR4sNTI1Pm4/jHuEHE8p64YbQFuM37MQr5kfg3kGAeTJVVuuABV0uZnCN8dTrcYBCoxfh3+c7Fqgn/N90uyyFguwvFrbbsuOE8TXTmCj9eJu0/RaBKscUyZPgi3saFW5mTqdOv6FOp2EWj6OdPD46s0b+By14Qlv/8MfRErhtz3KlbNGlLSLzZr85jq1s3+Xub1z3c9RjmnOx5zMSKDFqI3omgc+0kseBnQsKRY0ngLkRKLMAU66ywNt3QHaugu09SMALdcmAUwnqXfuI0Ov2B2bQNlctHZL8uDTVWuc/prundIXkmHqegvi+wJ9faWk53t74MOb7MUW1CTfPQyoma8XJMcCqIX/51NncXd5UAcOqAMX1MERQJ1rk0Bdeo01OyGLF1fglXS3KLfJPUqHngPsbb6ki5yaeJXAL12AWg8ve2PPHN316yyKd81DFMMy9Pmcks78lWbU4hqfDrO9Lk+sLmv3/CpJ4cYFjFBCmRPT3u6EjZ9FXU3p6YDp7loWRwCxHpM7/D/nqsviTZm3nesvVUUOwcAU/Isw6dAfxxz4g75ZvCSTT9mU9XQW20L/SevSIvylWzNX4tx9mfkOqDFyPFNRLFcPlLmMs1gcb+IwJ5bIDZW01kSioYA9ejKR6mwbPfhYZ9r3LgO0l9cq4g9yd8TXdGMCZlfX97Lvy/1agF2OhbVhB+EeMLWL6YcPDXEvl1Y3W8PnF3gy1dzDvAIsz/VD4wtyIJdUMtczm0rihh5eSS5sNpXEwT2ikr7H2VbTbnCq6NSqGres3XxGMLW+8FIQVfNnggsbSeESmGVyUrYxEhUu+2Y5ofSmb/o0ZW9a82zt3t3eOUlTbqpyyxfvZ9W3el8nafOmd6W3EV7K7/O+7ktCN937va/jA71x8e56Hto3j3THNv4UAP2HuG572IoMuG2b97m+oMq5bdup61yibW5fkGUxnz6lGyT3D77j62O+oBGZS2KoxnGJXRZ3wnFXVj/OK3mc0fT4eVIULqGn6HLQuhJshsdNV9CK0vd80+ib/66XfKvK3LWw1ScHyiITW9jB1x0qfDPf2KB7u/U54IugYjBfPQblf/jtP6mD31n5FIvzbbZfubcCafkdO29tpZXJiaoQCiv4Vm/qRv/wybu/oUuHc3f+yX0md9zbMFQFpdtzKN0WGhcB0W34nd/QNW0DZBe5AF1zErxiEGS5QrsiDVULsMN7vA3C6+HuFS721jfielFU3Lu5Fdu//ft6TgYq9Iw3b/8aGrE3bv1cXzj9IH+ti1wv+K0sj3PfcUnwGPXuSzM3y/Dv93Rn7Ld8J+bA25jkQqZ9uoftnpbCzY30IKheszc9leo67s7P837njlc9W3l7WzVlb8lFSn5Pdkx0mScvhbmrS1Wa9sqL8WZV0bU93xOe3Lfgzd0xhc3/YxHMeNXQF1r2pYvitITMNznrW3W/kkueYQvL5WeqmJBfccoIMk7ra6WcaZVg3m0TZMg3XvN9wUfFSR1oTreH4e0zv6A9tOfP2t8B36h8AsOBehQPr9y767F8WUQ/5Ibzr7PMYK1/mNOjkks+PTKxh5V3/BQff+R8CXrso9NzoKwyKCGIk5dD9y01VCVsbDbUROPJxgTK1jv0VB2dhoSDTKQ7tICa7iZt7hGKioB9uA6gDLIsaUV4XoPDYntboZFLRvWGC17HzIsD5sc5OkblPKlIhSn6MHqOuAuG9orqe0mveGSitFf4MLpXnSNl5EoucbIdHXVs4pE5/ntEL8Laj9CNlQ60UoZOntHAS3fraT8enSjmMgaEF2cBgOTDcSZw9Woa8QVCo3qm7Af6ePmI3klE4xpefgQ0uFKoOmXcGNlnK6prK/Hw/hb6aFlQM/MsOeJ2F6lyWkwN/9qZeJwcPEfNwjMo74Hr8kD/5xHyWrj5AymPjVTC1SokEsS0JI12f7ubVXQ3NYAekNHemZM16Bozg6wFWSuK+HhctZhtfyIX8KiT52S5DB1OQjWOM1OGqmJcVxr+tA9bui300n4zlNO+MjT0YS4DcL0f7hgfygViDCiZPntiEyeZ9N5SCA87FQvJEaiiYY2i94Yec6PMTHkXlk55VBosTKdTeLYcpGcRjnuw6v0oD53jpTtjYOL4EI1IeMZ253zW6HXG4Jlj2NSDPmOeCg3jVM/YR+e7EE3uVn7UDE/P7YV0dw1oZgEtc+AYguSwuYuLyju+arqRJDqkqVpcKQlt0pIV/dzAex58AUsLJ7pXSeXc2L6Cp+f4R8anWvmujLXkCv2s5uohaQ85eCA3V9zlJdEEPtyGJCLFzIzaldk2XEZn+55S180YbFzMwDykoLtNm/3QgnXuJJs2lamxYQ2s/8t3vWRXbNK5rlFu+Ti+QIPaAAu7l+FQy3Fs/9g0Uwx65XOSFJvOKC1i1wYOpeoa2V1kO0pyPJOUjAVsyUjWCDYRLcazK1Gnk423RdjFY8rjiy/Onz/vXlHLVlG3DIrsRt5G05OXU49SB2ESi6yLKbPSfieE2Z0i5kzvNzrJVb4szBw10/d+ZQ3PNuW1Cwwa387AyNOgo1KAcNmVZQC7NGC3AXCmBqw2X/JGwm5uFDQIKyZ2gl3MBIC5myiRJ48dIxUialg1zbUqpNewWv37f8Yo2G1saoHGhF9uqKU02tyEAd5QdAT7htIZ1+BxEeGubmCxYcep4HMT1Mh6FEc9POg0D3+xdivYwKhYUcKaNTV5ylwpAKC+JJeJKrpMFA9I2TZMmwlfl4nNvgAyCvyZDXfCDiaF5aVBDFGJuVQTT8AHvWwrDHvSom3BNIp5Vpt6xpPwsHBuBrlcq59llN9NX03fUCdOXEzoDu7GiRPSoNQ2raFz17R2EicOrE8tTS++SLenkgaDJCrljHAw6NlktrRlackCFO3DuP+b0vophK5+mesiAA2xbgIwBJqmAadVXcaMGVtdJMzuJDHI7rtxa0rhFdQ1xTeZ1ihigJt0apsWhVY2FYJSiM0N71w/vatpjZ/bQ9GE2zT1bZPr/c0mLTYdtLmhzieb5j5amu7CzLSEOmwC4pMwhdeGSotc3bQWtFNujeOj4HF6dgHb+onCHG6p6Jlp+Bqn5JUMedIY13ZmyxdjNmm2/IyPc4tz0wszL9AQY8ydQm2uA1PaQgkkM5M11U2TaIDB5uiSKvhL3sVdJ8OsubLQXFMorUlNs8vZImkvoDpPtEJVZA8SgW42m6SXxfRuJf7hg9/+8MEt+J8qu+CXU3HQFt2Jwqsg/MPy90K3mnNNnh8sf4EvT5oR2ayCNHFXdZOIJBOvAXsJudsAUIzsCmBHj5ZX3xri1vSvCR23OYJ3MeoNdnUAU9nO1BN2D3r1tWkoH+fPXo2aEkMf0AS8L2a8xgeZxjl3I/xxDgw4reZj8XSrObTzh2LvXB33c/a4mBXFO2g65JySfn1rVfSnwifP8CpPfWs65wnBmAKvBXM5fOH4xBYIIgl8i1p0IeaOei3p48lQrP2B1LY3G3stHHM+qM1+hHwZHbnGQ/BPwDB2ghSwDkeDN1RfDtPtgFMLA22UXJlIdjPmx2iJB6Ycqhh4QQoSyQ7uWTwajkIAbOatMFYcw93gFhcMlaifQ68ytntWt8Il+bBOsIHcOmBrGybnRpqCYYGUQQObmo57UX2utZVgG7MJH40DxZPzaayDAMpZQVtbQe/PMHPuDnJlitb8U3Xqh1vvn4bxdwCljb+a211cvLREwwq3gp0oQdkhMnChcbZD0I/CdpHDl8hKTLYGSUn8tSAfLTAtdDeUpZn6o2BwTbLVEDbh/r4GAjjsr3ZYTzY2ZKHyBNUXm2SQZPl0+oSJ5zsVv8lK/BJwFlpdlJL6aHYFJSgzRF49SydvmmifagHYM0W3s6nAa92Mku6vpOiPDiw9DxZpreqD6E2WEL8ii2CoabvYC9QN5DiQWzX6XkBWStR3Qc9/ukMnqdE2Rjg9B3i7i7BU2/0MD1p3O1Er6qGBSfQNkkdg10BlvOEj4vBE4UsIW4RAOwQWS1d3oIjZCa6i+BhQ3Z8C9+Wk5FBwW3BsNmxzHhxnZLMLNKJXEKoBLiVFyXLSZ9AIEA0zh+qg3kDSqB5dkBlwAU7AWGCcAYxM94STJJc6CIIHH/NVRAdfq4MHh2+oZ8lj4VyG9FyTuWZT+8g1BjXRytdFuhADcABOMDqyxAWbAYbfIEHtp4SN23hv8RXar7RIlzGJUxszusaTKHaZFDhqfhZmTgpInU4Pa3dBnno3OaxvCwnONehyB8RuQo8n6+0IRZn5WdiRsjFwQ57EfmZTICZUCz7ZjmYYRAO60q3Un8VLmJ7DDS45eKSCyylN9CzUElJAXZyL6IKBKWa8MOInEAgw4O2a3VoVA2Md5N7EVS9CvlojFIfthEatJ8qRWlVgNbZi4g+EiONpBGy1ynQA64c/7eP1y7gspxA8L1EGGEWCg4XOdBuTz6KUEMV2ylq6AFjEeBdXJtmZT6nKkZ2v6NB6siFO9UWQcVUFhoWXgmKcc9XBBBBMgUY2cWEDGE75QqnC2PT6gpKFiXGpfot+qPq2ZAdHZ291SgudRhrgxV4Z021c7mdbnKLLzdbHZ0AG0nu8KW8wvYevg+i9nGb3xWs04c4EeMxxGsCzmwERqIDMzSmi8uxULc3OEqssEnjolwi8SPIgx28iNj9BYaRLII9doTOww0k7NiKknfk8n7sPVJZs9K4Kb4Tmh9PlwqjRn9CKQJ2xJFlgceGlxSUQ3bGnNGn3W9oThbzElw2I3p6bnj+/COU38NI4HD/eQYiAujy9uDi3KFKFfGhQFgFKYYOSjHFaBAVdJsKbxtOoJfRuK1oHXqRFGiskWfmJRBI/N0GJmNQOKepI9btJ7ORcK9DLKbNaAa5WgXziChIJ9YinlwOByDba7THiX8hnUxCtCZV9WrlAY8YGfSLpNSm1H45AQiUikACqVqcP8tji0gIaGuUKlp0MHSPAMWENWfrCYxN4ghs1BrkyfuCWyFE01hxwFkjMkEsiEJoc2/AP6uBXh39LsQ0PDr5UlbPQCcjVVaa9GALzzpfq4D0Ob/0CmSQQssp8jKtCyAElowKsuUthAcOJHJM3QQ+al9Z0hFZR0xjsAnSq42jdDG8Qrbo+cTJUKY88C3SkMo8+r6D91iEgCnUWZ8lz20tvQGxG9maFRCa8w6aq0We624Utci5CRuIYSOQm0IzzFVF2wz5I7x1xKPubzQj57lpajFwEgd09xm/4JIbCtwEsTX2EdEo9+yr8V79woT47+5xZEQ87gP6xsoVNX4CN6eEJWqIP3qfFp5ApVUFrzKiVd3gntkPljEYnchWpIXTtnzd5GOPp4VgzI8gBs608m7WSbvgc8TG+OcjgCAl6z2lritfHEMwp52fa0jSEqekiBc7Gdq0pQAmYAKY41Laymuq766Bj5Ma1oQt4jpKIGN71losXeZuxtiGD013iuuh+OWDjifz9LQjiUSzPtP2sHjrwPtFOQbrbcePPs17YlSujCIvbw/ng5YCvbMedhxEm7K501Fk0V9mzXHzXbrFHuUZqBDu6aHiPojhoim2ntAeSl1LJxjAHs+t01miQ9C6lCcpoGbBy23xhc0h2BooteW5cw9HhHFMgSQ7Y1ng0HHc1o0t+UzNubIUBSqNNCsj8DEOXSP58Hed98J5/igZ3sRM5eqpq9IQ825DpEFVAizCTBspVcUQG8ThkRNurafFxqWlwzYqdPY3cI5IS3DtkJZxwuSk2PoGaBqvfQ4Nzc/naqvRrNDymVM3l5aFreEP/Xl01dHaaIuctec2PyZJEI4fraJVkQyKesxrzBA/n+SSoWDZIksFdoEkn3snknQqxXWMgxxGj7uhGXLxTJN1WE7kL2eKnNIkWYvwEERLbz4kTEhirzvKVG4CGwtTNtAj2KG020dNGNBmoSRquk31+O0zxtja5SQfJdU2kRUXnGfXJMinSMB0vAeG6Ukfi1gbFkpomtmGUqAbupbxGhK053MRQHOPYeFZW5jnO6oucieO3dGs4xKaq5HkKCgZPI7Q4rGzGYvPFPlBhBys2iJpyOoWICbG+kbgrd/mA2JpcZSStEcZsbyOCwYzpKuygaF21+8sJ9OR7VThCCqVVx3GinuVzss8NNuYZT84QbmjKDGSHg3xHHp7TVbYwx3ak5bG6JQdFJmh69big6UmzQHdrjOJ9tkmX+eH5wBDUkUyHd7FER8drYNRdNLUC+iFrMT0NZ4TkqJtub4UpWiZ82dEoXldRwQNR37G+4pBNf009xCZ1DWLYThLBMBCr0R5GJAJ7846MGSs080c0u5FeEvlws5kYNd4gutImNvjqtYteCm2oxpUT1A+tia9ceEC5oWaXHebNXWoWZHdQxfMCVm3MXcCLIusB9DENeGEBUNvd3iCGTvImWpXQu+QQTeCtD83PG7jGRDyDjQ1W7fgqR8TpMjixwQdHQFdU6quKhLYAqOp1po0DiAwxcKa2OPfFHkZWbO66NNkjjbMcNon58NDoTGIMEcpXEhC52L4MsIcBMhFtDCDtKKDjClxjQWhcwGdprqHz9XUi2nloGR4+J8vsb1hXDGmjK5Ju7GQNjfwkbMvoyCFg3hbaKncSGSkW8LYiIM7yxblXkIg2ly9cmp0/9yo/z86dn1uaW6WIc7EB4o4kg6/cO+iY4YFLYZS0cqOkmSWjzo/GfNxMO5jxne84e9KdZQEHfC6NaB119L1rHCzBUXyAib0YZMX1ftQhbU/4Of0GLm5Hj+2Q8JD1I8yJIPWlPPC9fhz1qADa0BPc/fWMamS2EXEAY0gMU7kJ3le4+XlcmRY85g2pdje8t4YvoaHHIRxdUQAqc7b96oDdD8s4WB8h/mTDVGDFNrTChRWJdJTRByILUdzt9wYzPIDSMF4HnwtsDgNPIu7ei7UxYTbDQ1Bqci8t4p4YJnXu/ALTwxAX5HdOlzklr+IOYaTziuNeyLb50z7pZaCZELz6XSp/JXeZLjprZHuMYHLBRtjbtQwHRB4JBgCUwEw8u0LPakKo7fDEoLlNJEAydnTTcIeinlvoYIvxqm3EYQrLE8ZT2J/Y7ULYQceoYavEeTiaCkgIEF6Qvy/zHiH5mtP0PR8N5BuyRTi0nUwUpFZEdno8LTrn7txfqqm2CU/KB0sUXDU68gpnIo3bQAmkBUXDo32bi0+wHzRT47iC4ntmdlD/wsuXSz6zebU28ISL/VTwZpkvTsCBfemIrJpHwFp2EgC1nh6wa+Kzm5mFlZTJg8fGkQAHNdutlXSSlGL02jqexJA+aQjJFWzWVhAn7FUy29Zat3yQa1ovDcwg6moHA98oP2C0XuCCu57GtVMbrC/Xhqi6TFDyaqcm3ILAT+j4CET2P4LSyJdONqyCgxqj5GaNDLVq1/CUDR4/wZ0uEg8RodoRlLYp3ZIXb4kXZtOWoqMXg3UZnMMQ0o6fC6SdI6MKRFCCoaborm4bL1XTqjNfKC0CQj7leZGsY9dE1ssvXB5BwzkWC9k0apO4KESRsKQN2xLRSLv5WdagW3uHk/Fyoop9D6Gkp9ROFKhmEX+aLqk+y7A6rwNu8Hr65vKygebqKpmM8OjIjpb6yAavzb8wVaK15H3Xp3K4HCkDrS3GyFI6jogu99Iv0jjtHhCpTcc1N5vNLma0yDCjhbw70g6x9YX2z2N3wMl66hIFuLvyukDjFT174pnI6TCaIoOJUiAwuxQo5Ieu2OVcvvpWc8q6ZkV3x744x/fRQ5svwz5sEz3bNvEihKEYdxGmeNsqiMwRURgyq+MDWyfp1W6X3uDR/aZxQS3IipyL4jZddO5aOlxzkgQU9UhJqpGnBFpMMhPCoWdExtgtSm7LCbgpaCZov8YIIOl0EdSG5jhSpaZL6KvdCoNOb0tUCQwoyCgo0N/TA4mGhPEOoRtSohj1HWUwCXTt6sDhJBeQVgj7dqKImXT8tB/BTuZLvQtUQ5oTN7fu5Ak1TbHJlruMoh8mUlmTkC2WqWlzINaZw5BGL4KhFeA3hIgYWwc2Swxyoc98kTY9Tt9KaAEVJkJGMel4LxDeSY2bPMHYqoHxaKX7/DIGvnrwQIlNoOxwZlmtNNzQQ9WXphCQToDW0cFsM1oPIiDI+skS87XFuy3ahCd5X1Dsqg00dHe8hIFXbGw46dGzJiAczRPnZhqiCxvLEzBVzyvvNndSmqOQbmpuLt4EaIUUouTbqB6m3VPSrhPZ/UQurFu8vLiKOXNSLeddzayLC22rtquSAMyhgZdeRIFrLNQNDoy/lMNyfmAFOpaImqKWLEoIBk6Y5rwYTKB5XYwvEjN+JBeYCJ3D4DA0JeHFZP1tulN8Aw07frQmMeugZ8moRr5zWPZ5JBIuiqI+4NATI5D6kqQj/XkxTKgB0xjydGgg8UOkHEL58HO5zXeSYsDQQI3BDYGELdQQnXnt9UkHJvuEjZcF9zLGRnEdFMke9mptvtATajJkEh/H9kdRO6pu4jUpuheYhDgYiMnIiQw03zkq1IgYn7np2fqli+dfZce63lfQGk8QOZoQT7Yek5QCO25xaWF+Zun8q+rywqUX5s/OL83NiozEffRZ+rkMHCAGgZn0TdBRQoAN3hSJkZnbGCvZBvWrpraiza0O/H/PWqUoKo6BnmwAeqnJH269fxIqRHSwvwUajw2nG2gsZbljVixHqD3Mc2w9numB2bl0bU6iSlF8CUT1p0UQ8oPBm4C7Xei74iwJTuE5jPqj2y/DtmcXEhYU9Lii3ZIXE6XTHhQo6TyfBpUYmA/+BTMRcmae7yWL3v7BbZ3gBCNC/UQtlDnlXJ/Mny+AGv4zDIEdV/OtcD25VurO9LNzKL6G5QRMn5aHhdWpExzG8zNip21YX0XXHyHNBGZbU2kQX7Gxt2JHiDAhGupPgFIoEnFUGNnvI0D2yTrd/ZMGHDrB3okwIG+aRIITyK0fSRNmPMuUXeH1sfpcTWVAWonTu/hRs/G52GAMrA1n5s8VNGPQjGCWulnyZMgGG3e3FG7PXdqCHK6VRZux5pwznUDUVIPvjkS8qwk4rjtgN8khLTRA8JRsQHhDufsIMKmFgPwpwBs3BqIiOlQAUjYGh4PCxEoLWkoYXFGkWhC97iaI96iDkveuZk3+IArwYT4KQccwVBODg2CYJs8N1KuYQG3CUi2gkPMin8hAAvob6tJ6L6BYTNlbslCsxwmv0v4pffHmaeYp5Gv2jc5lgXNiEBoUc9zUJFvi50qCiv2WdPmHi5jDWm5MMQYX2WiEowS0jQhT01oJGh0T4voY4cCbeoo8LQB+unbT+cBWi030NWA4MS2/lzpkKC1gjKDIAvS87oAgiDG44+YUFx7b8jztDx8n7MNeDQCAGjjGI0UR41a1YcSGh/MC0yQlymmdV+MxI4vFTT1EAjFZ4woRxuzght00habj+gZzRXZE1DjRIztRQNtJrjhHBOUEOa+JOTFYFEO0Dx0lEd3dTJ9i3vvrnSN6nAuOeM+XEXiKhcQFoMeJ87U5V3IOlU0MP9ZnbjGjiNjGyWhLovXFuZfnFoBwUhHivuZsSGJOJqFFtKNPDl22cH0+YFfvZaM/4GIj7FC3I5k6DUnDaEdpb1duXpP4B+w9irUeQTym6ZiMSCzPhtn4X8roxA2MdLBBquJao2z6I5Q3rM1fDKebW028/XuIRqnnTbb/7NGspxU/0MZz5GlZ0XHo5Vx0tEHFLINwpWwSuTI2xESsf2ImshEmaDXDWAKKhBolzxBfdrMDPMEi+CyZczzPH7+SM/tNTjwIM/Z3P8BIEsv8qYG5ZTiUR7Vp05kXPMdnafe+ALvX9qsx3O5smTOzHc4ZRp7RmjVPUmEXJ2pmh4GmH9j2uELVYSJxwp1oT9aGvoELRSlKleJfWmrCpCUZgqEcszrdwyhUcjJ32XQuRDyUpLxSFw2bsxnyRyUkMwnzm96NsGIEoSioEICB+oJJzqklDGJWvuXa8eNjTKcgnE3U3z6K8FxH0YiC6jSZ1J5+FANmXpi++Pzc+UvPe9ICB+FxNLI3Eab8/e2sLEhZs16i3NmWq8wIhiKiO3FtWN+eOouBV7BxIwAsY1DqsGMMp2CRNNi0VfSE+NDZ5pZ5Id+5DWZTJ5xoDCdp57AR+eNoi2mLQ+lMUgmynRZuXreHSHUsG8UU/3FDDEkUMr6JIfxfvITDBAAuMuiMkVGDU1fW8o820yLgJfNZps1T9vR8Tp/AqzpTNAkVxQFpH+WBy7rXeffUNEUb6eGOkgukNWOooIEpe9htaxcUEVitkA3jzkHJzEx6fPryvOpGPaRKI2QEzE1lI1SeQDsegkNcsmSo1QoUQ6pOrMkqT86BSMBQ4PodtrZLL1Pq0iIsO2hKaB6FJ8BZhDPQys006cci5OPSA02rqZfm1TrgK4oOGB66TflHQBGDT6gwxK3dXPBNhucwGZlOaKtvuoPMKWirObyRFW2h9ryryLDIIjmenE52Juje4E1hzuIWj8E64Qj2+CcSR0R3VJYf4wyo6xv3DzGV6GR4/tNFZcOlefnquHzIpYG04NEY0+FZjd7FySG0qTR52eQASwyEs2sNBpFWwq3azTffwrj6HLiR16aNqoOJdwcdSnXm7s7q4RRIXdNT9zjKcUofRwWYvODsnzmcxgydkLBwg/cGTNk4x/Nw5lj4smTowQWiBwyXWXM4+VLXDwOD97TqsKDuCWhVwUDgLiIliTx+gHA86Bg4ynu54+PoTBPZ3Uk9At3hUSpoCTsbcMJZs3H3YCwASKuh/hlZ6x45yjnZJ1UFEyAfvk4WtTvmpgk5FmvVWXHOObqn1Wzd9BT5DtUTT6hSTVUT0OoUteTRe3PqtZFXS0foo0iihvAi/FxuDj85NdgNkwuJJv9ASdqeo1rHiYwa6/jJKXti5chh0NSEYTwmqEAfsfdGP37w+cGHxIH4Hjfp9t/cWD5H7vEZDTftWWRoMqw4dmA9dLMeiP4DkmlpkChqICZOdDRNJ1APIux+fNVo2u7Ed9vzqsb8KZlVyQZl+0PxkG+T0oJgXumz2byGxDivnZNLZZs+EfewaBARH9pgSez0EUg61nLJOY9jN79XRgb61uiOeBuWCYQcJSQ07AXymw9LyE1tIBDHbfQI2hgx9DxbI2wuuB5tb4B4lZJw3izvAxWtvoYqJvrI3Nj4aq4/jC3boMgnaBBUeTxOhXGes9UTJ0qPeeZOc1HghGtGHXoQS5/iGnnea+TpzSMZLBlPBhksj2aXRJIklN45w2OMknjYDs/3ycgfzirJxotxHaKR6Tu+GrvbHeQBTP6L+bKRWkj+VlQEp0xeVHsJS10d3zlxHAvi+bOI/NT8VVJLApumAFcs8lqyzt/IFlGHeWnrobTHA2GriBghYXYL9l4NRTS+jnypv96Pe/067TO534nOYzhD4+ZmdDw/nkjOIqQcNtsj8A1K40GyzrgO/f+LnSdtEeRp3s1OG2GvtVVvwwbbmrJJQW2HeN653xW73aCuYEH73TrrnX+xc3pId1ymbi5KOX6qMTl5vNitWMxy8XfzWkV10pn2oZUbxS5GhoLle9RmrMvC6aw5a1hngKzLqr6Bt1GWWq+yrZUxtfpnSPhzV6jjhU1qYKXYvWJ+VCfd3UGd5GBRqDagGzG3UbzuoKbj7rZqRSjw4ROel6bWPdyKimDWPmCbFfUJvdgz2iTk3BjYnjKZfbfDXjBsKSiFrKp3yUozHCFKjXZ/cv26kpsLQarmC7tu3lQ2U3dhLnpP+5e85DcJ5iZBH202ztulvrmlKcVf7Jx0b0ecEqHtFbwW0Q6lpo7Dv3SHYTZ+vDpkd/m0r3xCbvk2ihFTaCXNvDt8QZvWtKz4kaS/HOyVmMaARt/8/2R3TEA="
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
