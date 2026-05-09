package com.internship.tool.service;

import com.internship.tool.entity.RiskEvent;
import com.internship.tool.repository.RiskEventRepository;
import jakarta.persistence.EntityNotFoundException;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.internship.tool.aop.Auditable;

import java.util.List;
import java.util.UUID;

@Service
@RequiredArgsConstructor
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
    private final RiskEventRepository riskEventRepository;

    public Page<RiskEvent> getAllEvents(Pageable pageable) {
        return riskEventRepository.findByIsDeletedFalse(pageable);
    }
    
    public List<RiskEvent> getAllEventsList() {
        return riskEventRepository.findByIsDeletedFalse();
    }

    public Page<RiskEvent> searchEvents(String query, Pageable pageable) {
        if (query == null || query.trim().isEmpty()) {
            return getAllEvents(pageable);
        }
        return riskEventRepository.searchEvents(query, pageable);
    }

    public RiskEvent getEventById(UUID id) {
        RiskEvent event = riskEventRepository.findById(id)
                .orElseThrow(() -> new EntityNotFoundException("RiskEvent not found with id: " + id));
        if (event.getIsDeleted()) {
            throw new EntityNotFoundException("RiskEvent not found with id: " + id);
        }
        return event;
    }

    @Transactional
    @Auditable(action = "CREATE")
    public RiskEvent createEvent(RiskEvent riskEvent) {
        // Set default values if needed
        return riskEventRepository.save(riskEvent);
    }

    @Transactional
    @Auditable(action = "UPDATE")
    public RiskEvent updateEvent(UUID id, RiskEvent eventDetails) {
        RiskEvent existingEvent = getEventById(id);
        
        existingEvent.setTitle(eventDetails.getTitle());
        existingEvent.setDescription(eventDetails.getDescription());
        existingEvent.setStatus(eventDetails.getStatus());
        existingEvent.setSeverity(eventDetails.getSeverity());
        existingEvent.setCategory(eventDetails.getCategory());
        existingEvent.setOccurredAt(eventDetails.getOccurredAt());
        
        if (eventDetails.getAiScore() != null) {
             existingEvent.setAiScore(eventDetails.getAiScore());
        }
        if (eventDetails.getAiAnalysis() != null) {
             existingEvent.setAiAnalysis(eventDetails.getAiAnalysis());
        }

        return riskEventRepository.save(existingEvent);
    }

    @Transactional
    @Auditable(action = "DELETE")
    public void deleteEvent(UUID id) {
        RiskEvent existingEvent = getEventById(id);
        existingEvent.setIsDeleted(true);
        riskEventRepository.save(existingEvent);
    }
}
