-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create schema
CREATE SCHEMA IF NOT EXISTS resume_analyzer;

-- Create roles
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'readonly') THEN
        CREATE ROLE readonly;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'readwrite') THEN
        CREATE ROLE readwrite;
    END IF;
END
$$;

-- Set default privileges
ALTER DEFAULT PRIVILEGES IN SCHEMA resume_analyzer 
    GRANT SELECT ON TABLES TO readonly;
ALTER DEFAULT PRIVILEGES IN SCHEMA resume_analyzer 
    GRANT SELECT, INSERT, UPDATE ON TABLES TO readwrite;

-- Create tables
CREATE TABLE resume_analyzer.users (
    user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_registered TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE resume_analyzer.resumes (
    resume_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES resume_analyzer.users(user_id),
    file_name VARCHAR(255) NOT NULL,
    file_path TEXT NOT NULL,
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_analysis_date TIMESTAMP WITH TIME ZONE,
    vector_db_reference_id TEXT,
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE resume_analyzer.user_preferences (
    preference_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES resume_analyzer.users(user_id),
    preferred_job_title VARCHAR(100),
    preferred_location VARCHAR(100),
    preferred_salary_range VARCHAR(50),
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE resume_analyzer.analysis_results (
    analysis_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    resume_id UUID REFERENCES resume_analyzer.resumes(resume_id),
    analysis_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    summary_text TEXT,
    vector_db_reference_id TEXT,
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Create activity type enum
CREATE TYPE resume_analyzer.activity_type AS ENUM (
    'LOGIN',
    'LOGOUT',
    'UPLOAD_RESUME',
    'RUN_JOB_SEARCH',
    'UPDATE_PREFERENCES',
    'VIEW_RESULTS',
    'DOWNLOAD_REPORT'
);

-- Create user activity table
CREATE TABLE resume_analyzer.user_activity (
    activity_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES resume_analyzer.users(user_id),
    activity_type resume_analyzer.activity_type NOT NULL,
    activity_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    details JSONB,
    estimated_cost DECIMAL(10, 4),
    is_deleted BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes
CREATE INDEX idx_users_email ON resume_analyzer.users(email);
CREATE INDEX idx_resumes_user_id ON resume_analyzer.resumes(user_id);
CREATE INDEX idx_user_preferences_user_id ON resume_analyzer.user_preferences(user_id);
CREATE INDEX idx_analysis_results_resume_id ON resume_analyzer.analysis_results(resume_id);
CREATE INDEX idx_user_activity_user_id ON resume_analyzer.user_activity(user_id);
CREATE INDEX idx_user_activity_type ON resume_analyzer.user_activity(activity_type);
CREATE INDEX idx_user_activity_timestamp ON resume_analyzer.user_activity(activity_timestamp);

-- Function to add a new user with a hashed password
CREATE OR REPLACE FUNCTION resume_analyzer.add_user(
    p_username VARCHAR(50),
    p_email VARCHAR(255),
    p_password TEXT,
    p_first_name VARCHAR(50),
    p_last_name VARCHAR(50)
) RETURNS UUID AS $$
DECLARE
    v_user_id UUID;
BEGIN
    INSERT INTO resume_analyzer.users (username, email, password_hash, first_name, last_name)
    VALUES (p_username, p_email, crypt(p_password, gen_salt('bf')), p_first_name, p_last_name)
    RETURNING user_id INTO v_user_id;
    
    RETURN v_user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to soft delete a user
CREATE OR REPLACE FUNCTION resume_analyzer.soft_delete_user(p_user_id UUID) RETURNS VOID AS $$
BEGIN
    UPDATE resume_analyzer.users
    SET is_deleted = TRUE, deleted_at = CURRENT_TIMESTAMP
    WHERE user_id = p_user_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to soft delete a resume
CREATE OR REPLACE FUNCTION resume_analyzer.soft_delete_resume(p_resume_id UUID) RETURNS VOID AS $$
BEGIN
    UPDATE resume_analyzer.resumes
    SET is_deleted = TRUE, deleted_at = CURRENT_TIMESTAMP
    WHERE resume_id = p_resume_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to log user activity
CREATE OR REPLACE FUNCTION resume_analyzer.log_user_activity(
    p_user_id UUID,
    p_activity_type resume_analyzer.activity_type,
    p_details JSONB DEFAULT NULL,
    p_estimated_cost DECIMAL(10, 4) DEFAULT 0
) RETURNS UUID AS $$
DECLARE
    v_activity_id UUID;
BEGIN
    INSERT INTO resume_analyzer.user_activity (user_id, activity_type, details, estimated_cost)
    VALUES (p_user_id, p_activity_type, p_details, p_estimated_cost)
    RETURNING activity_id INTO v_activity_id;
    
    RETURN v_activity_id;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create views that exclude deleted records
CREATE OR REPLACE VIEW resume_analyzer.active_users AS
SELECT * FROM resume_analyzer.users WHERE NOT is_deleted;

CREATE OR REPLACE VIEW resume_analyzer.active_resumes AS
SELECT * FROM resume_analyzer.resumes WHERE NOT is_deleted;

CREATE OR REPLACE VIEW resume_analyzer.active_user_preferences AS
SELECT * FROM resume_analyzer.user_preferences WHERE NOT is_deleted;

CREATE OR REPLACE VIEW resume_analyzer.active_analysis_results AS
SELECT * FROM resume_analyzer.analysis_results WHERE NOT is_deleted;

CREATE OR REPLACE VIEW resume_analyzer.active_user_activities AS
SELECT * FROM resume_analyzer.user_activity WHERE NOT is_deleted;

-- Grant privileges
GRANT USAGE ON SCHEMA resume_analyzer TO readonly, readwrite;
GRANT SELECT ON ALL TABLES IN SCHEMA resume_analyzer TO readonly;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA resume_analyzer TO readwrite;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA resume_analyzer TO readwrite;

-- Grant SELECT on views
GRANT SELECT ON resume_analyzer.active_users TO readonly, readwrite;
GRANT SELECT ON resume_analyzer.active_resumes TO readonly, readwrite;
GRANT SELECT ON resume_analyzer.active_user_preferences TO readonly, readwrite;
GRANT SELECT ON resume_analyzer.active_analysis_results TO readonly, readwrite;
GRANT SELECT ON resume_analyzer.active_user_activities TO readonly, readwrite;