package com.internship.tool.service;

import com.internship.tool.entity.RiskEvent;
import com.internship.tool.exception.ResourceNotFoundException;
import com.internship.tool.repository.RiskEventRepository;
import com.internship.tool.dto.RiskEventRequest;
import com.internship.tool.dto.RiskEventResponse;
import com.internship.tool.specification.RiskEventSpecification;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class RiskEventService {

    private final RiskEventRepository repository;
    private final AiServiceClient aiServiceClient;

    public RiskEventService(RiskEventRepository repository, AiServiceClient aiServiceClient) {
        this.repository = repository;
        this.aiServiceClient = aiServiceClient;
    }

    // 🔹 CREATE
    public RiskEventResponse createRiskEvent(RiskEventRequest request) {

        RiskEvent event = new RiskEvent();

        event.setTitle(request.getTitle());
        event.setDescription(request.getDescription());
        event.setCategory(request.getCategory());
        event.setSeverity(request.getSeverity());
        event.setStatus(request.getStatus());

        RiskEvent saved = repository.save(event);

        enrichWithAiDescription(saved.getId(), saved.getTitle(), saved.getDescription());

        return mapToResponse(saved);
    }

    @org.springframework.scheduling.annotation.Async
    public void enrichWithAiDescription(Long id, String title, String description) {
        try {
            com.fasterxml.jackson.databind.JsonNode result = aiServiceClient.describe(title, description, null, null);
            if (result != null && result.has("analysis") && result.get("analysis").has("description")) {
                repository.findById(id).ifPresent(event -> {
                    event.setAiDescription(result.get("analysis").get("description").asText());
                    repository.save(event);
                });
            } else if (result != null && result.has("description")) {
                repository.findById(id).ifPresent(event -> {
                    event.setAiDescription(result.get("description").asText());
                    repository.save(event);
                });
            }
        } catch (Exception e) {
            // handle null/error gracefully
        }
    }

    // 🔹 GET ALL
    public List<RiskEventResponse> getAllRiskEvents() {
        return repository.findAll()
                .stream()
                .map(this::mapToResponse)
                .toList();
    }

    // 🔹 GET ALL WITH PAGINATION
    public Page<RiskEventResponse> getAllWithPagination(Pageable pageable) {
        return repository.findAll(pageable)
                .map(this::mapToResponse);
    }

    // 🔥 UPDATED — ADVANCED SEARCH WITH PAGINATION
    public Page<RiskEventResponse> advancedSearch(
            String keyword,
            String category,
            String severity,
            String status,
            Pageable pageable
    ) {

        Specification<RiskEvent> spec = Specification
                .where(RiskEventSpecification.hasKeyword(keyword))
                .and(RiskEventSpecification.hasCategory(category))
                .and(RiskEventSpecification.hasSeverity(severity))
                .and(RiskEventSpecification.hasStatus(status));

        return repository.findAll(spec, pageable)
                .map(this::mapToResponse);
    }

    // 🔹 GET BY ID
    public RiskEventResponse getById(Long id) {

        RiskEvent event = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException(
                        "RiskEvent not found with id: " + id
                ));

        return mapToResponse(event);
    }

    // 🔹 UPDATE
    public RiskEventResponse updateRiskEvent(Long id, RiskEventRequest request) {

        RiskEvent event = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException(
                        "RiskEvent not found with id: " + id
                ));

        event.setTitle(request.getTitle());
        event.setDescription(request.getDescription());
        event.setCategory(request.getCategory());
        event.setSeverity(request.getSeverity());
        event.setStatus(request.getStatus());

        RiskEvent updated = repository.save(event);

        return mapToResponse(updated);
    }

    // 🔹 DELETE
    public void deleteRiskEvent(Long id) {

        RiskEvent event = repository.findById(id)
                .orElseThrow(() -> new ResourceNotFoundException(
                        "RiskEvent not found with id: " + id
                ));

        repository.delete(event);
    }

    // 🔹 MAPPING
    private RiskEventResponse mapToResponse(RiskEvent event) {
        return RiskEventResponse.builder()
                .id(event.getId())
                .title(event.getTitle())
                .description(event.getDescription())
                .category(event.getCategory())
                .severity(event.getSeverity())
                .status(event.getStatus())
                .createdAt(event.getCreatedAt())
                .updatedAt(event.getUpdatedAt())
                .build();
    }
}