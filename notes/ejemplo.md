Yo (Gustavo) le paso a Juan \$1000
Pedro le pasa a Juan \$1000

```sql
UPDATE cuentas SET saldo = saldo - 1000 WHERE id = 1; -- GUSTAVO
UPDATE cuentas SET saldo = saldo + 1000 WHERE id = 2; -- JUAN
UPDATE cuentas SET saldo = saldo - 1000 WHERE id = 3; -- PEDRO
UPDATE cuentas SET saldo = saldo + 1000 WHERE id = 2; -- JUAN
```

## Saldo de Juan

