| Поток/Элемент        | Угроза (STRIDE)        | Риск | Контроль                            | Проверка/Артефакт                  |
|---------------------|-----------------------|------|------------------------------------|-----------------------------------|
| R1 /auth/register   | S: Spoofing           | R1   | Проверка username + CAPTCHA        | Integration test + negative signup simulation |
| R4 /auth/register   | T: Tampering          | R2   | Валидация пароля + проверка источника данных | Unit test PasswordHasher + integration test формы регистрации |
| R7 /auth/register   | I: Information disclosure | R3 | Ограниченный ответ при ошибках    | Contract/API schema test + log scan |
| L1 /auth/login      | S: Spoofing           | R4   | MFA + rate-limit на /login         | Unit test rate-limit + login attempt simulation |
| L4 /auth/login      | T: Tampering          | R5   | verify_password безопасно          | Unit test verify_password + SAST проверка |
| L7 /auth/login      | I: Information disclosure | R6 | Нормализация ошибок               | Contract/API schema test + log scan |
| W1 /workouts POST   | S: Spoofing           | R7   | Проверка JWT токена                 | Unit test JWT verification + integration test POST unauthorized |
| W1 /workouts POST   | T: Tampering          | R8   | Валидация полей тренировки + проверка ownership | Unit test Workout validation + integration test POST чужого user_id |
| W3 /workouts PATCH  | T: Tampering          | R9   | Проверка ownership + валидация     | Unit test ownership check + integration test PATCH чужого объекта |
| W4 /workouts DELETE | D: Denial of Service  | R10  | Rate-limit + проверка прав         | Load test + integration test soft delete/recovery |
| W2 /workouts GET    | I: Information disclosure | R11 | Фильтр по user_id                  | Unit test + integration test фильтрации данных |
| W3 /workouts PATCH  | E: Elevation of privilege | R12 | Проверка токена и прав             | Unit test JWT claims + code review RBAC |
