# Подключение к Supabase PostgreSQL

## Важно: Direct connection не работает с IPv4

Supabase Direct (`db.xxx.supabase.co`) использует **только IPv6**. На многих сетях это даёт `getaddrinfo failed`.

## Решение: Session pooler (поддерживает IPv4)

1. Открой **Supabase Dashboard** → свой проект
2. Нажми **Connect** (кнопка вверху)
3. Выбери **Session** (не Direct, не Transaction)
4. Скопируй **URI** целиком — он будет вида:
   ```
   postgres://postgres.XXXXXXXX:[YOUR-PASSWORD]@aws-0-eu-central-1.pooler.supabase.com:5432/postgres
   ```
5. Замени `[YOUR-PASSWORD]` на свой пароль. Если в пароле есть `;` → замени на `%3B`
6. Вставь в `.env` как `DB_URL=...`

Регион (`eu-central-1`, `us-east-1` и т.д.) **должен совпадать** с твоим проектом — копируй из дашборда, не подставляй вручную.
