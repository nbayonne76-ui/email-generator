-- Données d'exemple pour development_db (idempotent : ré-exécutable sans doublons)
-- Usage : psql -U postgres -h localhost -d development_db -f database/seeds/sample_data.sql

BEGIN;

-- ---------- Templates ----------
INSERT INTO templates (name, subject, body, category, variables)
SELECT 'Initial Outreach',
       'Partenariat avec {{company}}',
       E'Bonjour {{contact_name}},\n\nJe me permets de vous contacter au sujet d''une collaboration possible entre nos équipes et {{company}}.\n\nSeriez-vous disponible pour un court échange la semaine prochaine ?\n\nCordialement,\n{{sender_name}}',
       '1st_contact',
       '["contact_name", "company", "sender_name"]'::jsonb
WHERE NOT EXISTS (
    SELECT 1 FROM templates WHERE name = 'Initial Outreach' AND category = '1st_contact'
);

INSERT INTO templates (name, subject, body, category, variables)
SELECT 'Follow-up Check',
       'Suite à mon précédent message',
       E'Bonjour {{contact_name}},\n\nJe reviens vers vous concernant mon message du {{last_contact_date}}. Avez-vous eu l''occasion d''y réfléchir ?\n\nJe reste à votre disposition pour en discuter.\n\nCordialement,\n{{sender_name}}',
       'follow_up',
       '["contact_name", "last_contact_date", "sender_name"]'::jsonb
WHERE NOT EXISTS (
    SELECT 1 FROM templates WHERE name = 'Follow-up Check' AND category = 'follow_up'
);

-- ---------- Partners ----------
-- La table n'a pas de colonne dédiée au code partenaire : il est stocké dans metadata.partner_code.
INSERT INTO partners (name, email, company, contact_name, phone, metadata)
VALUES
    ('TechSolutions Inc', 'contact@techsolutions.example', 'TechSolutions Inc',
     'Alice Martin', '+33 1 23 45 67 89', '{"partner_code": "P001"}'::jsonb),
    ('DataCorp', 'hello@datacorp.example', 'DataCorp',
     'Bruno Leroy', '+33 1 98 76 54 32', '{"partner_code": "P002"}'::jsonb)
ON CONFLICT (email) DO NOTHING;

COMMIT;
