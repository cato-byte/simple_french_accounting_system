-- 📦 Esquema PostgreSQL: Aplicación de Contabilidad Simple
-- Autor: Cato
-- Propósito: Almacenar usuarios, clientes, facturas, gastos e informes

-- Eliminar el esquema si existe y volver a crearlo (usar con precaución en desarrollo)
DROP SCHEMA IF EXISTS accounting_app CASCADE;
CREATE SCHEMA accounting_app;
SET search_path TO accounting_app;


-- Tabla USERS (Capa de autenticación)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT now()
);

-- CLIENTS table (for invoice targets)
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    email TEXT,
    address TEXT,
    created_at TIMESTAMP DEFAULT now()
);
CREATE INDEX idx_clients_user_id ON clients(user_id);

-- INVOICES table (core income records)
CREATE TABLE invoices (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    client_id INTEGER REFERENCES clients(id) ON DELETE SET NULL,
    invoice_number TEXT NOT NULL,
    invoice_date DATE NOT NULL,
    description TEXT NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    payment_method TEXT CHECK (payment_method IN ('cash', 'transfer')),
    is_sent BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT now(),
    UNIQUE (user_id, invoice_number)
);
CREATE INDEX idx_invoices_user_date ON invoices(user_id, invoice_date);

-- MONTHLY REPORTS table (generated PDFs summary)
CREATE TABLE monthly_reports (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    month DATE NOT NULL, -- Represent the month with first day (e.g., '2025-04-01')
    s3_url TEXT,
    generated_at TIMESTAMP DEFAULT now(),
    UNIQUE(user_id, month)
);
CREATE INDEX idx_reports_user_month ON monthly_reports(user_id, month);

-- EXPENSES table (optional tracking)
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    expense_date DATE NOT NULL,
    vendor TEXT NOT NULL,
    description TEXT,
    amount NUMERIC(10, 2) NOT NULL,
    payment_method TEXT CHECK (payment_method IN ('cash', 'transfer')),
    invoice_number TEXT,
    created_at TIMESTAMP DEFAULT now()
);
CREATE INDEX idx_expenses_user_date ON expenses(user_id, expense_date);

-- ✔️ Schema created for accounting_app
