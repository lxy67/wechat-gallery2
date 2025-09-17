-- Create extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Countries table
CREATE TABLE IF NOT EXISTS countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Regions table
CREATE TABLE IF NOT EXISTS regions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    country_id INTEGER REFERENCES countries(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, country_id)
);

-- Diseases table
CREATE TABLE IF NOT EXISTS diseases (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Drug resistance table
CREATE TABLE IF NOT EXISTS drug_resistances (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Strains table (main data)
CREATE TABLE IF NOT EXISTS strains (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    strain_id VARCHAR(255) NOT NULL UNIQUE,
    gene_seq TEXT NOT NULL,
    country_id INTEGER REFERENCES countries(id) ON DELETE SET NULL,
    region_id INTEGER REFERENCES regions(id) ON DELETE SET NULL,
    disease_id INTEGER REFERENCES diseases(id) ON DELETE SET NULL,
    drug_resistance_id INTEGER REFERENCES drug_resistances(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_strains_strain_id ON strains(strain_id);
CREATE INDEX IF NOT EXISTS idx_strains_country_id ON strains(country_id);
CREATE INDEX IF NOT EXISTS idx_strains_region_id ON strains(region_id);
CREATE INDEX IF NOT EXISTS idx_strains_disease_id ON strains(disease_id);
CREATE INDEX IF NOT EXISTS idx_strains_drug_resistance_id ON strains(drug_resistance_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update updated_at on row update
CREATE TRIGGER update_strains_updated_at
BEFORE UPDATE ON strains
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();
