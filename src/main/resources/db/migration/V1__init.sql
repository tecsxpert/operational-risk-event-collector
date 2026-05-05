-- Create the table for Risk Events
CREATE TABLE risk_events (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    event_title VARCHAR(255) NOT NULL,
    description TEXT,
    event_category VARCHAR(100) NOT NULL, -- e.g., Fraud, System Failure, Legal
    severity_level VARCHAR(50) NOT NULL,  -- e.g., Low, Medium, High, Critical
    financial_loss DECIMAL(15, 2) DEFAULT 0.00,
    occurrence_date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'OPEN'      -- e.g., OPEN, UNDER_REVIEW, CLOSED
);

-- Optional: Add an index for faster searching by category
CREATE INDEX idx_risk_category ON risk_events(event_category);