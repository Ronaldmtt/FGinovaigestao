#!/usr/bin/env python3
"""
Gera um refresh token OAuth do Google para a conta do hub, uma única vez,
sem depender de usuário interno do Gestão.

Uso:
    python scripts/get_google_hub_refresh_token.py

Fluxo:
1. Lê GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET e REDIRECT_URI do .env
2. Gera a URL de consentimento do Google
3. Pede para você abrir a URL num navegador e autenticar com a conta do hub
4. Recebe de volta a URL final do callback (ou só o code)
5. Troca o code por access_token + refresh_token
6. Imprime um bloco pronto para colar no .env

Observações:
- Para garantir refresh_token, o script envia access_type=offline e prompt=consent
- Se o Google já tiver concedido acesso e não devolver refresh_token, revogue o app
  na conta Google do hub e rode de novo
- Esse script NÃO grava nada sozinho no banco nem no .env
"""

import json
import os
import sys
from urllib.parse import parse_qs, urlparse

from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session


load_dotenv()

SCOPES = [
    'openid',
    'email',
    'profile',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events',
]
TOKEN_URL = 'https://oauth2.googleapis.com/token'
AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'


def fail(message: str, code: int = 1):
    print(f'\n[ERRO] {message}\n')
    raise SystemExit(code)


def get_required_env(name: str) -> str:
    value = (os.environ.get(name) or '').strip()
    if not value:
        fail(f'Variável obrigatória ausente no ambiente/.env: {name}')
    return value


def extract_code(user_input: str) -> str:
    raw = (user_input or '').strip()
    if not raw:
        fail('Nenhuma entrada recebida. Cole a URL final do callback ou apenas o parâmetro code.')

    if 'code=' in raw:
        parsed = urlparse(raw)
        query = parse_qs(parsed.query)
        code = (query.get('code') or [''])[0].strip()
        if not code:
            fail('Não consegui extrair o parâmetro code da URL informada.')
        return code

    return raw


def main():
    client_id = get_required_env('GOOGLE_OAUTH_CLIENT_ID')
    client_secret = get_required_env('GOOGLE_OAUTH_CLIENT_SECRET')
    redirect_uri = get_required_env('REDIRECT_URI')

    oauth = OAuth2Session(client_id=client_id, redirect_uri=redirect_uri, scope=SCOPES)
    authorization_url, state = oauth.authorization_url(
        AUTH_URL,
        access_type='offline',
        prompt='consent',
        include_granted_scopes='true',
    )

    print('\n=== Google Hub Refresh Token Bootstrap ===\n')
    print('1) Abra a URL abaixo em um navegador onde você consiga logar com a conta Google do hub.')
    print('2) Faça o consentimento.')
    print('3) Quando o navegador cair no callback, copie a URL completa da barra de endereço.')
    print('   Se preferir, pode copiar só o valor do parâmetro code.')
    print('\nURL de autorização:\n')
    print(authorization_url)
    print('\nRedirect URI esperado:')
    print(redirect_uri)
    print('\nConta sugerida: a conta Google do hub\n')

    user_input = input('Cole aqui a URL final do callback (ou apenas o code):\n> ')
    code = extract_code(user_input)

    token = oauth.fetch_token(
        TOKEN_URL,
        code=code,
        client_secret=client_secret,
        include_client_id=True,
    )

    refresh_token = (token.get('refresh_token') or '').strip()
    if not refresh_token:
        fail(
            'O Google não devolveu refresh_token. Revogue o acesso anterior da aplicação na conta do hub e rode o script de novo.'
        )

    payload = {
        'token': token.get('access_token'),
        'refresh_token': refresh_token,
        'token_uri': TOKEN_URL,
        'client_id': client_id,
        'client_secret': client_secret,
        'scopes': token.get('scope', '').split() if isinstance(token.get('scope'), str) else token.get('scope', SCOPES),
        'expiry': None,
    }

    print('\n[SUCCESS] Refresh token obtido com sucesso.\n')
    print('Bloco sugerido para .env (integração compartilhada do hub):\n')
    print(f"GOOGLE_SHARED_ACCOUNT_EMAIL=hub@inovailab.com")
    print(f"GOOGLE_SHARED_REFRESH_TOKEN={refresh_token}")
    print('\nSe você ainda quiser usar JSON compartilhado temporariamente, o payload é:\n')
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print('\nGuarde isso com segurança.\n')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\nInterrompido pelo usuário.\n')
        sys.exit(130)
