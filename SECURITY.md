# Segurança

Este repo lida com tokens de API que dão acesso a ad accounts (com poder de gastar dinheiro real). Leia antes de usar.

## O que NUNCA pode ir pro git

| Tipo | Exemplos | Por quê |
|------|----------|---------|
| Arquivos `.env` | `.env`, `.env.local`, `.env.production` | Têm tokens em texto puro |
| OAuth do Google | `client_secret*.json`, `google-ads.yaml`, `token.json`, `refresh_token*` | Dão acesso à conta Google Ads |
| Tokens de API | `*_token.txt`, `*_token.json`, qualquer arquivo com `Bearer ...` | Acesso direto às plataformas |
| Service accounts | `service-account*.json` | Identidade da máquina/app |
| Chaves SSL/SSH | `*.pem`, `*.key`, `*.p12`, `*.pfx` | Quebra autenticação inteira |
| Pastas de credenciais | `credentials/`, `secrets/` | Convenção, sempre fica fora |

O `.gitignore` deste repo já cobre todos esses padrões. **Não remova linhas dele sem entender o que faz.**

---

## Antes de cada commit

Roda:

```bash
git status
```

Se aparecer qualquer arquivo com `.env`, `secret`, `token`, `credential`, `client_secret`, **PARA**. Adicione no `.gitignore` antes de continuar.

Pra varredura mais profunda:

```bash
# procura padrões de chave em arquivos staged
git diff --cached | grep -iE "(api[_-]?key|secret|token|password|bearer|sk-[a-z0-9]|AIza[0-9A-Za-z_-])"
```

Se o grep retornar qualquer coisa, **NÃO COMMITA**. Investigue.

---

## Se você acidentalmente commitou um segredo

1. **Considere o segredo comprometido.** Mesmo que você reverta, o histórico do git guarda. Se você já deu push, o segredo virou público em segundos (bots fazem scrape de GitHub o tempo todo).

2. **Rode imediatamente:**
   - Google Ads: revogue o refresh token em https://myaccount.google.com/permissions e gere outro
   - Meta: revogue o system user token no Business Manager e gere outro
   - LinkedIn: revogue o access token no app config e gere outro

3. **Limpe o histórico do git** (só funciona ANTES de outros clonarem o repo público):
   ```bash
   # opção 1: bfg (mais fácil)
   bfg --delete-files .env
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   git push --force
   ```

4. **Se o repo é público e tem mais de uma hora desde o vazamento**, considere o vazamento permanente. Apenas a rotação de credencial salva.

---

## Boas práticas

- Nunca cole token/chave em mensagem de chat, PR, issue, screenshot
- Não rode `git add .` sem antes ter feito `git status` e revisado
- Use `git add <arquivo específico>` quando possível
- Considere instalar [git-secrets](https://github.com/awslabs/git-secrets) ou [gitleaks](https://github.com/gitleaks/gitleaks) como pre-commit hook
- Pra times: revise `.gitignore` em todo PR que mexe nele

---

## Princípio do menor privilégio nas APIs

- **Google Ads:** crie uma conta de serviço dedicada com acesso só ao MCC necessário, não ao seu Google pessoal
- **Meta:** sempre system user, nunca token de usuário pessoal. Sistema users sobrevivem a você sair da empresa.
- **LinkedIn:** scopes mínimos (`r_ads`, `rw_ads`, `r_ads_reporting`). Não pede `w_organization_social` se não vai postar.

---

## Suspeita de comprometimento?

Se você suspeita que um token vazou (mensagens estranhas no log, gastos não previstos, campanhas que você não criou):

1. Revogue o token na hora
2. Audite a ad account: o que rodou nas últimas 24h?
3. Troque a senha da conta principal
4. Habilite 2FA se ainda não tem
5. Pague o gasto e siga a vida (fazer BO não traz dinheiro de volta)
