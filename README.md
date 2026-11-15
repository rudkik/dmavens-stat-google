# Dmavens · Google — дашборд баеров

Статистика воронки Chatterfy по кампаниям, в названии которых есть `Google` (`CAMPAIGN_MATCH` в `.env`, без учёта регистра).
Домен: `google.dmavens.xyz`. Открыт без токена, только чтение.

- **Статистика** — строка на каждый источник (Chatterfy Source) кампании: старты, диалоги, подписки, реги, депозиты,
  теги REG / DEP / ПОТЕНЦИАЛ, конверсии между шагами, суммы депозитов (FD / RD). Период — по дате события, дни по Москве.
- **Диалоги** — люди с регой / депозитом / тегом в периоде, со ссылкой на чат в Chatterfy.

Своей базы и ключей Chatterfy здесь нет: `server.py` (stdlib) раздаёт страницу и проксирует `/api/*` в общий сервис
синхронизации **dmavens-stat-cf**, добавляя фильтр кампаний. Что и как считается — в его README.

## Запуск

```
# сначала поднять dmavens-stat-cf (он создаёт docker-сеть dmavens-stat-net)
make up        # создаст .env из .env.example, соберёт и поднимет; порт 8082
```

Caddy (проект `dmavens-crm-obrab`, `deploy/Caddyfile`) проксирует `google.dmavens.xyz` → `host.docker.internal:8082`.

Без Docker: `CF_URL=http://localhost:8079 CAMPAIGN_MATCH=Google TITLE=Google python3 server.py 8082`.

Код одинаковый с дашбордом `dmavens-stat-fb` — отличается только `.env`; правки переносить в оба.
