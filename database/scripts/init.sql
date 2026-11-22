-- Initialisation de la base development_db
-- Usage : psql -U postgres -h localhost -f database/scripts/init.sql

SELECT 'CREATE DATABASE development_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'development_db')\gexec

\connect development_db

CREATE TABLE IF NOT EXISTS templates (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(255) NOT NULL,
    subject     VARCHAR(500) NOT NULL,
    body        TEXT NOT NULL,
    category    VARCHAR(100),
    variables   JSONB NOT NULL DEFAULT '[]'::jsonb,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS partners (
    id            SERIAL PRIMARY KEY,
    name          VARCHAR(255) NOT NULL,
    email         VARCHAR(255) NOT NULL UNIQUE,
    company       VARCHAR(255),
    contact_name  VARCHAR(255),
    phone         VARCHAR(50),
    metadata      JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS generated_emails (
    id           SERIAL PRIMARY KEY,
    template_id  INTEGER REFERENCES templates(id) ON DELETE SET NULL,
    partner_id   INTEGER REFERENCES partners(id) ON DELETE CASCADE,
    subject      VARCHAR(500) NOT NULL,
    body         TEXT NOT NULL,
    status       VARCHAR(20) NOT NULL DEFAULT 'draft'
                 CHECK (status IN ('draft', 'sent', 'failed')),
    sent_at      TIMESTAMPTZ,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_generated_emails_template_id ON generated_emails(template_id);
CREATE INDEX IF NOT EXISTS idx_generated_emails_partner_id  ON generated_emails(partner_id);
CREATE INDEX IF NOT EXISTS idx_generated_emails_status      ON generated_emails(status);

-- Mise à jour automatique de updated_at
CREATE OR REPLACE FUNCTION set_updated_at() RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_templates_updated_at ON templates;
CREATE TRIGGER trg_templates_updated_at BEFORE UPDATE ON templates
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_partners_updated_at ON partners;
CREATE TRIGGER trg_partners_updated_at BEFORE UPDATE ON partners
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
