## Symfony stack

Expected profile:
- PHP
- Symfony
- Symfony Security
- Doctrine ORM/DBAL
- MySQL/InnoDB by default
- Twig where used

Rules:
- inspect `composer.json`/`composer.lock` and supported PHP/Symfony versions
- follow existing service/autowiring/configuration conventions
- keep object-level authorization in voters/policies or repository convention
- Doctrine migrations and generated SQL require review
- use the selected database vendor skill for engine-specific behavior
- avoid lazy-loading query storms from controllers/templates
- respect existing PHPUnit/PHPStan/Psalm tooling
