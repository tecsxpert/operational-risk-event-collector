package com.internship.tool.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;
import org.springframework.http.*;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestClientException;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * AiServiceClient — HTTP client for the Flask AI microservice.
 * <p>
 * Day 4 (AI Developer 1) task: RestTemplate calls to all Flask endpoints,
 * 10-second timeout, null return on error.
 * <p>
 * All methods return null on any error — callers must handle null gracefully.
 */
@Component
public class AiServiceClient {

    private static final Logger log = LoggerFactory.getLogger(AiServiceClient.class);

    @Value("${ai.service.url:http://ai-service:5000}")
    private String aiServiceUrl;

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    public AiServiceClient(RestTemplate restTemplate, ObjectMapper objectMapper) {
        this.restTemplate = restTemplate;
        this.objectMapper = objectMapper;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // POST /api/ai/describe
    // ─────────────────────────────────────────────────────────────────────────

    /**
     * Call the AI /describe endpoint to get a structured risk analysis.
     *
     * @param title       event title
     * @param description event description
     * @param eventDate   ISO 8601 date string (nullable)
     * @param department  affected department (nullable)
     * @return parsed JSON node, or null if AI service is unavailable
     */
    public JsonNode describe(String title, String description,
                             String eventDate, String department) {
        String url = aiServiceUrl + "/api/ai/describe";
        Map<String, String> body = new HashMap<>();
        body.put("title", title);
        body.put("description", description);
        if (eventDate != null)   body.put("event_date", eventDate);
        if (department != null)  body.put("department", department);
        return post(url, body);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // POST /api/ai/recommend
    // ─────────────────────────────────────────────────────────────────────────

    /**
     * Call the AI /recommend endpoint to get 3 risk mitigation recommendations.
     *
     * @param title       event title
     * @param description event description
     * @param severity    severity string (nullable)
     * @param riskScore   numeric risk score (nullable)
     * @return parsed JSON node, or null if AI service is unavailable
     */
    public JsonNode recommend(String title, String description,
                              String severity, Integer riskScore) {
        String url = aiServiceUrl + "/api/ai/recommend";
        Map<String, Object> body = new HashMap<>();
        body.put("title", title);
        body.put("description", description);
        if (severity != null)  body.put("severity", severity);
        if (riskScore != null) body.put("risk_score", riskScore);
        return post(url, body);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // POST /api/ai/generate-report
    // ─────────────────────────────────────────────────────────────────────────

    /**
     * Call the AI /generate-report endpoint to generate a comprehensive risk report.
     *
     * @param events          list of risk event maps (title, severity, risk_score, event_type)
     * @param reportingPeriod human-readable period string (e.g. "April 2026")
     * @param reportTitle     optional custom report title
     * @return parsed JSON node, or null if AI service is unavailable
     */
    public JsonNode generateReport(List<Map<String, Object>> events,
                                   String reportingPeriod,
                                   String reportTitle) {
        String url = aiServiceUrl + "/api/ai/generate-report";
        Map<String, Object> body = new HashMap<>();
        body.put("events", events);
        if (reportingPeriod != null) body.put("reporting_period", reportingPeriod);
        if (reportTitle != null)     body.put("report_title", reportTitle);
        return post(url, body);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // GET /health
    // ─────────────────────────────────────────────────────────────────────────

    /**
     * Check the AI service health.
     *
     * @return parsed health JSON node, or null if unavailable
     */
    public JsonNode health() {
        String url = aiServiceUrl + "/health";
        try {
            ResponseEntity<String> response = restTemplate.getForEntity(url, String.class);
            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                return objectMapper.readTree(response.getBody());
            }
        } catch (ResourceAccessException e) {
            log.warn("AI service /health unreachable (connection timeout): {}", e.getMessage());
        } catch (Exception e) {
            log.error("AI service /health unexpected error: {}", e.getMessage());
        }
        return null;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Internal — shared POST helper
    // ─────────────────────────────────────────────────────────────────────────

    private JsonNode post(String url, Object requestBody) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Object> entity = new HttpEntity<>(requestBody, headers);

            ResponseEntity<String> response = restTemplate.postForEntity(url, entity, String.class);

            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                JsonNode node = objectMapper.readTree(response.getBody());
                log.info("AI service call success: POST {}", url);
                return node;
            } else {
                log.warn("AI service returned non-2xx: {} for POST {}", response.getStatusCode(), url);
                return null;
            }

        } catch (ResourceAccessException e) {
            log.warn("AI service unreachable (timeout/connection refused): POST {} — {}", url, e.getMessage());
            return null;
        } catch (RestClientException e) {
            log.error("AI service REST error: POST {} — {}", url, e.getMessage());
            return null;
        } catch (Exception e) {
            log.error("AI service unexpected error: POST {} — {}", url, e.getMessage());
            return null;
        }
    }
}
